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
f0 = 500    # frequency of the sine signal [Hz]

t = np.arange(0, T, 1/fs)
x = np.sin(2*np.pi*f0*t)

# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=48000,
               channels=2,
               output_mapping=(1),
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take just the 1st channel and the last second
y1 = y[-fs:, 0]

# fft
Y1 = np.fft.rfft(y1)/len(y1)*2
f_axis = np.fft.rfftfreq(len(y1), 1/fs)

fig, ax = plt.subplots()
ax.plot(f_axis, 20*np.log10(np.abs(Y1)))
ax.set(title='Spectra of the output signal')
ax.set(xlabel='Frequency [Hz]', ylabel='Power Spectra [dB]')

# plot the signal
fig, ax = plt.subplots()
ax.plot(y1)
ax.set(title='Output signal')
ax.set(xlabel='Samples [-]')

plt.show()
