# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01b : Electrostatic microphone calibration

Description:
    Sends a sine signal to the NI acquisition device output AO0,
    records the input AI1, and calculates and plots the Fourier Transform
    of input AI1.

Usage:
    Measure and plot the distorted spectra to estimate the 
    Total Harmonic Distortion (THD) for a single frequency.

Author:
    Antonin Novak - 29.10.2021
'''


import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI


""" Parameters """
Dev = 'Dev1'    # name of the NI device
fs = 102400     # sampling frequency


""" SINE signal definition """
A = 0.1
f0 = 1500
T = 2
t = np.arange(0, T, 1/fs)
x = np.sin(2*np.pi*f0*t)


""" Measurement  """
y = measurement_NI(A*x, fs, Dev)


""" plot the recorded signal """
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title='Recorded signals')


""" select one second of the output signal """
y2 = y[1][-fs:]


""" calculate the FFT """
Y2 = np.fft.rfft(y2)/len(y2)*2
f_axis = np.fft.rfftfreq(len(y2), 1/fs)


""" SAVE  """
np.savez('results/TP01b/TP01b_meas_data_thd_mic1.npz',
         f_axis=f_axis, fs=fs, Y2=Y2)


""" plot FFT of y2 """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y2)))
ax.set(xlim=(200, 20e3), ylim=(-100, -0))
