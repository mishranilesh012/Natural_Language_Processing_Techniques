import struct

import scipy.io.wavfile as wf
import numpy
import pydub



# for i in range(wave_file.getnframes()):
#     # read a single frame and advance to next frame
#     current_frame = wave_file.readframes(1)
#
#     # check for silence
#     silent = True
#     # wave frame samples are stored in little endian**
#     # this example works for a single channel 16-bit per sample encoding
#     unpacked_signed_value = struct.unpack("<h", current_frame) # *
#     if abs(unpacked_signed_value[0]) > 500:
#         silent = False
#
#     if silent:
#         print("Frame %s is silent." % wave_file.tell())
#     else:
#         print("Frame %s is not silent." % wave_file.tell())

# rate, data = wf.read('testing.wav')
# # data0 is the data from channel 0.
# data0 = data[:, 0]
#
# print(data0)


# from pydub import AudioSegment
# from pydub.silence import detect_silence, detect_nonsilent
#
# song = AudioSegment.from_wav("soundaudio.wav")
# val = detect_silence(song)
# print(val)


from pyAudioAnalysis import audioSegmentation as aS
[flagsInd, classesAll, acc, CM] = aS.mtFileClassification("data/scottish.wav", "data/svmSM", "svm", True, 'data/scottish.segments')