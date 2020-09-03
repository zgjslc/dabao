import numpy as np
from scipy.fftpack import fft
import matplotlib.pyplot as plt
Fs = int(10e3)
f1 = 390
f2 = 2e3

t = np.linspace(0, 1, int(Fs))
noise1 = np.random.random(len(t))
noise2 = np.random.normal(1, 10, int(Fs))

y = 8 * np.sin(2 * np.pi * f1 * t) + 5 * np.sin(2 * np.pi * f2 * t)


def FFT(Fs, data):
    L = len(data)
    N = np.power(2, np.ceil(np.log2(L)))
    N = int(N)
    FFT_y1 = np.abs(fft(data, N))/L*2#振幅大小

    fre = np.arange(int(N/2))*Fs/N*2
    FFT_y1 = FFT_y1[range(int(N/2))]
    return fre, FFT_y1

fre , FFT_y1 = FFT(Fs,y)
plt.figure()
plt.plot(fre)
print(np.argmax(FFT_y1,axis=0))
print(FFT_y1[639])
print(fre[639])
plt.grid()
plt.show()

