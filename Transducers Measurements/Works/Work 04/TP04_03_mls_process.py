import numpy as np
import matplotlib.pyplot as plt


file_names = ['mls.npz']

fig_FRF, ax_FRF = plt.subplots()  # figure for the Frequency Response
fig_IR, ax_IR = plt.subplots()  # figure for the Impulse Response

for file_name in file_names:

    """ Load the measurement data """
    with np.load(f'results_part_3/{file_name}') as data:
        u = data['u']                       # recorded signal [V]
        x = data['x']                       # original MLS signal
        N_bits = data['N_bits']             # Number of bits for the MLS
        L_sequence = data['L_sequence']     # Length of the MLS sequence
        N_periods = data['N_periods']       # Number of periods
        mic_sens = data['mic_sens']         # microphone sensitivity [V/m]
        fs = data['fs']                     # sample rate [Hz]

    """ Convert the measured voltage to pressure using microphone sensitivity """
    p = u[fs:]  # first second removed

    # """ Do the averaging (calculate the mean value across periods) """
    # p = ...     # 1) change the shape to (N_periods, L_sequence)
    # p = ...     # 2) calculate the mean value accross the 1st axis (N_periods)

    """ Calculate the Fourier Transform and create frequency axis """
    X = np.fft.rfft(x)
    P = np.fft.rfft(p)
    f_axis = np.fft.rfftfreq(len(p), 1/fs)

    """ Calculate the FRF and IR """
    FRF = ...   # Frequency Response Function
    h = ...     # Impulse re

    ax_FRF.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
    ax_FRF.set(xlim=(20, 20e3))
    ax_FRF.grid()
    ax_FRF.legend()

    ax_IR.plot(h)
