import numpy as np
import matplotlib.pyplot as plt

''' LOAD DATA'''
# load the data file
data = np.load('meas_data.npz')

# extract the frequency axis
f_axis = data['f_axis']

# use only useful frequencies
f1, f2 = np.argmax(f_axis > 20), np.argmax(f_axis > 20e3)
f_axis = data['f_axis'][f1:f2]
omega = 2*np.pi*f_axis
U = data['U'][f1:f2]
I = data['I'][f1:f2]
V = data['V'][f1:f2]

f_lim = np.argmax(f_axis > 2e3)
V[f_lim:] = 0  # ignore velocity above 2kHz

# plot the impedance
Z = U/I
# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(Z))
# ax.set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohm]')
# ax.set(xlim=(20, 20e3))
# ax.grid()


# estimate BL
# plt.ion()
# fig, ax = plt.subplots()
# ax.grid()
# ax.set(xlabel='Frequency [Hz]', ylabel='Re(U/I - Bl*V/I)')
# ax.set(xlim=(20, 500), ylim=(0, 10))
# for Bl in np.arange(10, 11, .1):
#     ax.plot(f_axis, np.abs (U/I - Bl*V/I))
#     ax.set(title=f"Bl = {Bl:0.2f} Tm")
#     plt.waitforbuttonpress()

# plt.ioff()


Bl = 10.8  # Tm ... estimated form previous figure

# --- Electrical part
Ze = U/I - Bl*V/I

# Leach model (see the video recording "Advanced Method - Ze" https://imdea.ant-novak.com/TM/video/CM02/)
Re = 4.92
eta = 0.8
K = 2.7e-3

Ze_model = Re + K*(1j*omega)**eta

# plot Re (np.real(Ze))
fig, ax = plt.subplots(2)
ax[0].semilogx(f_axis, np.real(Ze), label='Measured')
ax[0].semilogx(f_axis, np.real(Ze_model), '--', label='Leach model')
ax[0].set(xlabel='Frequency [Hz]', ylabel='Re(Ze) [Ohm]')
ax[0].set(xlim=(20, 20e3))
ax[0].legend()
ax[0].grid()
# plot Le (np.imag(Ze)/omega)
ax[1].semilogx(f_axis, np.imag(Ze)/omega*1000, label='Measured')
ax[1].semilogx(f_axis, np.imag(Ze_model)/omega*1000, '--', label='Leach model')
ax[1].set(xlabel='Frequency [Hz]', ylabel='Le [mH]')
ax[1].set(xlim=(20, 20e3))
ax[1].legend()
ax[1].grid()


# --- Mechanical Part
Zm = Bl*I/V

# plot abs(Zm)
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(Zm))
ax.set(xlabel='Frequency [Hz]', ylabel='|Zm| [N.s/m]')
ax.set(xlim=(20, 1e3))
ax.grid()


# Mechanical losses
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.real(Zm))
ax.set(xlabel='Frequency [Hz]', ylabel='Mechanical resistance [N.s/m]')
ax.set(xlim=(20, 400), ylim=(0, 20))
ax.grid()

# Take Rms as a constant value at the resonance frequency
Rms = 2.4  # N.s/m

# Mms and Kms
# Limit the frequency range to around the resonance frequency
fres_1, fres_2 = np.argmax(f_axis > 100), np.argmax(f_axis > 250)
B = np.array([omega[fres_1:fres_2], -1/omega[fres_1:fres_2]]).T
Mms, Kms = np.linalg.lstsq(B, np.imag(Zm[fres_1:fres_2]), rcond=None)[0]
print(f'Mms = {Mms*1000:.2f} g')
print(f'Kms = {Kms:.2f} N/m')


Zm_model = Rms + 1j*omega*Mms + Kms/(1j*omega)

# plot the mechanical admittance
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(1/Zm), label='Measured')
ax.semilogx(f_axis, np.abs(1/Zm_model), '--', label='Model')
ax.set(xlabel='Frequency [Hz]', ylabel='|1/Zm| [m/(N.s)]')
ax.set(xlim=(20, 1e3))
ax.grid()
ax.legend()

# --- Complete Model
Z_model = Ze_model + Bl**2/Zm_model

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
