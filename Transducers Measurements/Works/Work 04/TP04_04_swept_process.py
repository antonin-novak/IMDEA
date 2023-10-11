import numpy as np
import matplotlib.pyplot as plt
from functions.SynchSweptSine import SynchSweptSine


""" Load the measurement data """
with np.load('results_part_4/swept.npz') as data:
    u = data['u']                   # recorded signal [V]
    f1 = data['f1']                 # start frequency [Hz]
    f2 = data['f2']                 # end frequency [Hz]
    T = data['T']                   # time length of the swept-sine [s]
    mic_sens = data['mic_sens']     # microphone sensitivity [V/m]
    fs = data['fs']                 # sample rate [Hz]


""" Parameters for nonlinear sepearation """
sss = SynchSweptSine(f1=f1, f2=f2, T=T, fs=fs)
len_IR = 2**13              # length of the extracted impulse responses
N = 3                       # number of higher harmonics to be extracted


""" Convert the measured voltage to pressure using microphone sensitivity """
p = u


""" Extract spectra from swept-sine  """
h = sss.getIR(p)                                # the full impulse response
Hs = sss.separate_IR(h, N, n_samples=len_IR)    # separatef HHFRs
f_axis = np.fft.rfftfreq(len_IR, 1/fs)


""" Plot HHFRs """
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Hs.T)))
ax.set(xlim=(20, 20e3))
ax.set(title='Higher Harmonic Frequency Responses')
ax.set(xlabel='Frequency [Hz]', ylabel='Sound Pressure Level [dB SPL]')


""" Plot Impulse Response """
fig, ax = plt.subplots()
ax.plot(h)
ax.set(title='Impulse Response')
ax.set(xlabel='Samples [-]')
