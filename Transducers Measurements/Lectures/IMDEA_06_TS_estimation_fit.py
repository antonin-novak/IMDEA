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


# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(U))
# ax.set(xlabel='Frequency [Hz]', ylabel='Voltage [V]')
# ax.set(xlim=(20, 20e3))

# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(I))
# ax.set(xlabel='Frequency [Hz]', ylabel='Current [A]')
# ax.set(xlim=(20, 20e3))

# get rid of the modal behaviour (keep only pistonic motion part)
f_lim = np.argmax(f_axis > 500)
V[f_lim:] = 0


# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(V))
# ax.set(xlabel='Frequency [Hz]', ylabel='Velocity [m/s]')
# ax.set(xlim=(20, 20e3))


## ----------------------------------------------- ##
# Estimation of Thiele-Small parameters
## ----------------------------------------------- ##

# electrical part
# U = Re*I + Le*jwI + Bl*V
A = np.array([I, jw*I, V]).T
# Re, Le, Bl = np.linalg.lstsq(np.real(A), np.real(U), rcond=None)[0]
Re, Le, Bl = np.linalg.lstsq(np.imag(A), np.imag(U), rcond=None)[0]

# print(f"Re = {Re}")
# print(f"Le = {Le}")
# print(f"Bl = {Bl}")


# Mechanical part
A = np.array([jw*V, V, V/jw]).T
Mms, Rms, Kms = np.linalg.lstsq(np.real(A), np.real(Bl*I), rcond=None)[0]
# Mms, Rms, Kms = np.linalg.lstsq(np.imag(A), np.imag(Bl*I), rcond=None)[0]

print(f"Mms = {Mms}")
print(f"Rms = {Rms}")
print(f"Kms = {Kms}")


# Impedance from the model
Ze = Re + jw*Le
Zm = Mms*jw + Rms + Kms/jw
Z_model = Ze + Bl**2 / Zm


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
