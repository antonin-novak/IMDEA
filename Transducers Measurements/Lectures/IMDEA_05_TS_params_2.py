import numpy as np
import matplotlib.pyplot as plt

with open('meas_data.npz', 'rb') as f:
    data = np.load(f)
    f_axis = data['f_axis']
    U = data['U']
    I = data['I']
    V = data['V']

# -------------------------------------------------------------------------
# Select the frequency range used for the analysis.
#
# The measurement data are restricted to the measured frequency range
# from 20 Hz to 20 kHz.
# -------------------------------------------------------------------------
f_limits = (20, 20000)
f_idx_range = (f_axis >= f_limits[0]) & (f_axis <= f_limits[1])
U = U[f_idx_range]
I = I[f_idx_range]
V = V[f_idx_range]
f_axis = f_axis[f_idx_range]


# -------------------------------------------------------------------------
# Plot the magnitude spectra of the three measured quantities:
#   - U: loudspeaker terminal voltage
#   - I: loudspeaker current, measured with a current probe
#   - V: diaphragm velocity, measured with a laser Doppler vibrometer
#
# This diagnostic plot is currently disabled. It can be uncommented when
# inspection of the measured signals is required.
# -------------------------------------------------------------------------
# fig, axs = plt.subplots(3, 1, figsize=(8, 7), sharex=True)

# axs[0].semilogx(f_axis, 20 * np.log10(np.abs(U)), label='Voltage (U)', color='blue')
# axs[0].set_ylim([-60, 0])
# axs[0].set_ylabel('Magnitude [dB re 1V]')

# axs[1].semilogx(f_axis, 20 * np.log10(np.abs(I)), label='Current (I)', color='red')
# axs[1].set_ylim([-60, -10])
# axs[1].set_ylabel('Magnitude [dB re 1A]')

# axs[2].semilogx(f_axis, 20 * np.log10(np.abs(V)), label='Velocity (V)', color='green')
# axs[2].set_xlabel('Frequency [Hz]')
# axs[2].set_ylim([-60, -10])
# axs[2].set_ylabel('Magnitude [dB re 1m/s]')

# for ax in axs:
#     ax.set_xlim([20, 20000])
#     ax.grid(True)
#     ax.legend()

# fig.tight_layout()

# Angular frequency (rad/s)
omega = 2 * np.pi * f_axis


# -------------------------------------------------------------------------
# Calculate the measured electrical impedance from the measured terminal
# voltage and current:
#
#     Z = U / I
#
# Z is complex-valued and expressed in Ohms.
# -------------------------------------------------------------------------
Z = U / I


# -------------------------------------------------------------------------
# Interactive estimation of the force factor Bl
#
# The following block can be used to inspect the electrical impedance after
# subtracting the motional contribution Bl*V/I:
#
#     Ze = Z - Bl * V / I
#
# For a suitable value of Bl, the resulting impedance should mainly
# represent the electrical voice-coil impedance. Physically, it should not
# exhibit any resonance behavior, and should be flat.
#
# -------------------------------------------------------------------------

plt.ion()
fig, ax = plt.subplots(2)
for Bl in np.arange(0, 20, 1):
    Ze = Z - Bl * V / I
    ax[0].plot(f_axis, np.real(Ze))
    ax[0].set_xlabel('Frequency [Hz]')
    ax[0].set_ylabel('Impedance [Ohm]')
    ax[0].set_xlim([20, 500])
    ax[0].set_ylim([0, 10])
    ax[0].grid(True)
    ax[0].set_title(f'Bl = {Bl:0.2f} Tm')
    ax[0].legend()

    ax[1].plot(f_axis, np.imag(Ze))
    ax[1].set_xlabel('Frequency [Hz]')
    ax[1].set_ylabel('Imaginary Part [Ohm]')
    ax[1].set_xlim([20, 500])
    ax[1].set_ylim([-2, 2])
    ax[1].grid(True)
    ax[1].legend()
    plt.waitforbuttonpress()

plt.ioff()


# Force factor estimated from the interactive inspection above.
#
# Bl is the electromechanical force factor and relates current to force
# and velocity to back-EMF:
#
#     F = Bl * I
#     e = Bl * V
#
# Units: T*m, or N/A
Bl = 10.8


# -------------------------------------------------------------------------
# Limit the frequency range over which the measured diaphragm velocity is
# used.
#
# The velocity measurement is considered reliable only up to 2.5 kHz.
# Above this frequency, V is set to zero so that the velocity-dependent
# correction does not contaminate the electrical impedance.
# -------------------------------------------------------------------------
f_max_limit = 2500
V[f_axis > f_max_limit] = 0


# -------------------------------------------------------------------------
# Estimate the purely electrical voice-coil impedance.
#
# The total measured electrical impedance contains both the
# electrical impedance of the voice coil and the motional impedance
# reflected from the mechanical system.
#
# Using the measured diaphragm velocity, the motional contribution is
# subtracted according to:
#
#     Ze = Z - Bl * V / I
#
# where:
#     Z  : measured (total) impedance [Ohm]
#     Ze : electrical voice-coil impedance [Ohm] (blocked impedance)
#     Bl : force factor [T*m]
#     V  : diaphragm velocity [m/s]
#     I  : voice-coil current [A]
# -------------------------------------------------------------------------
Ze = Z - Bl * V / I


# DC resistance of the voice coil, estimated independently from
# low-frequency measurements.
#
# Units: Ohm
Re = 4.95


# -------------------------------------------------------------------------
# Fit the Leach model to the measured electrical impedance.
#
# The Leach model accounts for the frequency-dependent electrical
# impedance of the voice coil.
#
# The Electrical_Impedance class provides the model implementation and
# returns the corresponding model impedance as a function of frequency.
# -------------------------------------------------------------------------
from functions.Electrical_Impedance import Electrical_Impedance

my_model = Electrical_Impedance(omega, Ze, Re_estimated=Re, model='Leach')
Ze_model = my_model.Ze_model(omega)


# -------------------------------------------------------------------------
# Compare the measured electrical impedance with the fitted Leach model.
#
# Top plot:
#     Real part of the electrical impedance, corresponding to the
#     apparent resistance.
#
# Bottom plot:
#     Imaginary part divided by angular frequency:
#
#         Le = Im(Ze) / omega
#
#     which gives an apparent inductance. The factor 1000 converts H
#     to mH for plotting.
# -------------------------------------------------------------------------
fig, ax = plt.subplots(2)

ax[0].semilogx(f_axis, np.real(Ze), label='Measured Ze')
ax[0].semilogx(f_axis, np.real(Ze_model), label='Leach model')
ax[0].set_xlabel('Frequency [Hz]')
ax[0].set_ylabel('Apparent Resistance [Ohm]')
ax[0].legend()
ax[0].grid(True)

ax[1].semilogx(f_axis, 1000*np.imag(Ze)/omega, label='Measured Ze')
ax[1].semilogx(f_axis, 1000*np.imag(Ze_model)/omega, label='Leach model')
ax[1].set_xlabel('Frequency [Hz]')
ax[1].set_ylabel('Apparent Inductance [mH]')
ax[1].legend()
ax[1].grid(True)


# -------------------------------------------------------------------------
# Calculate the mechanical impedance from the measured electrical current
# and diaphragm velocity.
#
# From the electromechanical force relation:
#
#     F = Bl * I
#
# and the definition of mechanical impedance:
#
#     Zm = F / V
#
# the mechanical impedance can therefore be estimated as:
#
#     Zm = Bl * I / V
#
# Zm is expressed in N.s/m.
# -------------------------------------------------------------------------
Zm = Bl * I / V


# -------------------------------------------------------------------------
# Plot the real part of the measured mechanical impedance.
#
# The real part represents the mechanical resistance. Around the
# fundamental resonance, it is expected to provide an estimate of the
# mechanical resistance Rms.
# -------------------------------------------------------------------------
fig, ax = plt.subplots()

ax.semilogx(f_axis, np.real(Zm))
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Mechanical Impedance [N.s/m]')
ax.set_xlim([20, 400])
ax.set_ylim([0, 20])
ax.grid(True)


# Mechanical resistance estimated from the measured mechanical impedance
# around the resonance frequency.
#
# Units: N.s/m
Rms = 2.45


# -------------------------------------------------------------------------
# Estimate the moving mass Mms and mechanical stiffness Kms.
#
# The mechanical impedance of the lumped loudspeaker model is:
#
#     Zm = Rms + j*omega*Mms + Kms/(j*omega)
#
# Since:
#
#     1/j = -j
#
# the imaginary part can be written as:
#
#     Im(Zm) = omega*Mms - Kms/omega
#
# Therefore, Mms and Kms can be estimated using a linear least-squares
# fit of Im(Zm) against:
#
#     [omega, -1/omega]
#
# The fit is restricted to 80-300 Hz, where the lumped mechanical model
# is considered appropriate for the present measurement.
# -------------------------------------------------------------------------
f_limits = (80, 300)
f_idx_range = (f_axis >= f_limits[0]) & (f_axis <= f_limits[1])

A = np.array([omega[f_idx_range], -1/omega[f_idx_range]]).T
Mms, Kms = np.linalg.lstsq(A, np.imag(Zm[f_idx_range]), rcond=None)[0]

print(f'Mms = {1000*Mms:0.3f} g')
print(f'Kms = {Kms:0.3f} N/m')


# -------------------------------------------------------------------------
# Construct the complete loudspeaker impedance model.
#
# The mechanical impedance is reconstructed from the estimated mechanical
# parameters:
#
#     Zm_model = Rms + j*omega*Mms + Kms/(j*omega)
#
# The mechanical impedance is then reflected into the electrical domain
# through the electromechanical coupling factor Bl:
#
#     Z_motional = Bl^2 / Zm_model
#
# Finally, the total electrical impedance is:
#
#     Z_model = Ze_model + Bl^2 / Zm_model
#
# where Ze_model is the frequency-dependent electrical voice-coil
# impedance obtained from the Leach model.
# -------------------------------------------------------------------------
Zm_model = 1j*omega*Mms + Rms + Kms/(1j*omega)
Z_model = Ze_model + Bl**2 / Zm_model


# -------------------------------------------------------------------------
# Compare the measured electrical impedance with the complete
# electromechanical model.
#
# The measured electrical impedance is obtained directly from the
# measured voltage and current:
#
#     Z_measured = U / I
#
# The comparison is shown in terms of both magnitude and phase.
# -------------------------------------------------------------------------
fig, ax = plt.subplots(2)

ax[0].semilogx(f_axis, np.abs(U/I), label='Measured')
ax[0].semilogx(f_axis, np.abs(Z_model), label='Model')
ax[0].set_ylabel('Magnitude [Ohm]')
ax[0].set_xlim([5, 40000])
ax[0].grid(True)
ax[0].legend()

ax[1].semilogx(f_axis, np.angle(U/I, deg=True), label='Measured')
ax[1].semilogx(f_axis, np.angle(Z_model, deg=True), label='Model')
ax[1].set_xlabel('Frequency [Hz]')
ax[1].set_ylabel('Phase [deg]')
ax[1].set_xlim([5, 40000])
ax[1].grid(True)


plt.show()
