# import the module
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt


# sample rate
fs = 48000

# generate MLS signal
M = 15
N = 2**M - 1
shift_register = np.ones(M)
mls_signal = np.zeros(N)

for n in range(N):
    mls_signal[n] = shift_register[-1]
    temp = np.logical_xor(shift_register[14], shift_register[7])
    shift_register = np.roll(shift_register, 1)
    shift_register[0] = temp

x = 2*mls_signal - 1

# plot MLS signal
fig, ax = plt.subplots()
ax.plot(x)

# Fourier Transform
X = np.fft.rfft(x)

# plot the spectrum
fig, ax = plt.subplots()
ax.plot(np.abs(X))


# set the device numbers (input, output)
sd.default.device = (6, 6)


# play and record simultaneously
y = sd.playrec(0.8*np.concatenate((x, x)),  # x is the signal to play
               samplerate=fs,
               channels=1,
               output_mapping=(1),
               input_mapping=(1),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )

x = x[-N:]
y = y[-N:, 0]

# plot the signal
fig, ax = plt.subplots()
ax.plot(y)

# Fourier Transform
X = np.fft.rfft(x) / len(x) * 2
Y = np.fft.rfft(y) / len(y) * 2
f_axis = np.fft.rfftfreq(len(y), 1/fs)

# FRF
FRF = Y/X


# impulse response
h = np.fft.irfft(FRF)

# plot the impulse response
fig, ax = plt.subplots()
ax.plot(h)

# limit the IR to useful part
h_cut = h[9200:10000]
FRF_cut = np.fft.rfft(h_cut)
f_axis_cut = np.fft.rfftfreq(len(h_cut), 1/fs)

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
ax.semilogx(f_axis_cut, 20*np.log10(np.abs(FRF_cut)))
ax.set(xlabel='Freqeuncy [Hz]', ylabel='FRF [dB]')


plt.show()
