import os
import unittest

import numpy as np

from ctsndfile.libsndfile import SndFile, OPEN_MODES, FILE_FORMATS

CURR_DIR = os.path.dirname(os.path.abspath(__file__))


class TestSndFile(unittest.TestCase):

    test_filename = os.path.join(CURR_DIR, "test.wav")
    test_file = open(test_filename, "r")

    def test_open_filename(self):
        f = SndFile(self.test_filename)
        self.assertEqual(f.samplerate, 8000)
        self.assertEqual(f.format, FILE_FORMATS.SF_FORMAT_WAV | FILE_FORMATS.SF_FORMAT_PCM_16)
        self.assertEqual(f.channels, 1)
        f.close()

    def test_read_all(self):
        f = SndFile(self.test_filename)
        data, n_samples = f.read(dtype=np.float64)
        self.assertEqual(n_samples, 19968)
        f.close()

        f = SndFile(self.test_filename)
        data, n_samples = f.read(dtype="float64")
        self.assertEqual(n_samples, 19968)
        f.close()

        f = SndFile(self.test_filename)
        data, n_samples = f.read(dtype="short")
        self.assertEqual(n_samples, 19968)
        f.close()

    def test_read_all_from_file(self):
        _f = open(self.test_filename, "r")
        f = SndFile(_f)
        data, n_samples = f.read(dtype=np.float64)
        self.assertEqual(n_samples, 19968)
        f.close()
        _f.close()

    def test_write(self):
        f = SndFile(self.test_filename)
        data, n_samples = f.read(dtype=np.float64)
        self.assertEqual(n_samples, 19968)
        f.close()

        f = SndFile(self.test_filename + "_tmp", open_mode=OPEN_MODES.SFM_WRITE,
                    writeSamplerate=8000,
                    writeFormat=FILE_FORMATS.SF_FORMAT_WAV|FILE_FORMATS.SF_FORMAT_PCM_16,
                    writeNbChannels=1)
        f.write(data)
        f.close()

        f = SndFile(self.test_filename + "_tmp")
        data2, n_samples2 = f.read(dtype=np.float64)
        f.close()

        self.assertEqual(n_samples, n_samples2)
        self.assertEqual(data[100], data2[100])

    def test_write_from_file(self):
        _f = open(self.test_filename, "r")
        f = SndFile(_f)
        data, n_samples = f.read(dtype=np.float64)
        f.close()
        _f.close()

        _g = open(self.test_filename + "_tmp", "w")


        g = SndFile(_g, writeSamplerate=8000,
                    open_mode=OPEN_MODES.SFM_WRITE,
                    writeFormat=FILE_FORMATS.SF_FORMAT_WAV|FILE_FORMATS.SF_FORMAT_PCM_16,
                    writeNbChannels=1)
        g.write(data)
        g.close()
        _g.close()


if __name__=="__main__":
    with SndFile("LS100673.WAV") as f:
        #print various information
        print f
        #read from 1 to 3 seconds
        data, nbFramesRead = f.readFromTo(1*f.samplerate, 3*f.samplerate, dtype=np.float64)
        print "nb frames read:",nbFramesRead

        #get the left channel
        lChannel = data[:,0]

        from scipy.signal import butter, lfilter
        cutoffL=200.
        # Low-pass filter on the left channel at 200 Hz
        b,a = butter(3, cutoffL/(f.samplerate/2), btype="low")
        lChannelFiltered = lfilter(b, a, lChannel)

        #write the 2 seconds read as an ogg file
        with SndFile("output.ogg", OPEN_MODES.SFM_WRITE,
                     writeFormat=FILE_FORMATS.SF_FORMAT_OGG^FILE_FORMATS.SF_FORMAT_VORBIS) as fo:
            fo.write(data)

        import matplotlib.pyplot as plt
        plt.plot(np.arange(len(data), dtype=np.float)*1000./f.samplerate, lChannel, label="left channel")
        plt.plot(np.arange(len(data), dtype=np.float)*1000./f.samplerate, lChannelFiltered, label="filtered left channel")
        plt.xlabel("time (ms)")
        plt.ylabel("amplitude (arbitrary unit)")
        plt.title("waveform of filtered and original left channel")
        plt.legend()
        plt.show()
