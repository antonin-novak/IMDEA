import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

''' sample rate '''
fs = 48000  # [Hz]

''' Devices (Sounddevice) '''
print(sd.query_devices())
sd.default.device = (3, 3)
print(sd.query_devices())

''' MLS definition '''
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

''' Fourier Transform '''
X = np.fft.rfft(x)

''' Playing and Recording '''
y = sd.playrec(np.tile(x, 2),  # input signal (repeted twice)
               samplerate=fs,
               channels=1,
               blocking=True)

# extract the 1st channel
y = y[-N:, 0]  # taking just the last 1 second (fs samples)
print(y.shape)

''' calculate the CREST FACTOR '''
crest_factor = np.max(np.abs(x)) / np.std(x)
print(crest_factor)

''' Fourier Transform '''
X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

''' Frequency Response Function '''
FRF = Y/X

''' Impulse Response '''
IR = np.fft.irfft(FRF)

''' Plot '''
fig, ax = plt.subplots()
ax.plot(IR)
ax.set(title='Impulse Response', xlabel='samples [-]')

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))
ax.set(title='Output Power Spectrum',
       xlabel='Frequency [Hz]', ylabel='Magnitude [dB]')

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
ax.set(title='Frequency Response Function',
       xlabel='Frequency [Hz]', ylabel='Magnitude [dB]')

plt.show()
