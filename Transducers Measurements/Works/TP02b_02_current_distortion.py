# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
TP02b : Harmonic Distortion of blocked coil
    
Description:
    Sends a Sine signal to output AO_0 of the data acquisition
    device and records the inputs AI_0 (voltage across the load) 
    and AI_1 (voltage across resistor with oposite polarity).

    Supposed sound card: Data Acquisition Module NI USB-4431

Usage:
    Current Distortion measurement of blocked voice-coil .


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


""" SINE signal generation """
f0 = 500
T = 2
t = np.arange(0, T, 1/fs)
x = np.sin(2*np.pi*f0*t)


""" Measurement  """
y = measurement_NI(0.9*x, fs, Dev)

# voltage [V] (time domain signal)
u = voltage_sensitivity*np.array(y[0])[-fs:]
# current [A] (time domain signal)
i = current_sensitivity*np.array(y[1])[-fs:]

""" Calculate the FFT """
U = np.fft.rfft(u)/len(u)*2
I = np.fft.rfft(i)/len(u)*2
f_axis = np.fft.rfftfreq(fs, 1/fs)

#np.savez('results/TP02b/distortion.npz', f_axis=f_axis, fs=fs, U=U, I=I)

""" PLOT for verification """
fig, ax = plt.subplots()
ax.plot(u)
ax.set(title=f'Voltage, Vrms = {np.std(u):0.2f}')

""" PLOT for verification """
fig, ax = plt.subplots()
ax.plot(f_axis, 20*np.log10(np.abs(I)))
ax.set(title='Current',
       xlabel='Frequency [Hz]', ylabel='I [dB re A]')
ax.set(xlim=(0, 5e3), ylim=(-90, 10))

plt.show()
