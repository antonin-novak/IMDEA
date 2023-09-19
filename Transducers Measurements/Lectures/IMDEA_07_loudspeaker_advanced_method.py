import numpy as np
import matplotlib.pyplot as plt

# -- import measured data
data = np.load('meas_data.npz')
print(list(data.keys()))

f_axis = data['f_axis']

# limit the data between 20 Hz and 18 kHz
f_mask = (f_axis > 20) & (f_axis < 18e3)

U = data['U'][f_mask]
I = data['I'][f_mask]
V = data['V'][f_mask]
f_axis = data['f_axis'][f_mask]

w = 2*np.pi*f_axis
jw = 1j*w

# Get rid of high frequencies for the velocity
# There are modes => non-pistonic motion
V[f_axis > 2.5e3] = 0

''' Bl estimation '''
fig, ax = plt.subplots()
for Bl in np.arange(10, 12, 0.2):
    Ze = U/I - Bl*V/I
    ax.semilogx(f_axis, np.real(Ze), label=f'Bl = {Bl:.2f}')
ax.set(xlim=(50, 400), ylim=(0, 50))
ax.legend()
ax.grid()

# estimated value of Bl from the previous loop
Bl = 10.8  # Tm

''' Electrical impedance '''
Ze = U/I - Bl*V/I

''' Fit the Leach model '''
# Ze_Leach = Re + K*(jw)**beta
Re = 4.92
# Ze_Leach - Re = K*(jw)**beta
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.angle(Ze - Re)/(np.pi/2))
beta = 0.8
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(Ze - Re)/(w**beta))
K = 2.7e-3

Ze_Leach = Re + K*(jw)**beta


fig, ax = plt.subplots()
ax.semilogx(f_axis, np.real(Ze))
ax.semilogx(f_axis, np.real(Ze_Leach))
ax.set(xlabel='Frequency [Hz]', ylabel='Resistance [Ohms]')

fig, ax = plt.subplots()
ax.semilogx(f_axis, 1000*np.imag(Ze)/w)
ax.semilogx(f_axis, 1000*np.imag(Ze_Leach)/w)
ax.set(xlabel='Frequency [Hz]', ylabel='Inductance [mH]')


''' Mechanical impedance '''
f_axis = data['f_axis']
f_mask = (f_axis > 100) & (f_axis < 200)

U = data['U'][f_mask]
I = data['I'][f_mask]
V = data['V'][f_mask]
f_axis = data['f_axis'][f_mask]
w = 2*np.pi*f_axis

Zm = Bl*I/V

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.real(Zm))
ax.set(xlabel='Frequency [Hz]', ylabel='Mechanical losses [Ns/m]')

''' Kms and Mms '''
# imag(Zm) = Mms*w - Kms/w
A = np.array([w, -1/w]).T
solution = np.linalg.lstsq(A, np.imag(Zm), rcond=None)[0]
Mms, Kms = solution
print(f'Mms = {Mms:.3e}')
print(f'Kms = {Kms:.3e}')

# ''' Different way of estimating Kms, Mms '''
# fig, ax = plt.subplots()
# for Mms in np.arange(10, 12, 0.2):
#     Kms = w**2 * Mms/1000 - w * np.imag(Zm)
#     ax.semilogx(f_axis, Kms, label=f'Mms = {Mms:.2f}')
# ax.set(xlim=(20, 400))
# ax.legend()
# ax.grid()


''' MODELING '''
f_axis = data['f_axis']
f_mask = (f_axis > 20) & (f_axis < 18e3)

U = data['U'][f_mask]
I = data['I'][f_mask]
V = data['V'][f_mask]
f_axis = data['f_axis'][f_mask]

w = 2*np.pi*f_axis
jw = 1j*w

Rms = 2.45  # estimated from the Mechanical losses graph (near fres)

Le = 1e-3  # inductance [H] estimated from the graph (LF)
Le = 0.2e-3  # inductance [H] estimated from the graph (HF)
Ze_TS = Re + jw*Le
Ze_Leach = Re + K*(jw)**beta
Zm_model = Mms*jw + Rms + Kms/jw

# TS model
Z_model = Ze_TS + Bl**2 / Zm_model

# model with Leach el. model
Z_model = Ze_Leach + Bl**2 / Zm_model

fig, ax = plt.subplots(2, 1)
ax[0].semilogx(f_axis, np.abs(U/I))
ax[0].semilogx(f_axis, np.abs(Z_model))
ax[0].set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohms]')
ax[0].grid()
ax[1].semilogx(f_axis, np.angle(U/I))
ax[1].semilogx(f_axis, np.angle(Z_model))
ax[1].set(xlabel='Frequency [Hz]', ylabel='Impedance (angle) [rad]')
ax[1].grid()

plt.show()
