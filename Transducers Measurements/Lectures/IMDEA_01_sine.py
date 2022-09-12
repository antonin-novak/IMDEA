import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# sample rate [Hz]
fs = 48000

print(sd.query_devices())
sd.default.device = (3, 3)
print(sd.query_devices())

# sin-wave definition
f0 = 553  # [Hz]
T = 2  # duration of sine wave [s]

t = np.arange(0, T*fs) / fs
x = np.sin(2*np.pi * f0 * t)

y = sd.playrec(x,  # input signal
               samplerate=fs,
               channels=1,
               blocking=True)

# extract the 1st channel
y = y[int(-fs):, 0]  # taking just the last 1 second (fs samples)
print(y.shape)

Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

fig, ax = plt.subplots()
ax.plot(y)

fig, ax = plt.subplots()
ax.plot(f_axis, 20*np.log10(np.abs(Y)))

plt.show()
