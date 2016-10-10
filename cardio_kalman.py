import numpy as np
from scipy import signal
from scipy.signal import buttord, butter, lfilter, filtfilt, argrelextrema,argrelmax,argrelmin,find_peaks_cwt, freqz
from math import pi
from matplotlib import pyplot as plt

def cardio_kalman(wave_input):
    globals()
    wave = wave_input
    original = wave_input
    order = 1
    fs = 170
    lowcut = 1
    highcut = 30
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band', analog=0)
    wave_a = np.asarray(wave)
    peaks_origin = argrelmax(wave_a)
    peak_data = []
    pk, vl = [], []
    for i in range(len(wave)):
        if (i in peaks_origin[0]):
            peak_data.append(wave[i])
            pk.append(wave[i])
            med = np.median(pk)
            avg = np.mean(pk)
            outliers = [i for i in pk if i > (1.4*med)]
            if ((max(med,avg)/min(med,avg))<=(0.2*max(med,avg))):
                lowcut = 5
                highcut = 20
                nyq = 0.5 * fs
                low = lowcut / nyq
                high = highcut / nyq
                b, a = butter(order, [low, high], btype='band', analog=0)
                y = lfilter(b, a, wave)
                wave = y.copy()
                break
            elif((max(pk) > 1.4*med) and (len(outliers) >= (0.3*len(pk)))):
                lowcut = 10
                #lowcut = lowcut*10
                #highcut = highcut*0.75
                low = lowcut / nyq
                high = highcut / nyq
                b, a = butter(order, [low, high], btype='band', analog=0)
                y = lfilter(b, a, wave)
                wave = y.copy()
            else:
                break
    return wave

def signal_detrend(wave_input):
    globals()
    wave = wave_input
    typedetrend = 'constant'
    detrended = signal.detrend(wave, type=typedetrend)
    return detrended

if __name__ == '__main__':
    filename = raw_input('->')
    filename = filename + '.txt'
    fp = open(filename, 'r')
    wave = []
    rawdata = fp.read().splitlines()
    for each in rawdata:
        #each = each[1:-1]
        #each_1 = each.split(',')
        wave.append(int(each))
        #data1.append(int(each_1[1]))
        #data2.append(int(each_1[2]))
    filtered = signal_detrend(wave)
    filtered = cardio_kalman(filtered)

    plt.figure(1)
    plt.subplot(211)
    plt.plot(wave, '-')
    
    plt.subplot(212)
    plt.plot(filtered, 'g-')
    plt.show()