# import the module
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# show list of devices
print(sd.query_devices())
# set the device numbers (input, output)
sd.default.device = (6, 6)

# sample rate
fs = 48000

# generate a sine wave
f0 = 500  # frequency of the sine wave
T = 4  # duration in seconds
t = np.arange(0, T, 1/fs)  # time vector

frequencies = np.unique(
    np.round(np.logspace(np.log10(20), np.log10(20000), 500)))
print(frequencies)

x = np.zeros_like(t)
for f0 in frequencies:
    random_phase = np.random.rand()*2*np.pi
    x += np.sin(2*np.pi*f0*t + random_phase)

# normalize the signal
x /= np.max(np.abs(x))


# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=48000,
               channels=2,
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take 1st channel only
# and get rid of the 1st second (latency + transien)
x = x[fs:]
y = y[fs:, 0]


# plot output
fig, ax = plt.subplots()
ax.plot(t[fs:], y)


# Spectrum of the signals
X = np.fft.rfft(x)
Y = np.fft.rfft(y)
f_axis = np.fft.rfftfreq(len(y), 1/fs)

f_index = frequencies * len(y) / fs
X_multitone = X[f_index.astype(int)]
Y_multitone = Y[f_index.astype(int)]


# plot the Spectrum
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, 20*np.log10(np.abs(X)))
# ax.set(xlim=(20, 20e3))
# ax.set_title(f'Spectrum of the excitation multitone signal')
# ax.set_xlabel('Frequency (Hz)')
# ax.set_ylabel('Magnitude (dB)')


# plot the Spectrum
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))
ax.semilogx(frequencies, 20*np.log10(np.abs(Y_multitone)), 'o')
ax.set(xlim=(20, 20e3))
ax.set_title(f'Spectrum of the signal')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')


# plot the FRF
FRF = Y_multitone / X_multitone
fig, ax = plt.subplots()
ax.semilogx(frequencies, 20*np.log10(np.abs(FRF)))
ax.set(xlim=(20, 20e3))
ax.set_title(f'FRF')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')


plt.show()
