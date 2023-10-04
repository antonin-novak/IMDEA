# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
TP03 : Eddy currents - measurement
    
Description:
    Sends a multitone signal to output AO_0 of the data acquisition
    device and records the inputs AI_0 (voltage across the voice-coil) 
    and AI_1 (voltage across a 1 Ohm resistor = current).

    Supposed sound card: Data Acquisition Module NI USB-4431

Usage:
    Blocked impedance voice-coil measurement.


Author:
    Antonin Novak - 04.10.2023

"""


import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.Multitone import Multitone

""" Parameters """
Dev = 'Dev6'  # name of the NI device
fs = 48000  # sampling frequency


""" Sensitivities """
voltage_sensitivity = 1  # V/V
current_sensitivity = 1  # A/V (depends on resistor value)


""" MULTI-TONE signal generation """
multitone = Multitone(f1=10, f2=20e3, N=100, T=3, fs=fs)


""" Measurement  """
y = measurement_NI(0.9*multitone.signal, fs, Dev)

# voltage [V] (time domain signal)
u = voltage_sensitivity*np.array(y[0])
# current [A] (time domain signal)
i = current_sensitivity*np.array(y[1])

""" Calculate the FFT """
U = multitone.extract_spectra(u)
I = multitone.extract_spectra(i)
f_axis = multitone.frequencies

""" SAVE  """
np.savez('results_part_1/coil_in_air.npz',
         f_axis=f_axis, fs=fs, U=U, I=I)


""" Apparent Resistance and Inductance  """
Ze = U/I
Re = np.real(Ze)
Le = np.imag(Ze)/(2*np.pi*f_axis)

""" PLOT the results  """
fig, ax = plt.subplots(2)
ax[0].set(title=f'Blocked Impedance (@ {np.std(u):0.2f} Vrms)')

ax[0].semilogx(f_axis, np.abs(Re))
ax[0].set(xlabel='Frequency [Hz]', ylabel='Re(f) [Ohm]')
ax[0].set(xlim=[10, 20e3], ylim=[0, 10])
ax[0].grid(True)

ax[1].semilogx(f_axis, np.abs(1000*Le))
ax[1].set(xlabel='Frequency [Hz]', ylabel='Le(f) [mH]')
ax[1].set(xlim=[10, 20e3], ylim=[0, 1])
ax[1].grid(True)


plt.show()
