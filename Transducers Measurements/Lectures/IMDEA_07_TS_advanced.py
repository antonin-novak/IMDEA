import numpy as np
import matplotlib.pyplot as plt

''' LOAD DATA'''
# load the data file
data = np.load('meas_data.npz')

# extract the frequency axis
f_axis = data['f_axis']
f1, f2 = np.argmax(f_axis > 20), np.argmax(f_axis > 20e3)

# use only useful frequencies
f_axis = data['f_axis'][f1:f2]
U = data['U'][f1:f2]
I = data['I'][f1:f2]
V = data['V'][f1:f2]

# input impedance
Z = U/I

# angular frequency
w = 2*np.pi*f_axis
jw = 1j*w


# get rid of the modal behaviour (keep only pistonic motion part)
f_lim = np.argmax(f_axis > 1e3)
V[f_lim:] = 0

## ----------------------------------------------- ##
# Estimation of Thiele-Small parameters - pedagogical approach
## ----------------------------------------------- ##

# electrical part

# fig, ax = plt.subplots()
# line, = ax.semilogx(f_axis, np.zeros_like(f_axis))
# ax.set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohm]')
# ax.set(xlim=(20, 1e3), ylim=(-10, 10))

# for Bl in np.arange(10, 11, .1):
#     Ze = U/I - Bl*V/I
#     line.set_ydata(np.imag(Ze))
#     ax.set(title=f"Bl = {Bl:0.1f}")
#     plt.pause(1)

# plt.show

Bl = 10.8  # [Tm] estimated from the pedagogical approach above


# electrical impedance
Ze = U/I - Bl*V/I

Re_freq = np.real(Ze)
Le_freq = np.imag(Ze)/w

# fit to Leach model
# Ze = Re + K*(jw)**beta
# Ze - Re  = K*(jw)**beta = K * w**beta * exp(j pi/2 beta)

# [Ohms] estimated from the "Resistance Re [Ohm]" graph at DC (approx)
Re = 4.9

# angle(Ze - Re) = pi/2 beta
# angle(Ze - Re) / (pi/2) =  beta

# (0.7 - 0.8) estimared from "ax.semilogx(f_axis, np.angle(Ze - Re) / (np.pi/2))" graph
beta = 0.75

# abs(Ze - Re)  = K * w**beta
# abs(Ze - Re) / w**beta  = K
# (3.5e-3 - 4.5e-3) estimated from "ax.semilogx(f_axis, np.abs(Ze - Re) / w**beta)" graph
K = 4e-3

Ze_leach = Re + K*(jw)**beta


# fig, ax = plt.subplots()
# ax.semilogx(f_axis, Re_freq, label='measured')
# ax.semilogx(f_axis, np.real(Ze_leach), label='leach model')
# ax.set(xlabel='Frequency [Hz]', ylabel='Resistance Re [Ohm]')
# ax.set(xlim=(20, 20e3))
# ax.legend()

# fig, ax = plt.subplots()
# ax.semilogx(f_axis, 1000*Le_freq, label='measured')
# ax.semilogx(f_axis, 1000*np.imag(Ze_leach)/w, label='leach model')
# ax.set(xlabel='Frequency [Hz]', ylabel='Inductance Le [mH]')
# ax.set(xlim=(20, 20e3))
# ax.legend()


# mechanical part

Zm = Bl*I/V

# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(1/Zm))
# ax.set(xlabel='Frequency [Hz]', ylabel='Mechanical admittance [m/Ns]')
# ax.set(xlim=(20, 1e3))


# mechanical losses
Rms_freq = np.real(Zm)

# fig, ax = plt.subplots()
# ax.semilogx(f_axis, Rms_freq)
# ax.set(xlabel='Frequency [Hz]', ylabel='Mechanical losses [Ns/m]')
# ax.set(xlim=(20, 1e3))

# [Ns/m] estimated from the "ax.semilogx(f_axis, Rms_freq)" graph @ the resonant frequency (164 Hz)
Rms = 2.45

# Mms and Kms

# Zm = jw*Mms + Rms + Kms/jw
# imag(Zm) = w*Mms - Kms/w
# [image Zm] = [w, -1/w] * [Mms, Kms] matrix relation


f1, f2 = np.argmax(f_axis > 100), np.argmax(f_axis > 200)

# fit Kms and Mms
A = np.array([w[f1:f2], -1/w[f1:f2]]).T
Mms, Kms = np.linalg.lstsq(A, np.imag(Zm[f1:f2]), rcond=None)[0]

# print(f"Mms = {Mms}")
# print(f"Kms = {Kms}")

# Final model

Zm_model = jw*Mms + Rms + Kms/jw
Z_model = Ze_leach + Bl**2 / Zm_model


fig, ax = plt.subplots(2)
ax[0].semilogx(f_axis, np.abs(Z))
ax[0].semilogx(f_axis, np.abs(Z_model))
ax[0].set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohm]')
ax[0].set(xlim=(20, 20e3), ylim=(0, 60))
ax[0].grid()
ax[1].semilogx(f_axis, np.angle(Z))
ax[1].semilogx(f_axis, np.angle(Z_model))
ax[1].set(xlabel='Frequency [Hz]', ylabel='Phase [rad]')
ax[1].set(xlim=(20, 20e3))
ax[1].grid()

plt.show()
