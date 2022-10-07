# -*- coding: utf-8 -*-
''' Le Mans University, FRANCE
    M2 IMDEA, Transducers Measurement 
    TP01a : MLS, multitone, and swept-sine signals

Description:
    Sends a swept-sine signal to the soundcard output 1, records
    the inputs 1 and 2, and calculates and plots the Higher Harmonic
    Frequency Respones (HHFRs) of input 2 (output of the Device Under Test).

Usage:
    Measure the Higher Harmonic Frequency Respones (HHFRs).

Author:
    Antonin Novak - 29.10.2021
'''

import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from functions.SynchSweptSine import SynchSweptSine


""" Sound card setup """
print(sd.query_devices())   # show list of devices
sd.default.device = (1, 6)  # set the device numbers (input, output)


""" Parameters """
fs = 48000                  # sample rate [Hz]
f1 = 20                     # start frequency [Hz]
f2 = 20e3                   # end frequency [Hz]
T = 8                       # time length of the swept-sine [s]
len_IR = 2**13              # length of the extracted impulse responses
N = 3                       # number of higher harmonics to be extracted


""" SWEPT-SINE signal definition """
sss = SynchSweptSine(f1=f1, f2=f2, T=T, fs=fs)
# note that 'sss' is an object. To see the available methods check the class defined in './functions/SynchSweptSine.py'
out_signal = np.concatenate((sss.signal, np.zeros(int(0.5*fs))))


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

""" Extract spectra from swept-sine  """
h1 = sss.getIR(y[:, 0])     # impulse response of channel 1
h2 = sss.getIR(y[:, 1])     # impulse response of channel 2

# estimate the latency of the sound card from the first (direct) channel
LATENCY = np.where(h2 == np.max(h2))[0][0]

Hs = sss.separate_IR(h2, N, n_samples=len_IR, latency=LATENCY)
f_axis = np.fft.rfftfreq(len_IR, 1/fs)


""" plot FFT of Y2 """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Hs.T)))
ax.set(xlim=(10, 10e3), ylim=(-80, -0))
ax.set(title='Higher Harmonic Frequency Responses')
ax.set(xlabel='Frequency [Hz]', ylabel='Magnitude [dB re 1 V]')


""" SAVE the result to a numpy zip (.npz) file  """
#np.savez('results/TP01a/FRF_swept_sine.npz', f_axis=f_axis, Hs=Hs)
