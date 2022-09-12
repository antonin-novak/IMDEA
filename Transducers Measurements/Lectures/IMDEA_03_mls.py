import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# sample rate [Hz]
fs = 48000

print(sd.query_devices())
sd.default.device = (3, 3)
print(sd.query_devices())

# MLS definition
M = 15  # order of MLS
N = 2**M-1  # length of the MLS signal

shift_register = np.ones(M)
mls_signal = np.zeros(N)

for n in range(N):
    mls_signal[n] = shift_register[-1]
    temp = np.logical_xor(shift_register[14], shift_register[7])
    shift_register = np.roll(shift_register, 1)
    shift_register[0] = temp

x = 2*mls_signal - 1

X = np.fft.rfft(x)

fig, ax = plt.subplots()
ax.plot(np.abs(X))

# fig, ax = plt.subplots()
# ax.plot(mls_signal)

y = sd.playrec(np.tile(x, 2),  # input signal
               samplerate=fs,
               channels=1,
               blocking=True)


# extract the 1st channel
y = y[-N:, 0]  # taking just the last 1 second (fs samples)
print(y.shape)

# calculate the CREST FACTOR
crest_factor = np.max(np.abs(x)) / np.std(x)
print(crest_factor)

X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

# frequency response function
FRF = Y/X

# impulse response
IR = np.fft.irfft(FRF)

fig, ax = plt.subplots()
ax.plot(IR)
ax.set(title='Impulse Response')

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))


plt.show()
