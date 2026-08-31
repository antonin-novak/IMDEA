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
from functions.plot_data import plot_current_spec

files = []
files.append(('results_part_2/coil_in_air.npz', 'air'))
# files.append(('results_part_2/coil_in_iron.npz', 'motor'))

plot_current_spec(files, n_rows_max=2)

plt.show()
