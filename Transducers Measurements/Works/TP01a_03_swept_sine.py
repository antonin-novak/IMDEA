# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a Swept-sine signal to the soundcard output 1, records
    the inputs 1 and 2, and calculates the Fourier Transform
    of both inputs.

Usage:
    Complete the file and try to estimate the Frequency Response
    Function (FRF) and the Impulse Response (IR)

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
f1 = 20                     # start frequency [Hz]
f2 = 20e3                   # end frequency [Hz]
N = 100                     # number of frequencies
T = 3                       # time length of the swept-sine [s]


""" SWEPT-SINE signal generation """
t = np.arange(0, T, 1/fs)
L = T/np.log(f2/f1)
s = np.sin(2*np.pi*f1*L*(np.exp(t/L)))

# add 0.5 seconds of zeros at the end to take latency into account
out_signal = np.concatenate((s, np.zeros(round(0.5*fs))))


""" Play and record simultaneously with sound card """
y = sd.playrec(0.8*out_signal,        # swept-sine signal
               samplerate=fs,         # sample rate
               channels=2,            # number of input channels
               input_mapping=(1, 2),  # input channels 1 and 2
               blocking=True          # wait until playback is finished
               )


""" Plot the recorded signal """
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title='Recorder signals')


""" Calculate the FFT """
Y1 = np.fft.rfft(y[:, 0])/fs*2
Y2 = np.fft.rfft(y[:, 1])/fs*2


"""_______________________________________
CONTINUE THE CODE FROM HERE:

1) try to plot the Frequency Response Function (FRF) of the device under test
2) try to plot the Impulse Response (IR) of the device under test
3) save the results (FRF with frequency axis and IR) into a numpy zip (.npz) file

4) create a separate .py file in which you load all the data from previous 
   steps (MLS, Multitione) and plot them into the same figures for a) FRF, b) IR

"""

np.savez('results/TP01a/FRF_swept_sine.npz', Y1=Y1, Y2=Y2, fs=fs)