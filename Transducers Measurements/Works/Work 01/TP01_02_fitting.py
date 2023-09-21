# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP03a : Advanced linear parameters measurement

Description:
    Loads the saved data obtained from loudspeaker measurement.

Usage:
    Loads the following quantities. 
    U ... voltage across the loudspeaker
    I ... current through the loudspeaker
    X  ... displacement (from laser sensor)

Author:
    Antonin Novak - 29.10.2021, last modificaton 21.9.2023
'''

import numpy as np
import matplotlib.pyplot as plt


""" Load the saved data and extract the variables """
with np.load('results/meas_data.npz') as data:
    U = data['U']
    I = data['I']
    X = data['X']
    f_axis = data['f_axis']
    fs = data['fs']


""" PLOT for verification  """
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U))
ax.set(xlabel='Frequency [Hz]', ylabel='Voltage Spectra [V]', title='Voltage')
ax.set(xlim=[10, 20e3])
ax.grid(True)

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(I))
ax.set(xlabel='Frequency [Hz]', ylabel='Current Spectra [I]', title='Current')
ax.set(xlim=[10, 20e3])
ax.grid(True)

fig, ax = plt.subplots()
ax.semilogx(f_axis, 1000*np.abs(X))
ax.set(xlabel='Frequency [Hz]',
       ylabel='Displacement Spectra [mm]', title='Displacement')
ax.set(xlim=[10, 20e3])
ax.grid(True)
