# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP 2, part 3: Creep Effect

Description:
    Records the following inputs (5 minutes of recording):
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
    Antonin Novak - 29.10.2021, last modification 21.09.2023
'''

import numpy as np
import matplotlib.pyplot as plt
from functions.measurement_NI import measurement_NI


""" Parameters """
Dev = 'Dev2'  # name of the NI device
fs = 2000     # sampling frequency (very low to avoid huge data files)

""" Sensitivities """
voltage_sensitivity = 1  # [V/V]
current_sensitivity = 1  # [A/V]
displacement_sensitivity = 2e-3  # [m/V]
displacement_DC_offset = 2.5  # offset of the displacement sensor [V]


""" Prepare a signal of 5 minutes (just zeros) """
output = np.zeros(5*60*fs)


""" Measurement  """
y = measurement_NI(output, fs, Dev)

u = voltage_sensitivity * np.array(y[0])  # voltage [V] (time domain signal)
i = current_sensitivity * np.array(y[1])  # current [A] (time domain signal)
x = np.array(y[2]) - displacement_DC_offset
x *= displacement_sensitivity  # displacement [m] (time domain signal)

t = np.arange(0, len(u))/fs  # time axis [s]


""" SAVE  """
np.savez('results_part_3/meas_data_up.npz', u=u, i=i, x=x)


""" PLOT  """
fig, ax = plt.subplots(3, sharex=True)
ax[0].semilogx(t, u)
ax[0].set(ylabel='Voltage [V]')
ax[0].grid(True)

ax[1].semilogx(t, i)
ax[1].set(ylabel='Current [A]')
ax[1].grid(True)

ax[2].plot(t-1e-3, 1000*x)  # compensating displacement sensor delay of 1 ms
ax[2].set(ylabel='Displacement [mm]')
ax[2].grid(True)

plt.tight_layout()
