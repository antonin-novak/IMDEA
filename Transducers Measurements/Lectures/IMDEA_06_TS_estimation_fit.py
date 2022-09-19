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

# get rid of non-pistonic data
f_lim = np.argmax(f_axis > 1e3)
V[f_lim:] = 0

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(V))
ax.set(xlabel='Frequency [Hz]', ylabel='Velocity')

''' Parameters Estimation - Fitting '''
# U = Re*I + Le*jwI + Bl*V
A = np.array([I, jw*I, V]).T
Re, Le, Bl = np.linalg.lstsq(np.real(A), np.real(U), rcond=0)[0]
print(Re)
print(Le)
print(Bl)

# Bl*I = Mms*jw*V + Rms*V + Kms/(jw)*V
A = np.array([jw*V, V, V/jw]).T
Mms, Rms, Kms = np.linalg.lstsq(np.imag(A), np.imag(Bl*I), rcond=0)[0]
print(Mms)
print(Rms)
print(Kms)


''' Impedance reconstruction from the model '''
Ze = Re + Le*jw
Zm = Mms*jw + Rms + Kms/jw

Z_model = Ze + Bl**2/Zm

# plot
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(Z), label='meas. data')
ax.semilogx(f_axis, np.abs(Z_model), label='model')
ax.set(xlabel='Frequency [Hz]', ylabel='Impedance (abs) [Ohm]')
ax.legend()

plt.show()
