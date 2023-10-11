
import numpy as np
import matplotlib.pyplot as plt


""" Load the measurement data """
with np.load('results_part_2/multitone.npz') as data:
    out_signal = data['out_signal']     # original multitone signal
    u = data['u']                       # recorded signal [V]
    frequencies = data['frequencies']   # vector of multitone frequencies [Hz]
    T = data['T']                       # Total time for the sine wave [s]
    mic_sens = data['mic_sens']         # microphone sensitivity [V/m]
    fs = data['fs']                     # sample rate [Hz]


""" Convert the measured voltage to pressure using microphone sensitivity """
p = u


""" Calculate the Fourier Transform and create frequency axis """
P = np.fft.rfft(p)
f_axis = np.fft.rfftfreq(len(p), 1/fs)


""" Plot the Frequency Spectrum (in dB SPL) """
fig, ax = plt.subplots()  # figure for displacement over voltage
ax.semilogx(f_axis, 20*np.log10(np.abs(P)))
ax.set(xlabel='Frequency [Hz]', ylabel='Sound Pressure Level [dB SPL]')
ax.set(xlim=(20, 20e3))
