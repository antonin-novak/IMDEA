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
omega = 2*np.pi*f_axis
U = data['U'][f1:f2]
I = data['I'][f1:f2]
V = data['V'][f1:f2]

f_lim = np.argmax(f_axis > 1e3)
V[f_lim:] = 0  # ignore velocity above 1kHz

# plot the measurement data
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U))
ax.set(xlabel='Frequency [Hz]', ylabel='Voltage [V]')
ax.set(xlim=(20, 20e3))

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(I))
ax.set(xlabel='Frequency [Hz]', ylabel='Current [A]')
ax.set(xlim=(20, 20e3))

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(V))
ax.set(xlabel='Frequency [Hz]', ylabel='Velocity [m/s]')
ax.set(xlim=(20, 20e3))


# ---- Fit the parameters
# -- Electrical part
# U = Re * I + Le * jw * I + Bl * V
#
# matrix form: [U] = [A] * [parameters]
# split the real and imaginary part and stack them
A = np.vstack([np.real(np.array([I, 1j*omega*I, V]).T),
               np.imag(np.array([I, 1j*omega*I, V]).T)])
U_comb = np.hstack([np.real(U), np.imag(U)])

# estimate Re, Le, and Bl using least squares
Re, Le, Bl = np.linalg.lstsq(A, U_comb, rcond=None)[0]

# print the estimated parameters
print(f'Re = {Re:.2f} Ohm')
print(f'Le = {1000*Le:.2f} mH')
print(f'Bl = {Bl:.2f} N.s/m')

# -- Mechanical part
# Bl*I = Mms * jw * V + Rms * V + Kms * 1/(jw) * V
# Limit the frequency range to around the resonance frequency
fres_1, fres_2 = np.argmax(f_axis > 100), np.argmax(f_axis > 250)
V_res = V[fres_1:fres_2]  # frequency limited velocity
I_res = I[fres_1:fres_2]  # frequency limited current
# frequency limited angular frequency
omega_res = 2 * np.pi * f_axis[fres_1:fres_2]

# matrix form: [Bl*I] = [B] * [parameters]
B = np.vstack([np.real(np.array([1j*omega_res*V_res, V_res, V_res/(1j*omega_res)]).T),
               np.imag(np.array([1j*omega_res*V_res, V_res, V_res/(1j*omega_res)]).T)])
I_comb = np.hstack([np.real(I_res), np.imag(I_res)])

# estimate Mms, Rms, and Kms using least squares
Mms, Rms, Kms = np.linalg.lstsq(B, Bl*I_comb, rcond=None)[0]

# print the estimated parameters
print(f'Mms = {Mms*1000:.2f} g')
print(f'Rms = {Rms:.2f} N.s/m')
print(f'Kms = {Kms:.2f} N/m')


# ---- Model reconstruction and comparison
Z = U/I  # measured impedance

# Parameters estimated for f1 = 50 Hz, f2 = 300 Hz
Re = 5.11
Le = 0.61/1000
Bl = 10.87
Mms = 10.78/1000
Rms = 2.52
Kms = 11079.49

# Model
Z_model = Re + 1j*omega*Le + (Bl**2) / (1j*omega*Mms + Rms + Kms/(1j*omega))

# Plot the results
fig, ax = plt.subplots(2)
ax[0].semilogx(f_axis, np.abs(Z), label='Measured')
ax[0].semilogx(f_axis, np.abs(Z_model), label='Model')
ax[0].set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohm]')
ax[0].legend()
ax[0].grid()

ax[1].semilogx(f_axis, np.angle(Z, deg=True), label='Measured')
ax[1].semilogx(f_axis, np.angle(Z_model, deg=True), label='Model')
ax[1].set(xlabel='Frequency [Hz]', ylabel='Phase [deg]')
ax[1].legend()
ax[1].grid()

plt.show()
