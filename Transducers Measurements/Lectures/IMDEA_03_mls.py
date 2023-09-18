# import the module
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import max_len_seq

# set the device numbers (input, output)
sd.default.device = (5, 5)

# show list of devices
print(sd.query_devices())

# sample rate
fs = 48000

M = 17   # length of the shift register
N = 2**M-1

''' Coding a loop to generate the MLS signal '''
# shift_register = np.ones(M, dtype=bool)
# mls_sequence = np.zeros(N)

# for n in range(N):
#     mls_sequence[n] = shift_register[-1]
#     temp = shift_register[2] ^ shift_register[-1]
#     shift_register = np.roll(shift_register, 1)
#     shift_register[0] = temp

''' Using the max_len_seq to generate the MLS signal '''
mls_sequence = max_len_seq(M)[0]

# MLS is between 0 and 1. Let's put it between -1 and 1.
x = 2*mls_sequence - 1

fig, ax = plt.subplots()
ax.plot(x)

# Power spectra
X = np.fft.rfft(x)/N*2

# np.concatenate((1.0*x,1.0*x))
# play and record simultaneously
y = sd.playrec(np.tile(1.0*x, 2),  # x is the signal to play
               samplerate=48000,
               channels=2,
               output_mapping=(1),
               input_mapping=(1, 2),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

# take just the 1st channel and N last samples (1 period of MLS)
y1 = y[-N:, 0]

# Power spectra
Y1 = np.fft.rfft(y1)/len(y1)*2
f_axis = np.fft.rfftfreq(len(y1), 1/fs)

fig, ax = plt.subplots()
ax.plot(y1)

# fig, ax = plt.subplots()
# ax.plot(20*np.log10(np.abs(X)))


# get the Frequency Response Function
FRF = Y1/X

# get the Impulse Response
h = np.fft.irfft(FRF)

# cut the IR to remove noise (remove useless signal)
h2 = h[8000:16000]
FRF2 = np.fft.rfft(h2)
f_axis2 = np.fft.rfftfreq(len(h2), 1/fs)

# plot the results
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
ax.semilogx(f_axis2, 20*np.log10(np.abs(FRF2)))

fig, ax = plt.subplots()
ax.plot(h)
ax.set(title='Impulse response')


plt.show()
