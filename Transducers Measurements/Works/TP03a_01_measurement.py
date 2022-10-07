# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP03a : Advanced linear parameters measurement

Description:
    Sends a Swept-sine signal to the NI acquisition device output AO0,
    records the following inputs:
    AI0 ... voltage across the loudspeaker
    AI1 ... voltage (oposite polarity) across the 1 Ohm resistor
    AI2 ... displacement (from laser sensor)
    Calculate their Fourier Transform and saves these values
    into a .npz file (use TP03a_02_data_load.py to continue)

Usage:
    Measures and saves the frequency response of 
    U ... voltage across the loudspeaker
    I ... current (voltage across the 1 Ohm resistor)
    X  ... displacement (from laser sensor)

Author:
    Antonin Novak - 29.10.2021
'''


import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.SynchSweptSine import SynchSweptSine


""" Parameters """
Dev = 'Dev2'  # name of the NI device
fs = 48000  # sampling frequency

""" Sensitivities """
voltage_sensitivity = 1  # [V/V]
current_sensitivity = -1  # [A/V]
displacement_sensitivity = 2e-3  # [m/s]

""" Creating Swept-sine wave for Analog output generation"""
sss = SynchSweptSine(f1=5, f2=20e3, T=10, fs=fs)
x = np.concatenate((np.zeros(10000), sss.signal, np.zeros(10000)))


""" Measurement  """
y = measurement_NI(0.5*x, fs, Dev)
# voltage [V] (time domain signal)
u = voltage_sensitivity * np.array(y[0])
# current [A] (time domain signal)
i = current_sensitivity * np.array(y[1])
# displacement [m] (time domain signal)
x = displacement_sensitivity * np.array(y[2])


""" Extract spectra from swept-sine  """
U = sss.getFRF(u, fs)          # voltage [V] (frequency domain)
I = sss.getFRF(i, fs)          # current [A] (frequency domain)
X = sss.getFRF(x, fs)          # displacement [m] (frequency domain)
f_axis = sss.f_axis(fs)

""" SAVE  """
np.savez('results/TP03a/meas_data.npz', f_axis=f_axis, fs=fs, U=U, I=I, X=X)


"""_______________________________________
You do not need to modify this file (except name of the save-file).
1) use this file to measure and save the data to a .npz file
2) load the data in the separate file 'TP03a_02_data_load.py'
"""


""" PLOT for verification  """
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U))
ax.set(xlabel='Frequency [Hz]', ylabel='Voltage Spectra [V]')
ax.set(xlim=[10, 20e3])
ax.grid(True)

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(I))
ax.set(xlabel='Frequency [Hz]', ylabel='Current Spectra [V]')
ax.set(xlim=[10, 20e3])
ax.grid(True)

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(X))
ax.set(xlabel='Frequency [Hz]', ylabel='Displacement Spectra [m]')
ax.set(xlim=[10, 20e3])
ax.grid(True)
