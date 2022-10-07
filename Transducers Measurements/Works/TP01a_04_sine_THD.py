# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement 
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a sine signal to the soundcard output 1, records
    the inputs 1 and 2, and calculates and plots the Fourier Transform
    of input 2 (output of the Device Under Test).

Usage:
    Measure and plot the distorted spectra to estimate the 
    Total Harmonic Distortion (THD) for a single frequency.

Author:
    Antonin Novak - 29.10.2021
'''

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


""" Sound card setup """
print(sd.query_devices())   # show list of devices
sd.default.device = (1, 6)  # set the device numbers (input, output)


""" Parameters """
fs = 48000                  # sample rate [Hz]


""" SINE signal definition """
f0 = 500                    # frequency [Hz]
T = 2                       # time duration [s]
t = np.arange(0, T, 1/fs)   # time axis
x = np.sin(2*np.pi*f0*t)    # signal definition


""" Play and record simultaneously with sound card """
y = sd.playrec(0.8*x,                 # x is the signal to play
               samplerate=fs,         # sample rate
               channels=2,            # number of input channels
               input_mapping=(1, 2),  # input channels 1 and 2
               blocking=True          # wait until playback is finished
               )


""" Plot the recorded signal """
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title='Recorder signals')


""" Select one second of the output signal """
y2 = y[-fs:, 1]


""" Calculate the FFT """
Y2 = np.fft.rfft(y2)/len(y2)*2
f_axis = np.fft.rfftfreq(len(y2), 1/fs)


""" Plot FFT of y2 """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y2)))
ax.set(xlim=(200, 20e3), ylim=(-50, -0))
ax.set(title='Power Spectrum of the signal y2')
ax.set(xlabel='Frequency [Hz]', ylabel='Magnitude [dB re 1 V]')


"""_______________________________________

CONTINUE THE CODE FROM HERE:

1) use the 'TP01a_05_swept_sine_nonlinear.py' program to measure the Higher Harmonic Frequency Responses (HHRFs),
   and save them to a numpy zip (.npz) file

2) load the '.npz' file here and plot it to the same graph with the Power Spectra of the signal y2
   to verify the correct HHRFs 

"""

