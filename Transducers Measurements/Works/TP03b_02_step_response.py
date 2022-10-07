# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP03b : Dynamic compression & study of feedback u_emf

Description:
    Records the following inputs (5 seconds recordings):
    AI0 ... voltage across the loudspeaker
    AI1 ... voltage (oposite polarity) across the 1 Ohm resistor
    AI2 ... displacement (from laser sensor)
    Deduces the voltage, current and displacement (time-dimain signals).

Usage:
    Measures, saves and plots the following signals (5 seconds recordings):
    u ... voltage across the loudspeaker under test
    i ... current through the loudspeaker
    x ... displacement (laser sensor)

Author:
    Antonin Novak - 29.10.2021
'''

import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI


""" Parameters """
Dev = 'Dev2'  # name of the NI device
fs = 48000  # sampling frequency

""" Sensitivities """
voltage_sensitivity = 1  # [V/V]
current_sensitivity = -1  # [A/V]
displacement_sensitivity = 2e-3  # [m/s]
displacement_DC_offset = 2.5  # offset of the displacement sensor [V]


""" Prepare a signal of 5 seconds (just zeros) """
x = np.zeros(5*fs)


""" Measurement  """
y = measurement_NI(x, fs, Dev)

u = voltage_sensitivity * np.array(y[0])  # voltage [V] (time domain signal)
i = current_sensitivity * np.array(y[1])  # current [A] (time domain signal)
x = np.array(y[2]) - displacement_DC_offset
x *= displacement_sensitivity  # displacement [m] (time domain signal)


""" SAVE  """
np.savez('results/TP03b/meas_data_open.npz', u=u, i=i, x=x)


""" PLOT for verification  """
fig, ax = plt.subplots(3, sharex=True)
ax[0].plot(u)
ax[0].set(ylabel='Voltage [V]')
ax[0].grid(True)

ax[1].plot(i)
ax[1].set(ylabel='Current [A]')
ax[1].grid(True)

ax[2].plot(1000*x)
ax[2].set(ylabel='Displacement [mm]')
ax[2].grid(True)

plt.tight_layout()
plt.show()
