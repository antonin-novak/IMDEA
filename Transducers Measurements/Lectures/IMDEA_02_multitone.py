# import the module
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# set the device numbers (input, output)
sd.default.device = (5, 5)

# show list of devices
print(sd.query_devices())

# sine signal
fs = 48000  # sample rate
T = 2       # time duration of the sine signal [s]

# frequencies for the multitone signal [Hz]
frequencies = np.unique(
    np.round(np.logspace(np.log10(20), np.log10(20e3), 500)))
print(f'frequencies = {frequencies}')

# time axis
t = np.arange(0, T, 1/fs)

# multitone signal generation
x = 0
for f0 in frequencies:
    random_phase = 2*np.pi*np.random.rand()
    x += np.sin(2*np.pi*f0*t + random_phase)

# signal normalization
x /= np.max(np.abs(x))

# fft of the multitone signal
X_all = np.fft.rfft(x[-fs:])/fs*2

fig, ax = plt.subplots()
ax.plot(x)
ax.set(title='Multitone signal')
ax.set(xlabel='Samples [-]')

fig, ax = plt.subplots()
ax.semilogx(20*np.log10(np.abs(X_all)))
ax.set(title='Spectra of the multitone signal')
ax.set(xlabel='Frequency [Hz]', ylabel='Power Spectra [dB]')

crest_factor = np.max(np.abs(x)) / np.std(x)
print(f'crest factor = {crest_factor}')

# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=48000,
               channels=2,
               output_mapping=(1),
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take just the 1st channel, and last second
y1 = y[-fs:, 0]

# fft
Y1_all = np.fft.rfft(y1)/len(y1)*2
f_axis = np.fft.rfftfreq(len(y1), 1/fs)

# select only the frequencies we used for the multitone
Y1 = Y1_all[frequencies.astype('int')]
X = X_all[frequencies.astype('int')]

# plot the spectra
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y1_all)))
ax.semilogx(frequencies, 20*np.log10(np.abs(Y1)))
ax.set(title='Spectra of the output signal')
ax.set(xlabel='Frequency [Hz]', ylabel='Power Spectra [dB]')

fig, ax = plt.subplots()
ax.semilogx(frequencies, 20*np.log10(np.abs(Y1/X)))
ax.set(title='Frequency Response Function')
ax.set(xlabel='Frequency [Hz]', ylabel='FRF [dB]')

# # plot the signal
# fig, ax = plt.subplots()
# ax.plot(y1)


plt.show()
