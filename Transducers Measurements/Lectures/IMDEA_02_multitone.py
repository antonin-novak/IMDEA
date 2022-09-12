import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# sample rate [Hz]
fs = 48000

print(sd.query_devices())
sd.default.device = (3, 3)
print(sd.query_devices())

# multitone definition
T = 2  # duration of sine wave [s]
t = np.arange(0, T*fs) / fs

frequencies = np.unique(
    np.round(np.logspace(np.log10(20), np.log10(20e3), 500)))
# print(frequencies)

x = 0
for f0 in frequencies:
    x += np.sin(2*np.pi * f0 * t + 2*np.pi*np.random.rand())

# signal normalization
x /= np.max(np.abs(x))

y = sd.playrec(x,  # input signal
               samplerate=fs,
               channels=1,
               blocking=True)


# extract the 1st channel
x = x[int(-fs):]  # taking just the last 1 second (fs samples)
y = y[int(-fs):, 0]  # taking just the last 1 second (fs samples)
print(y.shape)

# calculate the CREST FACTOR
crest_factor = np.max(np.abs(y)) / np.std(y)
print(crest_factor)

X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

X_multitone = X[frequencies.astype('int')]
Y_multitone = Y[frequencies.astype('int')]

FRF = Y_multitone/X_multitone

fig, ax = plt.subplots()
ax.plot(y)

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))
ax.semilogx(frequencies, 20*np.log10(np.abs(Y_multitone)))

fig, ax = plt.subplots()
ax.semilogx(frequencies, 20*np.log10(np.abs(FRF)))


plt.show()
