import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

''' sample rate '''
fs = 48000  # [Hz]

''' Devices (Sounddevice) '''
print(sd.query_devices())
sd.default.device = (3, 3)
print(sd.query_devices())

''' Multitone definition '''
T = 2  # duration of multitone [s]
t = np.arange(0, T*fs) / fs

frequencies = np.unique(
    np.round(np.logspace(np.log10(20), np.log10(20e3), 500)))
x = 0
for f0 in frequencies:
    x += np.sin(2*np.pi * f0 * t + 2*np.pi*np.random.rand())

x /= np.max(np.abs(x))  # signal normalization

''' Playing and Recording '''
y = sd.playrec(x,  # input signal
               samplerate=fs,
               channels=1,
               blocking=True)

# extract the 1st channel
x = x[int(-fs):]  # taking just the last 1 second (fs samples)
y = y[int(-fs):, 0]  # taking just the last 1 second (fs samples)
print(y.shape)

''' calculate the CREST FACTOR '''
crest_factor = np.max(np.abs(y)) / np.std(y)
print(crest_factor)

''' Fourier Transform '''
X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

''' Select the Multitone frequencies only '''
X_multitone = X[frequencies.astype('int')]
Y_multitone = Y[frequencies.astype('int')]

''' Frequency Response Function'''
FRF = Y_multitone/X_multitone

''' Plot '''
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title='output signal', xlabel='samples [-]')

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))
ax.semilogx(frequencies, 20*np.log10(np.abs(Y_multitone)))
ax.set(title='Output Power Spectrum',
       xlabel='Frequency [Hz]', ylabel='Magnitude [dB]')

fig, ax = plt.subplots()
ax.semilogx(frequencies, 20*np.log10(np.abs(FRF)))
ax.set(title='Frequency Response Function',
       xlabel='Frequency [Hz]', ylabel='Magnitude [dB]')


plt.show()
