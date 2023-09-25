# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP 2, part 1: Dynamic compression

Description:
    Sends a Swept-sine signal to the NI acquisition device output AO0,
    records the following inputs:
    AI0 ... voltage across the loudspeaker
    AI1 ... voltage (oposite polarity) across the 1 Ohm resistor
    AI2 ... displacement (from laser sensor)
    Calculates the fourier transform of voltage, current and displacement.

Usage:
    Measures, saves, and plots the following frequency responses:
    X/U ... displacement over voltage 
    X/I ... displacement over current 
    for several signal levels (see 'amplitudes' array)

Author:
    Antonin Novak - 29.10.2021, last modification 21.09.2023
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
current_sensitivity = 1  # [A/V]
displacement_sensitivity = 2e-3  # [m/V]


""" Creating Swept-sine wave for Analog output generation"""
sss = SynchSweptSine(f1=5, f2=1e3, T=5, fs=fs)
out_signal = np.concatenate((np.zeros(10000), sss.signal, np.zeros(10000)))


""" Amplitudes  """
# amplitudes = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
amplitudes = [1]

# prepare empty arrays
U, I, X = [], [], []


""" Measurement  """
for A in amplitudes:

    y = measurement_NI(A*out_signal, fs, Dev)

    ''' Extract signals from measured data '''
    u = voltage_sensitivity * np.array(y[0])       # voltage [V]
    i = current_sensitivity * np.array(y[1])       # current [A]
    x = displacement_sensitivity * np.array(y[2])  # displacement [m]

    ''' Extract spectra from swept-sine  '''
    U.append(sss.getFRF(u, fs)[:1000])  # voltage [V] (frequency domain)
    I.append(sss.getFRF(i, fs)[:1000])  # current [A] (frequency domain)
    X.append(sss.getFRF(x, fs)[:1000])  # displacement [m] (frequency domain)


# frequency axis
f_axis = sss.f_axis(fs)[:1000]


""" SAVE  """
np.savez('results_part_1/meas_data_speaker_01.npz',
         f_axis=f_axis, fs=fs, U=U, I=I, X=X)


""" PLOT the results  """
fig1, ax1 = plt.subplots()  # figure for displacement over voltage
fig2, ax2 = plt.subplots()  # figure for displacement over current

for k in range(len(U)):
    # calculate the rms value
    Urms = np.mean(np.abs(U[k][100:800])) / np.sqrt(2)
    ax1.semilogx(f_axis, np.abs(1000*X[k]/U[k]), label=f"{Urms:0.2f} Vrms")
    ax2.semilogx(f_axis, np.abs(1000*X[k]/I[k]), label=f"{Urms:0.2f} Vrms")


ax1.set(xlabel='Frequency [Hz]', ylabel='|X/U| [mm/V]')
ax1.set(xlim=[10, 500], ylim=[0, 1.5])
ax1.grid(True)
ax1.legend()

ax2.set(xlabel='Frequency [Hz]', ylabel='|X/I| [mm/A]')
ax2.set(xlim=[10, 500], ylim=[0, 40])
ax2.grid(True)
ax2.legend()
