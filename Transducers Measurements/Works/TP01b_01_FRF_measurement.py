# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01b : Electrostatic microphone calibration

Description:
    Sends a Swept-sine signal to the NI acquisition device output AO0,
    records the inputs AI0 and AI1, calculates the Frequency Response 
    Function (FRF) between AI1 and AI2.

Usage:
    Measure and plot the Frequency Response Function (FRF) H = AI1 / AI0
    AI0 ... analog input 0 of the NI acquisition device
    AI1 ... analog input 1 of the NI acquisition device

Author:
    Antonin Novak - 29.10.2021
'''

import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.SynchSweptSine import SynchSweptSine


""" Parameters """
Dev = 'Dev1'  # name of the NI device
fs = 102400  # sampling frequency
A = 0.5      # Amplitude [V] of the output signal (do not change !!!)


""" Swept-sine signal for Analog output generation"""
sss = SynchSweptSine(f1=5, f2=50e3, T=10, fs=fs)
x = np.concatenate((np.zeros(10000), sss.signal, np.zeros(10000)))


""" Measurement  """
y = measurement_NI(A*x, fs, Dev)


""" Extract spectra from swept-sine  """
Y1 = sss.getFRF(np.array(y[0]), fs)
Y2 = sss.getFRF(np.array(y[1]), fs)


""" Frequency Response Function """
H = Y2/Y1
f_axis = sss.f_axis(fs)


""" SAVE  """
np.savez('results/TP01b/meas_data_frf_mic1.npz', f_axis=f_axis, fs=fs, H=H)


""" PLOT  """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(H)))
ax.set(xlabel='Frequency [Hz]', ylabel='FRF [dB]')
ax.set(xlim=[10, 50e3])
ax.grid(True)
