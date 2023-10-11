
import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from TP04_00_parameters import Dev, fs, mic_sens

""" Filename of the numpy zip file """
filename = 'results_part_2/multitone.npz'


""" Generate a Multitone signal"""
T = 2                               # Total duration for the signals [s]
f1 = 20                             # First frequency of the multitone signal [Hz]
f2 = 20e3                           # Last frequency of the multitone signal [Hz]
N_freq = 100                        # Number of unique frequencies between f1 and f2
t = np.arange(0, T, 1/fs)           # Time vector ranging from 0 to T with intervals of 1/fs

# Generate a set of frequencies logarithmically spaced between f1 and f2
# np.round()  ... to ensure they are discrete frequencies
# np.unique() ... to ensure there are no repeated frequencies due to the rounding
frequencies = np.unique(np.round(np.logspace(np.log10(f1), np.log10(f2), N_freq, endpoint=True)))

# Generate the multitone signal
out_signal = 

# we need to normalize the signal to fit between digital +1 and -1
norm_amplitude = np.max(np.abs(out_signal))
out_signal /= norm_amplitude


""" Measurement using a National Instruments device  """
y = measurement_NI(out_signal, fs, Dev, iepe=[True])

# Extract signals from measured data (voltage)
u = np.array(y)



""" SAVE  """
np.savez(filename, u=u, out_signal=out_signal, frequencies=frequencies, mic_sens=mic_sens, T=T, fs=fs)


""" Plot the measured signal on input AI0 """
fi, ax = plt.subplots()
ax.plot(u)