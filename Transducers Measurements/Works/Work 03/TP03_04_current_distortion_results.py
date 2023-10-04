# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
TP03 : Harmonic Distortion of blocked coil - results
    
Description:
    Loads the data from the measurement of current distortion
    and plots it.

Author:
    Antonin Novak - 04.10.2023

"""


import numpy as np
import matplotlib.pyplot as plt
from functions.plot_data import plot_ReLe


def plot_current_spec(names, df=30):

    fig, ax = plt.subplots(1, len(names), sharex=True, sharey=True)

    ax = [ax] if not isinstance(ax, (list, tuple)) else ax

    for idx, name in enumerate(names):
        """ Load the saved data and extract the variables """
        with np.load(name[0]) as data:
            U = data['U']
            I = data['I']
            f_axis = data['f_axis']

        """ PLOT the results  """
        ax[idx].plot(f_axis, 20*np.log10(np.abs(I)), label=name[1])
        ax[idx].set(title=name[1])
        ax[idx].set(xlabel='Frequency [Hz]')
        ax[idx].set(xlim=(0, 5e3), ylim=(-90, 10))
        ax[idx].grid(True)

    ax[0].set(ylabel='Current Spectrum [dB re A]')
    fig.tight_layout()


files = []
files.append(('results_part_2/coil_in_air.npz', 'air'))
# files.append(('results_part_2/coil_in_motor.npz', 'motor'))
# files.append(('results_part_2/coil_in_assembled_plastic.npz', 'plastic'))
# files.append(('results_part_2/coil_in_assembled_magnet.npz', 'magnet'))

plot_current_spec(files)


plt.show()
