
import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.SynchSweptSine import SynchSweptSine
from TP04_00_parameters import Dev, fs, mic_sens

""" Filename of the numpy zip file """
filename = 'results_part_4/swept.npz'

""" Generate a Swept-sine signal"""
f1 = 20                     # start frequency [Hz]
f2 = 20e3                   # end frequency [Hz]
T = 8                       # time length of the swept-sine [s]

# note that 'sss' is an object.
sss = SynchSweptSine(f1=f1, f2=f2, T=T, fs=fs)
out_signal = np.concatenate((sss.signal, np.zeros(int(0.5*fs))))


""" Measurement using a National Instruments device  """
y = measurement_NI(out_signal, fs, Dev, iepe=[True])

# Extract signals from measured data (voltage)
u = np.array(y)


""" SAVE  """
np.savez(filename, u=u, f1=f1, f2=f2, T=T, mic_sens=mic_sens, fs=fs)


""" PLOT the results  """
fi, ax = plt.subplots()
ax.plot(u)
