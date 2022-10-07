# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a Maximum Length Sequence (MLS) signal to the soundcard
    output 1, records the inputs 1 and 2, and calculates 
    the Fourier Transform of both inputs.

Usage:
    Complete the file to estimate the Frequency Response Function (FRF)
    and the Impulse Response (IR)

Author:
    Antonin Novak - 29.10.2021
'''

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.signal import max_len_seq


""" Sound card setup """
print(sd.query_devices())   # show list of devices
sd.default.device = (1, 6)  # set the device numbers (input, output)


""" Parameters """
fs = 48000                  # sample rate [Hz]
M = 15                      # MLS order (length of the shift register)
N = 2**M - 1                # length of the MLS signal (one period)


""" MLS signal generation """
x = max_len_seq(15)[0]      # generate one period of the MLS signal


""" Play and record simultaneously with sound card """
y = sd.playrec(0.8*np.tile(x, 2),     # send 2 periods of MLS signal
               samplerate=fs,         # sample rate
               channels=2,            # number of input channels
               input_mapping=(1, 2),  # input channels 1 and 2
               blocking=True          # wait until playback is finished
               )


""" Plot the recorded signal """
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title='Recorder signals')


""" Separate channels """
y1 = y[-N:, 0]  # select just one period of MLS
y2 = y[-N:, 1]


""" calculate the FFT """
Y1 = np.fft.rfft(y1)/len(y1)*2
Y2 = np.fft.rfft(y2)/len(y2)*2


"""_______________________________________

CONTINUE THE CODE FROM HERE:

1) try to plot the Frequency Response Function (FRF) of the device under test
2) try to plot the Impulse Response (IR) of the device under test
3) save the results (FRF with frequency axis and IR) into a numpy zip (.npz)
"""

np.savez('results/TP01a/FRF_mls.npz', Y1=Y1, Y2=Y2, fs=fs)

