# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a Multitone signal to the soundcard output 1, records
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
f1 = 20                     # first frequency of the multi-tone signal [Hz]
f2 = 20e3                   # last frequency of the multi-tone signal [Hz]
# number of frequencies (may be reduced due to the 'unique' function)
N = 100
T = 2                       # time length of the multi-tone [s]


""" MULTI-TONE signal generation """
frequencies = np.unique(np.round(np.logspace(
    np.log10(f1), np.log10(f2), N))).astype(np.uint)
t = np.arange(0, T, 1/fs)
x = np.zeros(T*fs)

for f0 in frequencies:
    x += np.sin(2*np.pi*f0*t + 2*np.pi*np.random.rand())

x = x / np.max(np.abs(x))


""" Play and record simultaneously with sound card """
y = sd.playrec(0.8*x,                 # multi-tone signal
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
y1 = y[-fs:, 0]  # select just one secod of the multi-tone
y2 = y[-fs:, 1]


""" Calculate the FFT """
Y1all = np.fft.rfft(y1)/len(y1)*2
Y2all = np.fft.rfft(y2)/len(y2)*2
f_axis = np.fft.rfftfreq(len(y1), 1/fs)


""" PLOT the spectra of the outpus signal """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Y2all)))
ax.set(xlim=(20, 20e3), ylim=(-150, -40))
ax.set(title="Spectra of the ouptut signal")


"""_______________________________________

CONTINUE THE CODE FROM HERE:

1) try to plot the Frequency Response Function (FRF) of the device under test
2) try to plot the Impulse Response (IR) of the device under test
3) save the results (FRF with frequency axis and IR) into a numpy zip (.npz)

"""
np.savez('results/TP01a/FRF_multitone.npz', Y1all=Y1all, Y2all=Y2all, frequencies=frequencies, fs=fs)
