# import the module
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# show list of devices
print(sd.query_devices())
# set the device numbers (input, output)
sd.default.device = (5, 5)

# sample rate
fs = 48000

# generate a sine wave
f0 = 500  # frequency of the sine wave
T = 4  # duration in seconds
t = np.arange(0, T, 1/fs)  # time vector
x = np.sin(2*np.pi*f0*t)


# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=48000,
               channels=2,
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take 1st channel only
# and get rid of the 1st second (latency + transien)
y = y[fs:, 0]


# plot output
fig, ax = plt.subplots()
ax.plot(t[fs:], y)


# Spectrum of the signal
Y = np.fft.rfft(y)
f_axis = np.fft.rfftfreq(len(y), 1/fs)


# Calculate THD
N_harmonics = 15
f_harmonics = np.arange(1, N_harmonics+1) * f0
f_index_harmonics = f_harmonics * len(y) / fs
THD = np.sqrt(np.sum(np.abs(Y[f_index_harmonics[1:].astype(
    int)])**2)) / np.abs(Y[f_index_harmonics[0].astype(int)]) * 100


# plot the Spectrum
fig, ax = plt.subplots()
ax.plot(f_axis, 20*np.log10(np.abs(Y)))
ax.plot(f_axis[f_index_harmonics.astype(int)], 20 *
        np.log10(np.abs(Y[f_index_harmonics.astype(int)])), 'o')
ax.set_title(f'Spectrum of the signal, THD = {THD:.2f} %')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')

plt.show()
