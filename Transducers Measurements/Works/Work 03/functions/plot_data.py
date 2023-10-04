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

# Importing required libraries
import numpy as np
import matplotlib.pyplot as plt


def plot_ReLe(names, ylim_Re, ylim_Le):
    """
    Function to plot the apparent resistance Re(f) and 
    apparent inductance Le(f) against the frequency.

    Parameters:
    - names: List of tuples, where each tuple contains the name of the file
             to be loaded and the label to be displayed in the legend.
    - ylim_Re: Tuple of y-axis limits for the Re(f) plot.
    - ylim_Le: Tuple of y-axis limits for the Le(f) plot.
    """

    # Create a subplot with 2 rows
    fig, ax = plt.subplots(2)

    for name in names:
        # Load the saved data and extract the variables
        with np.load(name[0]) as data:
            U = data['U']
            I = data['I']
            f_axis = data['f_axis']

        # Calculate Apparent Resistance and Inductance
        Ze = U/I
        Re = np.real(Ze)
        Le = np.imag(Ze)/(2*np.pi*f_axis)

        # Plot the calculated values for Re and Le
        ax[0].semilogx(f_axis, np.abs(Re), label=name[1])
        ax[1].semilogx(f_axis, np.abs(1000*Le), label=name[1])

    # Set plot parameters for Re(f)
    ax[0].set(xlabel='Frequency [Hz]', ylabel='Re(f) [Ohm]')
    ax[0].set(xlim=[20, 20e3], ylim=ylim_Re)
    ax[0].grid(True)
    ax[0].legend(loc='upper left')

    # Set plot parameters for Le(f)
    ax[1].set(xlabel='Frequency [Hz]', ylabel='Le(f) [mH]')
    ax[1].set(xlim=[20, 20e3], ylim=ylim_Le)
    ax[1].grid(True)
    ax[1].legend()

    # Adjust layout
    plt.tight_layout()


def plot_current_spec(names, df=30, n_rows_max=3):
    """
    Function to plot the current spectrum against the frequency.

    Parameters:
    - names: List of tuples, where each tuple contains the name of the file
             to be loaded and the label to be displayed in the title.
    - df: Frequency resolution (not used in this function).
    - n_rows_max: Maximum number of rows for the subplot grid.
    """

    # Determine the number of rows and columns for the subplot grid
    n = len(names)
    n_rows = min(n_rows_max, n)
    n_cols = (n // n_rows_max) + (1 if n % n_rows_max else 0)

    # Create a subplot grid
    fig, axes = plt.subplots(n_cols, n_rows, sharex=True, sharey=True)
    axes = np.atleast_2d(axes)

    # Hide unused axes
    for i in range(n, n_rows * n_cols):
        axes.ravel()[i].axis('off')

    # Access the default color cycle
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for ax, name, color in zip(axes.ravel(), names, colors):
        # Load the saved data and extract the variables
        with np.load(name[0]) as data:
            I = data['I']
            f_axis = data['f_axis']

        # Plot the results in dB scale
        ax.plot(f_axis, 20*np.log10(np.abs(I)), label=name[1], color=color)
        ax.set_title(name[1], color=color)
        ax.set(xlim=(0, 5e3), ylim=(-90, 10))
        ax.grid(True)

    # Set y-label for the left-most plots
    for ax in axes[:, 0]:
        ax.set(ylabel='Current Spectrum [dB re A]')
    # Set x-label for the bottom-most plots
    for ax in axes[-1, :]:
        ax.set(xlabel='Frequency [Hz]')

    # Adjust layout
    fig.tight_layout()
