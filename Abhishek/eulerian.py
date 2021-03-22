import numpy as np
import scipy.fftpack as fftpack
# import sys
# import numpy
# numpy.set_printoptions(threshold=sys.maxsize)

# Temporal bandpass filter with Fast-Fourier Transform
def fft_filter(video, freq_min, freq_max, fps):
    print("video",video)
    print("video.shape",video.shape)
    fft = fftpack.fft(video, axis=0)
    print("fft.shape",fft.shape)
    print("fft",fft)
    frequencies = fftpack.fftfreq(video.shape[0], d=1.0 / fps)
    print("frequencies",frequencies)
    bound_low = (np.abs(frequencies - freq_min)).argmin()
    print("bound_low",bound_low)
    bound_high = (np.abs(frequencies - freq_max)).argmin()

    print("bound_high", bound_high)
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0
    print("fft2", fft)
    iff = fftpack.ifft(fft, axis=0)

    print("iff",iff)
    # file1 = open("iffabs.txt", "w")
    # # \n is placed to indicate EOL (End of Line)
    #
    #
    # print("-----------------------------------------------")
    result = np.abs(iff)
    # file1.writelines(str(data))
    # file1.close()  # to change file access modes
    # print(result[0][1][0][0])
    result *= 500  # Amplification factor

    return result, fft, frequencies