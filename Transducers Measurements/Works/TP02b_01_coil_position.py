# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
TP02a : Eddy currents, measurement and modeling
    
Description:
    Sends a Multitone signal to output AO_0 of the data acquisition
    device and records the inputs AI_0 (voltage across the load) 
    and AI_1 (voltage across resistor with oposite polarity).

    Supposed sound card: Data Acquisition Module NI USB-4431

Usage:
    Blocked impedance voice-coil measurement.


Author:
    Antonin Novak - 29.10.2021

"""


import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI
from functions.Multitone import Multitone

""" Parameters """
Dev = 'Dev2'  # name of the NI device
fs = 48000  # sampling frequency


""" Sensitivities """
voltage_sensitivity = 1  # V/V
current_sensitivity = -1  # A/V (depends on resistor value)


""" MULTI-TONE signal generation """
multitone = Multitone(f1=20, f2=20e3, N=100, T=3, fs=fs)


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

#np.savez('results/TP02b/impedance.npz', f_axis=f_axis, fs=fs, U=U, I=I)

""" PLOT for verification """
fig, ax = plt.subplots()
ax.plot(u)
ax.set(title=f'Voltage, Vrms = {np.std(u):0.2f}')

plt.show()
