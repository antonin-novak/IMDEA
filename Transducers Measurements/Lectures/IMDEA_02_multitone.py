# import the modules
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# set the device numbers (input, output)
sd.default.device = (6, 6)

# show list of devices
# print(sd.query_devices())

# sample rate
fs = 48000

# multitone signal
frequencies = np.unique(
    np.round(np.logspace(np.log10(20), np.log10(20e3), 500)))
T = 2
t = np.arange(0, T, 1/fs)
x = 0
for f in frequencies:
    x += np.sin(2 * np.pi * f * t + np.random.uniform(0, 2*np.pi))
#    x += np.sin(2 * np.pi * f * t  +  2 * np.pi * np.random.rand())

# normalize the signal
x /= np.max(np.abs(x))


# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=fs,
               channels=1,
               output_mapping=(1),
               input_mapping=(1),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# select the input channel and trim the output signal to 2s
x = x[int(-1*fs):]
y = y[int(-1*fs):, 0]


# plot the output signal
fig, ax = plt.subplots()
ax.plot(y)

# FFT
X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

# select the indexes of the frequencies of multitone signal
X_multitone = X[frequencies.astype(int)]
Y_multitone = Y[frequencies.astype(int)]

# FRF
FRF = Y_multitone / X_multitone

# plot the spectrum
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))
ax.semilogx(frequencies, 20*np.log10(np.abs(Y_multitone)))
ax.set(xlabel='Freqeuncy [Hz]', ylabel='Power Spectra [dB]')

# plot the FRF
fig, ax = plt.subplots()
ax.semilogx(frequencies, 20*np.log10(np.abs(FRF)))
ax.set(xlabel='Freqeuncy [Hz]', ylabel='FRF [dB]')


plt.show()
