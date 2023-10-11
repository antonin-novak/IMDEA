
import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from TP04_00_parameters import Dev, fs, mic_sens


""" Filename of the numpy zip file """
filename = 'results_part_1/sine01.npz'

""" Generate a Sine-wave signal"""
T = 2                               # Total time for the sine wave [s]
f0 = 500                            # Frequency of the sine wave [Hz]
t = np.arange(0, T, 1/fs)           # Time vector ranging from 0 to T with intervals of 1/fs
out_signal =                        # Generate the sine signal


""" Measurement using a National Instruments device  """
y = measurement_NI(out_signal, fs, Dev, iepe=[True])

# Extract signals from measured data (voltage)
u = np.array(y)


""" SAVE  """
np.savez(filename, u=u, f0=f0, mic_sens=mic_sens, T=T, fs=fs)


""" Plot the measured signal on input AI0 """
fi, ax = plt.subplots()
ax.plot(u)
