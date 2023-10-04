# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
TP03 : Eddy currents - results
    
Description:
    Loads the data from the measurement of blocked impedance
    and plots the apparent resistance Re(f)
    and apparent inductance Le(f)

Author:
    Antonin Novak - 04.10.2023

"""


import numpy as np
import matplotlib.pyplot as plt
from functions.plot_data import plot_ReLe


""" PLOT the results  """
files = []
files.append(('results_part_1/coil_in_air.npz', 'in air'))
#files.append(('results_part_1/coil_in_motor.npz', 'in motor'))

plot_ReLe(files, ylim_Re=[0, 10], ylim_Le=[0, 2])





plt.show()

