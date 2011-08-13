"""
A (currently) limited wrapper around the library libsndfile by Erik Castro de Lopo

http://www.mega-nerd.com/libsndfile/

licensed under the LGPL
(http://www.gnu.org/copyleft/lesser.html)

All sounds formats supported by libsndfile are available and a class interface
is implemented with some helper methods.

Requires numpy and ctypes. Tested under windows only.
"""

import os
import sys

try:
    import ctypes as ct
except ImportError:
    print "this module requires ctypes"
    sys.exit(-1)
try:
    import numpy as np
except ImportError:
    print "this module requires numpy"
    sys.exit(-1)

from ctypes.util import find_library

_lib = None

if os.name == "nt":
    shared_object_name = 'libsndfile-1'
else:
    shared_object_name = 'sndfile'



path = find_library(shared_object_name)
if path is None:
    print "library libsndfile not found"
    sys.exit(-1)

_lib = ct.CDLL(path)


_lib.sf_version_string.restype = ct.c_char_p
_lib.sf_version_string.argtypes = None
#print "libsndfile loaded version:", _lib.sf_version_string()



class FILE_FORMATS():
    SF_FORMAT_WAV           = 0x010000    # Microsoft WAV format (little endian default).
    SF_FORMAT_AIFF          = 0x020000    # Apple/SGI AIFF format (big endian).
    SF_FORMAT_AU            = 0x030000    # Sun/NeXT AU format (big endian).
    SF_FORMAT_RAW           = 0x040000    # RAW PCM data.
    SF_FORMAT_PAF           = 0x050000    # Ensoniq PARIS file format.
    SF_FORMAT_SVX           = 0x060000    # Amiga IFF / SVX8 / SV16 format.
    SF_FORMAT_NIST          = 0x070000    # Sphere NIST format.
    SF_FORMAT_VOC           = 0x080000    # VOC files.
    SF_FORMAT_IRCAM         = 0x0A0000    # Berkeley/IRCAM/CARL
    SF_FORMAT_W64           = 0x0B0000    # Sonic Foundry's 64 bit RIFF/WAV
    SF_FORMAT_MAT4          = 0x0C0000    # Matlab (tm) V4.2 / GNU Octave 2.0
    SF_FORMAT_MAT5          = 0x0D0000    # Matlab (tm) V5.0 / GNU Octave 2.1
    SF_FORMAT_PVF           = 0x0E0000    # Portable Voice Format
    SF_FORMAT_XI            = 0x0F0000    # Fasttracker 2 Extended Instrument
    SF_FORMAT_HTK           = 0x100000    # HMM Tool Kit format
    SF_FORMAT_SDS           = 0x110000    # Midi Sample Dump Standard
    SF_FORMAT_AVR           = 0x120000    # Audio Visual Research
    SF_FORMAT_WAVEX         = 0x130000    # MS WAVE with WAVEFORMATEX
    SF_FORMAT_SD2           = 0x160000    # Sound Designer 2
    SF_FORMAT_FLAC          = 0x170000    # FLAC lossless file format
    SF_FORMAT_CAF           = 0x180000    # Core Audio File format
    SF_FORMAT_WVE           = 0x190000    # Psion WVE format
    SF_FORMAT_OGG           = 0x200000    # Xiph OGG container
    SF_FORMAT_MPC2K         = 0x210000    # Akai MPC 2000 sampler
    SF_FORMAT_RF64          = 0x220000    # RF64 WAV file

    # Subtypes from here on.

    SF_FORMAT_PCM_S8        = 0x0001    # Signed 8 bit data
    SF_FORMAT_PCM_16        = 0x0002    # Signed 16 bit data
    SF_FORMAT_PCM_24        = 0x0003    # Signed 24 bit data
    SF_FORMAT_PCM_32        = 0x0004    # Signed 32 bit data

    SF_FORMAT_PCM_U8        = 0x0005    # Unsigned 8 bit data (WAV and RAW only)

    SF_FORMAT_FLOAT         = 0x0006    # 32 bit float data
    SF_FORMAT_DOUBLE        = 0x0007    # 64 bit float data

    SF_FORMAT_ULAW          = 0x0010    # U-Law encoded.
    SF_FORMAT_ALAW          = 0x0011    # A-Law encoded.
    SF_FORMAT_IMA_ADPCM     = 0x0012    # IMA ADPCM.
    SF_FORMAT_MS_ADPCM      = 0x0013    # Microsoft ADPCM.

    SF_FORMAT_GSM610        = 0x0020    # GSM 6.10 encoding.
    SF_FORMAT_VOX_ADPCM     = 0x0021    # OKI / Dialogix ADPCM

    SF_FORMAT_G721_32       = 0x0030    # 32kbs G721 ADPCM encoding.
    SF_FORMAT_G723_24       = 0x0031    # 24kbs G723 ADPCM encoding.
    SF_FORMAT_G723_40       = 0x0032    # 40kbs G723 ADPCM encoding.

    SF_FORMAT_DWVW_12       = 0x0040    # 12 bit Delta Width Variable Word encoding.
    SF_FORMAT_DWVW_16       = 0x0041    # 16 bit Delta Width Variable Word encoding.
    SF_FORMAT_DWVW_24       = 0x0042    # 24 bit Delta Width Variable Word encoding.
    SF_FORMAT_DWVW_N        = 0x0043    # N bit Delta Width Variable Word encoding.

    SF_FORMAT_DPCM_8        = 0x0050    # 8 bit differential PCM (XI only)
    SF_FORMAT_DPCM_16       = 0x0051    # 16 bit differential PCM (XI only)

    SF_FORMAT_VORBIS        = 0x0060    # Xiph Vorbis encoding.

    # Endian-ness options.

    SF_ENDIAN_FILE          = 0x00000000    # Default file endian-ness.
    SF_ENDIAN_LITTLE        = 0x10000000    # Force little endian-ness.
    SF_ENDIAN_BIG           = 0x20000000    # Force big endian-ness.
    SF_ENDIAN_CPU           = 0x30000000    # Force CPU endian-ness.

    SF_FORMAT_SUBMASK       = 0x0000FFFF
    SF_FORMAT_TYPEMASK      = 0x0FFF0000
    SF_FORMAT_ENDMASK       = 0x30000000


# String types that can be set and read from files. Not all file types
# support this and even the file types which support one, may not support
# all string types.
class FILE_STRINGS():
    SF_STR_TITLE        = 0x01
    SF_STR_COPYRIGHT    = 0x02
    SF_STR_SOFTWARE     = 0x03
    SF_STR_ARTIST       = 0x04
    SF_STR_COMMENT      = 0x05
    SF_STR_DATE         = 0x06
    SF_STR_ALBUM        = 0x07
    SF_STR_LICENSE      = 0x08

# Public error values. These are guaranteed to remain unchanged for the duration
# of the library major version number.
# There are also a large number of private error numbers which are internal to
# the library which can change at any time.
SF_ERR_NO_ERROR               = 0
SF_ERR_UNRECOGNISED_FORMAT    = 1
SF_ERR_SYSTEM                 = 2
SF_ERR_MALFORMED_FILE         = 3
SF_ERR_UNSUPPORTED_ENCODING   = 4


#other definitions :
sf_count_t = ct.c_longlong


#structs:
class SF_INFO(ct.Structure):
    _fields_ = [("frames", sf_count_t), #Used to be called samples.  Changed to avoid confusion.
                ("samplerate", ct.c_int),
                ("channels", ct.c_int),
                ("format", ct.c_int),
                ("sections", ct.c_int),
                ("seekable", ct.c_int)]

def __init_lib_methods():
    SNDFILE = ct.c_int

    #SNDFILE*     sf_open        (const char *path, int mode, SF_INFO *sfinfo) ;
    _lib.sf_open.restype = SNDFILE
    _lib.sf_open.argtypes = [ct.c_char_p, ct.c_int, ct.POINTER(SF_INFO)]

    #SNDFILE*  sf_open_fd (int fd, int mode, SF_INFO *sfinfo, int close_desc) ;
    _lib.sf_open_fd.restype = SNDFILE
    _lib.sf_open_fd.argtypes = [ct.c_int, ct.c_int, ct.POINTER(SF_INFO), ct.c_int]

    #int        sf_error        (SNDFILE *sndfile) ;
    _lib.sf_error.restype = ct.c_int
    _lib.sf_error.argtypes = [SNDFILE]

    #const char* sf_strerror (SNDFILE *sndfile) ;
    _lib.sf_strerror.restype = ct.c_char_p
    _lib.sf_strerror.argtypes = [SNDFILE]

    #int        sf_format_check    (const SF_INFO *info) ;
    _lib.sf_format_check.restype = ct.c_int
    _lib.sf_format_check.argtypes = [ct.POINTER(SF_INFO)]

    #sf_count_t    sf_seek         (SNDFILE *sndfile, sf_count_t frames, int whence) ;
    _lib.sf_seek.restype = sf_count_t
    _lib.sf_seek.argtypes = [SNDFILE, sf_count_t, ct.c_int]

    #const char* sf_get_string (SNDFILE *sndfile, int str_type) ;
    _lib.sf_get_string.restype = ct.c_char_p
    _lib.sf_get_string.argtypes = [SNDFILE, ct.c_int]

    #int         sf_set_string    (SNDFILE *sndfile, int str_type, const char* str) ;
    #TODO
    #_lib.sf_set_string.restype = ct.c_int
    #_lib.sf_set_string.argtypes = [SNDFILE, ct.c_int, ct.c_char_p]

    #sf_count_t    sf_read_raw        (SNDFILE *sndfile, void *ptr, sf_count_t bytes) ;
    _lib.sf_read_raw.restype = sf_count_t
    _lib.sf_read_raw.argtypes = [SNDFILE, ct.c_void_p, sf_count_t]

    # Functions for reading and writing the data chunk in terms of frames.
    # The number of items actually read/written = frames * number of channels.
    #     sf_xxxx_raw       read/writes the raw data bytes from/to the file
    #     sf_xxxx_short     passes data in the native short format
    #     sf_xxxx_int       passes data in the native int format
    #     sf_xxxx_float     passes data in the native float format
    #     sf_xxxx_double    passes data in the native double format
    # All of these read/write function return number of frames read/written.
    #sf_count_t    sf_readf_float    (SNDFILE *sndfile, float *ptr, sf_count_t frames) ;
    _lib.sf_read_float.restype = sf_count_t
    _lib.sf_read_float.argtypes = [SNDFILE, ct.POINTER(ct.c_float), sf_count_t]
    _lib.sf_read_double.restype = sf_count_t
    _lib.sf_read_double.argtypes = [SNDFILE, ct.POINTER(ct.c_double), sf_count_t]
    _lib.sf_read_short.restype = sf_count_t
    _lib.sf_read_short.argtypes = [SNDFILE, ct.POINTER(ct.c_short), sf_count_t]
    _lib.sf_read_int.restype = sf_count_t
    _lib.sf_read_int.argtypes = [SNDFILE, ct.POINTER(ct.c_int), sf_count_t]

    #sf_count_t    sf_write_raw     (SNDFILE *sndfile, const void *ptr, sf_count_t bytes) ;
    _lib.sf_write_raw.restype = sf_count_t
    _lib.sf_write_raw.argtypes = [SNDFILE, ct.c_void_p, sf_count_t]

    #int        sf_close        (SNDFILE *sndfile) ;
    _lib.sf_close.restype = ct.c_int
    _lib.sf_close.argtypes = [SNDFILE]

    #writing functions
    #sf_count_t  sf_write_short   (SNDFILE *sndfile, short *ptr, sf_count_t items) ;
    #sf_count_t  sf_write_int     (SNDFILE *sndfile, int *ptr, sf_count_t items) ;
    #sf_count_t  sf_write_float   (SNDFILE *sndfile, float *ptr, sf_count_t items) ;
    #sf_count_t  sf_write_double  (SNDFILE *sndfile, double *ptr, sf_count_t items) ;
    _lib.sf_write_int.restype = sf_count_t
    _lib.sf_write_int.argtypes = [SNDFILE, ct.POINTER(ct.c_int), sf_count_t]
    _lib.sf_write_short.restype = sf_count_t
    _lib.sf_write_short.argtypes = [SNDFILE, ct.POINTER(ct.c_short), sf_count_t]
    _lib.sf_write_float.restype = sf_count_t
    _lib.sf_write_float.argtypes = [SNDFILE, ct.POINTER(ct.c_float), sf_count_t]
    _lib.sf_write_double.restype = sf_count_t
    _lib.sf_write_double.argtypes = [SNDFILE, ct.POINTER(ct.c_double), sf_count_t]

__init_lib_methods()


#class definitions :
class OPEN_MODES():
    SFM_READ  = 0x10
    SFM_WRITE = 0x20
    SFM_RDWR  = 0x30

class SEEK_MODES():
    #stdio.h :
    SEEK_SET = 0
    SEEK_CUR = 1
    SEEK_END = 2

data_types_match = {
    np.float64: "double",
    np.float32: "float",
    np.int32: "int",
    np.int16: "short",
}

class SndFile(object):
    """ Main Class of the wrapper, provides easy access to audio file contents """

    def __init__(self, file_, open_mode=OPEN_MODES.SFM_READ,
                 writeSamplerate = 48000,
                 writeFormat = FILE_FORMATS.SF_FORMAT_WAV^FILE_FORMATS.SF_FORMAT_PCM_16,
                 writeNbChannels = 2):
        """ initializes a SndFile object from the file 'file_'. If file_ could be
        a python file instance or a filename. If file_ is the filename you should
        pass the open mode specified in OPEN_MODES. If file_ is a file instance
        you should call to snd_file_instance.close() prior to close the file with
        file_.close()"""
        self._lib = _lib

        self._sf_info = SF_INFO()
        if open_mode == OPEN_MODES.SFM_WRITE:
            self._sf_info.samplerate = writeSamplerate
            self._sf_info.format = writeFormat
            self._sf_info.channels = writeNbChannels
        self.currentPosition = 0

        if isinstance(file_, file):
          self._filename = file_.name
          self._SNDFILE = self._lib.sf_open_fd(file_.fileno(), open_mode,
                                               self._sf_info, 0)
        else:
          self._filename = file_
          self._SNDFILE = self._lib.sf_open(self._filename, open_mode, self._sf_info)

        if self._lib.sf_error(self._SNDFILE) != 0:
            raise Exception(self._lib.sf_strerror(self._SNDFILE))

    @property
    def nbFrames(self):
        """ the total number of frames for each channels """
        return self._sf_info.frames
    @property
    def samplerate(self):
        """ the samplerate in Hz"""
        return self._sf_info.samplerate
    @property
    def format(self):
        """ the audio file format as defined in FILE_FORMATS """
        return self._sf_info.format
    @property
    def isSeekable(self):
        """ True if seekable, False otherwise """
        return self._sf_info.seekable
    @property
    def channels(self):
        """ the number of channels """
        return self._sf_info.channels

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type!=None:
            print "an exception occured while in the with statement"
            print value

        self.close()

    def __str__(self):
        s = """
        audio file  : %s
        frames:     : %d
        samplerate  : %d
        channels    : %d
        format      : %d
        seekable    : %d
        """%(self._filename, self.nbFrames, self.samplerate,
             self.channels, self.format, self.isSeekable)
        return s

    def close(self):
        if self._SNDFILE != None:
            if self._lib.sf_close(self._SNDFILE) != 0:
                raise Exception("Can't close file")
            self._SNDFILE = None

    def write(self, data):
        """ write all the provided data to the file with the parameters
        specified when opening the file """
        type_ = data_types_match[data.dtype.type]
        ctypes_dtype = getattr(ct, "c_" + type_)
        ctypes_data =  data.ctypes.data_as(ct.POINTER(ctypes_dtype))
        write_func = getattr(self._lib, "sf_write_" + type_)

        return data, write_func(self._SNDFILE, ctypes_data, data.size)


    def read(self, nbFrames=None, dtype=np.float32):
        """ returns a numpy array of dimension (nbFrames, nbChannels) and of type dtype
        reads nbFrames for each channels if provided, else reads the entire file
        the data is read from the current position in the file, this can be set
        using the seek method.
        Reading beyond the limits of the file fills the output array with 0s.
        Accepted dtypes are numpy's int16, int32, float32, float64."""
        if not nbFrames: nbFrames=self.nbFrames
        try:
            data, nbFramesRead = self._read(nbFrames, dtype)
        except TypeError, te:
            raise te
        return data, nbFramesRead

    def seek(self, frame_position, whence=SEEK_MODES.SEEK_SET):
        """ seek to a position in the audio file, seek modes are those
        specified in SEEK_MODES.
        Raises an exception if tried to seek beyond the borders of the file.
        Else returns the current offset."""
        offset = self._lib.sf_seek(self._SNDFILE, frame_position, whence)
        if offset==-1:
            raise Exception(self._lib.sf_strerror(self._SNDFILE))
        return offset

    def _read(self, nbFrames, dtype):
        """ class internal common part of read and readFromTo """
        dtype = np.dtype(dtype).type
        data = np.empty((nbFrames, self.channels), dtype)

        type_ = data_types_match[dtype]
        ctypes_dtype = getattr(ct, "c_" + type_)
        ctypes_data =  data.ctypes.data_as(ct.POINTER(ctypes_dtype))
        read_func = getattr(self._lib, "sf_read_" + type_)

        return data, read_func(self._SNDFILE, ctypes_data, nbFrames*self.channels)/self.channels

    def readFromTo(self, startFrame, stopFrame, dtype=np.float32):
        """ helper read method to specify the start and ending frame of reading.
        Raises an exception if startFrame<0 or stopFrame<startFrame.
        Accepted dtypes are numpy's int16, int32, float32, float64.
        returns a numpy array of dimension (stopFrame-startFrame, nbChannels)
        and the number of frames actually read.
        Reading beyond the limits of the file fills the output array with 0s."""
        if stopFrame<=startFrame and startFrame>=0:
            raise Exception("Please choose stopFrame > startFrame >= 0")
        nbFrames = stopFrame-startFrame
        self.seek(startFrame)
        try:
            data, nbFramesRead = self._read(nbFrames, dtype)
        except TypeError, te:
            raise te
        return data, nbFramesRead

    def get_string(self, what_string):
        """ returns the queried string value if the file format supports it.
        the available string queries are specified in FILE_STRINGS """
        return self._lib.sf_get_string(self._SNDFILE, what_string)

    def set_string(self, what_string, value):
        """ sets the string of the audio file as specified in FILE_STRINGS """
        return self._lib.sf_set_string(self._SNDFILE, what_string, value)

if __name__=="__main__":
    with SndFile("test/LS100673.WAV") as f:
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
