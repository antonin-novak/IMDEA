
import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from TP04_00_parameters import Dev, fs, mic_sens


""" Load the measurement data """
with np.load('results_part_1/sine01.npz') as data:
    u = data['u']                   # recorded signal [V]
    f0 = data['f0']                 # frequency of the sine-wave [Hz]
    T = data['T']                   # Total time for the sine wave [s]
    mic_sens = data['mic_sens']     # microphone sensitivity [V/Pa]
    fs = data['fs']                 # sample rate [Hz]


""" Convert the measured voltage to pressure using microphone sensitivity """
p = u


""" Calculate the Fourier Transform and create frequency axis """
P = np.fft.rfft(p)
f_axis = np.fft.rfftfreq(len(p), 1/fs)


""" Plot the Frequency Spectrum (in dB SPL) """
fig, ax = plt.subplots()  # figure for displacement over voltage
ax.plot(f_axis, 20*np.log10(np.abs(P)))
ax.set(xlabel='Frequency [Hz]', ylabel='Sound Pressure Level [dB SPL]')
ax.set(xlim=(0, 2000))
