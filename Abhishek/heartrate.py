import math

from scipy import signal


# Calculate heart rate from FFT peaks
def find_heart_rate(fft, freqs, freq_min, freq_max):
    fft_maximums = []
    peek_frequency=[]

    # print(fft)
    # print(freqs)

    for i in range(fft.shape[0]):
        if freq_min <= freqs[i] <= freq_max:
            fftMap = abs(fft[i])
            # print(fftMap.max())
            fft_maximums.append(fftMap.max())
        else:
            fft_maximums.append(0)
    print("lenght of fft maximum", len(fft_maximums))
    print("fft_maximums",fft_maximums)
    peaks, properties = signal.find_peaks(fft_maximums)
    max_peak = -1
    max_freq = 0
    print("peak",peaks)
    # Find frequency with max amplitude in peaks
    for peak in peaks:
        print("peaks[i]",peak)
        if fft_maximums[peak] > max_freq:
            max_freq = fft_maximums[peak]
            max_peak = peak

        peek_frequency.append(freqs[peak] * 60)
    print(peek_frequency)
    #============================================RMS
    value = 0
    for n in peek_frequency:
        value += (n * n)
    rms = math.sqrt((value / len(peek_frequency)))
    print("RMS = "+str(rms))
    #=============================================RMS

    # ============================================AVG
    fcount=len(peek_frequency)
    data=0
    for f in peek_frequency:
        data=data+f
    avg=data//fcount
    print("AVG = "+str(avg))
    # ============================================AVG

    return freqs[max_peak] * 60
