# import the modules
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# set the device numbers (input, output)
sd.default.device = (6, 6)

# show list of devices
print(sd.query_devices())

# sample rate
fs = 48000

# sine wave
f0 = 400.5
T = 3
t = np.arange(0, T, 1/fs)
x = np.sin(2 * np.pi * f0 * t)

# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=fs,
               channels=1,
               output_mapping=(1),
               input_mapping=(1),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# select the input channel and trim the output signal to 2s
y = y[int(-2*fs):, 0]


# plot the output signal
fig, ax = plt.subplots()
ax.plot(y)

# FFT
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

# plot the spectrum
fig, ax = plt.subplots()
ax.plot(f_axis, 20*np.log10(np.abs(Y)))
ax.set(xlabel='Freqeuncy [Hz]', ylabel='Power Spectra [dB]')

plt.show()
