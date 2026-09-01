import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


# # set the device numbers (input, output)
sd.default.device = ('Fireface', 'Fireface')

# show list of devices
print(sd.query_devices())


# design a sine wave
fs = 48000 # sample rate
f = 500.2 # frequency
T = 3 # duration in seconds
t = np.arange(0, T, 1/fs) # time vector
x = np.sin(2 * np.pi * f * t)


# play and record simultaneously
y = sd.playrec(x, # x is the signal to play
    samplerate=fs,
    channels=2,
    input_mapping=(1, 2), # input channels 7 and 8
    blocking=True # wait until playback is finished
)

y1 = y[:, 0] # 1st channel (microphone)

# np.save('recorded_signal_2.npy', y1) # save the recorded signal

# with open('recorded_signal_2.npy', 'rb') as f:
#     y1 = np.load(f)

y1 = y1[fs:]

fig, ax = plt.subplots()
ax.plot(y1)
ax.set_xlabel('Samples [-]')
ax.set_ylabel('Amplitude')
ax.set_title('Output signal')
ax.grid()


# spectrum of the recorded signal
Y1 = np.fft.rfft(y1)/len(y1)*2 # normalize the amplitude

fig, ax = plt.subplots()
freq_ax = np.fft.rfftfreq(len(y1), 1/fs)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB SPL]')

ax.plot(freq_ax, 20*np.log10(np.abs(Y1/2e-5/np.sqrt(2))))


plt.show()