from unicodedata import name
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
f_lim = np.argmax(f_axis > 700)
V[f_lim:] = 0

# plot
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(Z))
ax.set(xlabel='Frequency [Hz]', ylabel='Impedance (abs) [Ohm]')

''' Bl estimation '''
fig, ax = plt.subplots()
line, = ax.semilogx(f_axis, np.zeros_like(f_axis))
ax.set(xlim=(20, 20e3), ylim=(0, 10))
for Bl in np.arange(10.6, 11, 0.1):
    Ze = Z - Bl*V/I
    line.set_ydata(np.real(Ze))
    ax.set(title=f'Bl = {Bl:.1f}')
    plt.pause(0.5)

Bl = 10.8  # Tm

''' Electrical Impedance '''

Ze = Z - Bl*V/I

''' Leach model estimation'''
Re = 4.91  # [Ohms]
beta = 0.8
K = 2.6e-3

Ze_leach = Re + K*(jw)**beta
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.angle(Ze-Re)/(np.pi/2))
# ax.semilogx(f_axis, (Ze-Re)/(jw**beta))

# Compare the Leach model with the data
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.real(Ze), label='meas. data')
ax.semilogx(f_axis, np.real(Ze_leach), label='Leach model')
ax.set(xlabel='Frequency [Hz]', ylabel='Re(f) [Ohm]')
ax.legend()

fig, ax = plt.subplots()
ax.semilogx(f_axis, 1000*np.imag(Ze)/w, label='meas. data')
ax.semilogx(f_axis, 1000*np.imag(Ze_leach)/w, label='Leach model')
ax.set(xlabel='Frequency [Hz]', ylabel='Le(f) [mH]')
ax.legend()

''' Mechanical part '''

# Mechanical impedance
Zm = Bl*I/V   # [Ns/m]
# Mechanical admittance
Ym = 1/Zm  # [m/s/N]

fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Zm)))
ax.set(title='Mechanical Impedance',
       xlabel='Frequency [Hz]', ylabel='Mech. Impedance (abs) [dB re 1 Ns/m]')


fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(Ym)))
ax.set(title='Mechanical Admittance',
       xlabel='Frequency [Hz]', ylabel='Mech. Admittance (abs) [dB re 1 m/s/N]')


''' Mechanical Resistance '''

Rms_f = np.real(Zm)

fig, ax = plt.subplots()
ax.semilogx(f_axis, Rms_f)
ax.set(title='Mechanical Resistance',
       xlabel='Frequency [Hz]', ylabel='Mech. Resistance [m/s/N]')

Rms = 2.44  # [Ns/m] estimated from Rms_f around fc


''' Mms and Kms estimation '''
f1, f2 = np.argmax(f_axis > 50), np.argmax(f_axis > 300)

A = np.array([w[f1:f2], -1/w[f1:f2]]).T
Mms, Kms = np.linalg.lstsq(A, np.imag(Zm[f1:f2]), rcond=0)[0]

# Kms = Mms*w**2 - np.imag(Zm)*w
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, Kms)


''' Impedance reconstruction from the model '''
Zm = Mms*jw + Rms + Kms/jw

Z_model = Ze_leach + Bl**2/Zm

# plot
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(Z), label='meas. data')
ax.semilogx(f_axis, np.abs(Z_model), label='model')
ax.set(xlabel='Frequency [Hz]', ylabel='Impedance (abs) [Ohm]')
ax.legend()

# plot
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.angle(Z), label='meas. data')
ax.semilogx(f_axis, np.angle(Z_model), label='model')
ax.set(xlabel='Frequency [Hz]', ylabel='Impedance (phase) [rad]')
ax.legend()

plt.show()
