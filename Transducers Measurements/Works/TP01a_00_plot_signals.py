# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a sine signal to the soundcard output 1, records
    the inputs 1 and 2, and plots the last 10 periods of both signals

Usage:
    Verify the setup.

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
f0 = 100                    # frequency [Hz]
T = 0.5                     # time duration [s]
t = np.arange(0, T, 1/fs)   # time axis
x = np.sin(2*np.pi*f0*t)    # signal definition


""" Play and record simultaneously with sound card """
y = sd.playrec(0.8*x,                 # x is the signal to play
               samplerate=fs,         # sample rate
               channels=2,            # number of input channels
               input_mapping=(1, 2),  # input channels 1 and 2
               blocking=True          # wait until playback is finished
               )


""" Plot last 10 periods of the recorded signal """
fig, ax = plt.subplots()
ax.plot(y[-10*np.round(fs/f0).astype(np.uint):, :])


"""_______________________________________

NOTE:

If the plot shows only one signal (or two very same signals) then probably Windows audio input
is set incorrectly to just one channel. See the following video-tutorial how to correct it.
https://umotion.univ-lemans.fr/video/8187-windows-10-sound-card-setup-2-channels/

"""
