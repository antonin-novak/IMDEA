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

# MLS signal- Maximum Length Sequence
N = 17
shift_register = np.ones(N)

M = 2**N - 1  # length of the sequence
x = np.zeros(M)

# generate the MLS sequence
for n in range(M):
    x[n] = shift_register[-1]
    temp = np.logical_xor(shift_register[2], shift_register[N-1])
    shift_register = np.roll(shift_register, 1)
    shift_register[0] = temp

x = 2*x - 1  # convert to +/-1

# MEASUREMENT
# play and record simultaneously
# use concatenate((x,x)) to repeat the signal twice
# this way we can then get rid of the first period that covers latency and transients
y = sd.playrec(np.concatenate((x, x)),  # x is the signal to play
               samplerate=48000,
               channels=2,
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take the 1st channel and get rid of the first period
y = y[M:, 0]

# plot the recorded signal
fig, ax = plt.subplots()
ax.plot(y)

# compute the FFT
X = np.fft.rfft(x)
Y = np.fft.rfft(y)
f_axis = np.fft.rfftfreq(len(y), 1/fs)

# plot the Spectrum
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y)))

# FRF
FRF = Y / X
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
ax.set(xlim=(20, 20e3))
ax.set_title(f'FRF')
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Magnitude (dB)')

# Impulse response
h = np.fft.irfft(FRF)

# plot the impulse response
fig, ax = plt.subplots()
ax.plot(h)

plt.show()
