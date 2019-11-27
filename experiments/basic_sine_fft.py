import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from matplotlib.widgets import Cursor
from scipy.io.wavfile import write

# Number of samplepoints
N = 6000

# sample spacing = ADC sampling period
T = 1.0 / 1000.0
x = np.linspace(0.0, N*T, N)

# y = 1.5sin(50*2pix) + 0.5sin(80*2pi)
y = 1.5*np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x) + 0.3*np.sin( 100 * 2.0*np.pi*x)

# get the FFT ( fast furier transform )
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

# scale the wave and save in a .wav
# int is -32768 to 32767
scaled = np.int16(y/np.max(np.abs(y)) * 32767)
write('test.wav', N, scaled)

plt.subplot(2, 1, 1)
plt.plot(xf, 2.0/N * np.abs(yf[:N//2]))
plt.title('Frequency')
plt.ylabel('Amplitud DB')

plt.subplot(2, 1, 2)
plt.plot(x, y)
plt.xlabel('time (s)')
plt.ylabel('Amplitud')

plt.show()
