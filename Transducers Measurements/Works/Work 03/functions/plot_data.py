# -*- coding: utf-8 -*-
"""
Le Mans University, FRANCE
M2 IMDEA, Transducers Measurement
    
Description:
    A function to load the data from the measurement of blocked impedance
    and plots the apparent resistance Re(f)
    and apparent inductance Le(f)

Author:
    Antonin Novak - 04.10.2023

"""

import numpy as np
import matplotlib.pyplot as plt

def plot_ReLe(names, ylim_Re, ylim_Le):
    
    fig, ax = plt.subplots(2)
    
    for name in names:
    
        """ Load the saved data and extract the variables """
        with np.load(name[0]) as data:
            U = data['U']
            I = data['I']
            f_axis = data['f_axis']
    
        
        """ Apparent Resistance and Inductance  """
        Ze = U/I
        Re = np.real(Ze)
        Le = np.imag(Ze)/(2*np.pi*f_axis)
 
        ax[0].semilogx(f_axis, np.abs(Re), label=name[1])
        ax[1].semilogx(f_axis, np.abs(1000*Le), label=name[1])
    
    
    ax[0].set(xlabel='Frequency [Hz]', ylabel='Re(f) [Ohm]')
    ax[0].set(xlim=[20, 20e3], ylim=ylim_Re)
    ax[0].grid(True)
    ax[0].legend(loc='upper left')
        
    ax[1].set(xlabel='Frequency [Hz]', ylabel='Le(f) [mH]')
    ax[1].set(xlim=[20, 20e3], ylim=ylim_Le)
    ax[1].grid(True)
    ax[1].legend()
    
    plt.tight_layout()
    
    
