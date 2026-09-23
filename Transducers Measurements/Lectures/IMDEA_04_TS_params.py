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
# The measured data are restricted to the measured frequency range
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
## -------------------------------------------------------------------------
fig, axs = plt.subplots(3, 1, figsize=(8, 7), sharex=True)

axs[0].semilogx(f_axis, 20 * np.log10(np.abs(U)), label='Voltage (U)', color='blue')
axs[0].set_ylim([-60, 0])
axs[0].set_ylabel('Magnitude [dB re 1V]')

axs[1].semilogx(f_axis, 20 * np.log10(np.abs(I)), label='Current (I)', color='red')
axs[1].set_ylim([-60, -10])
axs[1].set_ylabel('Magnitude [dB re 1A]')

axs[2].semilogx(f_axis, 20 * np.log10(np.abs(V)), label='Velocity (V)', color='green')
axs[2].set_xlabel('Frequency [Hz]')
axs[2].set_ylim([-60, -10])
axs[2].set_ylabel('Magnitude [dB re 1m/s]')

for ax in axs:
    ax.set_xlim([5, 40000])
    ax.grid(True)
    ax.legend()

fig.tight_layout()

# Angular frequency corresponding to each frequency sample.
omega = 2 * np.pi * f_axis

# -------------------------------------------------------------------------
# Loudspeaker electrical impedance equation
#
# The lumped-parameter electromechanical model is described by:
#
#     U = Re * I + j*omega*Le * I + Bl * V
#
# where:
#     Re : voice-coil DC resistance [Ohm]
#     Le : voice-coil inductance [H]
#     Bl : force factor [T*m]
#     I  : voice-coil current [A]
#     V  : diaphragm velocity [m/s]
#     U  : loudspeaker terminal voltage [V]
#
# The unknown parameters Re, Le, and Bl are estimated by linear
# least-squares regression using the complex measurement data.
# -------------------------------------------------------------------------

def estimate_parameters(f, U, I, V):
    """
    Estimate the loudspeaker's electrical and mechanical parameters.

    Parameters
    ----------
    f : array_like
        Frequency vector [Hz].
    U : array_like
        Measured loudspeaker terminal voltage [V].
    I : array_like
        Measured loudspeaker current [A].
    V : array_like
        Measured diaphragm velocity [m/s].

    Returns
    -------
    Re : float
        Voice-coil DC resistance [Ohm].
    Le : float
        Voice-coil inductance [H].
    Bl : float
        Electromagnetic force factor [T*m].
    Mms : float
        Moving mass [kg].
    Rms : float
        Mechanical resistance [N*s/m].
    Kms : float
        Mechanical stiffness [N/m].

    Notes
    -----
    The electrical equation is first written as a linear regression
    problem for Re, Le, and Bl. The real and imaginary parts
    of the complex equations are stacked before solving to obtain 
    a real-valued parameters.

    The estimated Bl is then used in the mechanical equation to estimate
    Mms, Rms, and Kms.
    """
    omega = 2 * np.pi * f

    # Electrical equivalent-circuit model:
    #
    #     U = Re*I + j*omega*Le*I + Bl*V
    #
    # Construct the matrix for the three unknown electrical
    # parameters [Re, Le, Bl].
    A = np.array([I, 1j*omega*I, V]).T

    # Convert the complex least-squares problem into an equivalent
    # real-valued problem by stacking real and imaginary components.
    A_stack = np.vstack([A.real, A.imag])
    U_stack = np.hstack([U.real, U.imag])

    Re, Le, Bl = np.linalg.lstsq(A_stack, U_stack, rcond=None)[0]

    print(f'Re = {Re:.4f} Ohm')
    print(f'Le = {1000*Le:.4f} mH')
    print(f'Bl = {Bl:.4f} T*m')

    # ---------------------------------------------------------------------
    # Mechanical equivalent-circuit model
    #
    # The force balance is written as:
    #
    #     Bl*I = j*omega*Mms*V + Rms*V + Kms/(j*omega)*V
    #
    # where:
    #     Mms : moving mass [kg]
    #     Rms : mechanical resistance [N*s/m]
    #     Kms : mechanical stiffness [N/m]
    #
    # With Bl known from the electrical fit, the equation is linear in
    # Mms, Rms, and Kms and can therefore be solved by least squares.
    # ---------------------------------------------------------------------
    B = np.array([1j*omega*V, V, V/(1j*omega)]).T
    Bl_I = Bl * I

    # As above, convert the complex regression problem into a real-valued
    # least-squares problem by stacking real and imaginary components.
    B_stack = np.vstack([B.real, B.imag])
    Bl_I_stack = np.hstack([Bl_I.real, Bl_I.imag])

    Mms, Rms, Kms = np.linalg.lstsq(B_stack, Bl_I_stack, rcond=None)[0]

    print(f'Mms = {1000*Mms:.4f} g')
    print(f'Rms = {Rms:.4f} N*s/m')
    print(f'Kms = {Kms:.4f} N/m')

    return Re, Le, Bl, Mms, Rms, Kms


def Z_model_func(f, Re, Le, Bl, Mms, Rms, Kms):
    """
    Calculate the loudspeaker electrical impedance from the lumped model.

    Parameters
    ----------
    f : array_like
        Frequency vector [Hz].
    Re : float
        Voice-coil DC resistance [Ohm].
    Le : float
        Voice-coil inductance [H].
    Bl : float
        Electromagnetic force factor [T*m].
    Mms : float
        Moving mass [kg].
    Rms : float
        Mechanical resistance [N*s/m].
    Kms : float
        Mechanical stiffness [N/m].

    Returns
    -------
    Z_model : ndarray
        Complex electrical impedance predicted by the loudspeaker model
        [Ohm].

    Notes
    -----
    The model consists of the electrical voice-coil impedance in series
    with the motional impedance reflected into the electrical domain:

        Ze = Re + j*omega*Le

        Zm = Rms + j*omega*Mms + Kms/(j*omega)

        Z = Ze + Bl^2/Zm
    """
    omega = 2 * np.pi * f

    Ze_model = Re + 1j*omega*Le
    Zm_model = Rms + 1j*omega*Mms + Kms/(1j*omega)
    Z_model = Ze_model + Bl**2 / Zm_model

    return Z_model


# -------------------------------------------------------------------------
# Parameter estimation over the complete measurement frequency range.
# This provides an initial estimate using all available data between
# 20 Hz and 20 kHz. The estimated parameters are wrong for several reasons:
#   - The lumped-parameter model is not valid at high frequencies.
#   - The measured data are spaced linearly in frequency, which gives more 
#     weight to high-frequency data.
#.  - Since the high-frequency data are more numerous, the least-squares fit
#     is dominated by the high-frequency data, which are not well represented
#     by the lumped-parameter model (modal behavior).
# -------------------------------------------------------------------------
Re, Le, Bl, Mms, Rms, Kms = estimate_parameters(f_axis, U, I, V)
Z_model = Z_model_func(f_axis, Re, Le, Bl, Mms, Rms, Kms)


# -------------------------------------------------------------------------
# Parameter estimation using frequencies up to 1 kHz.
# Restricting the fitting range can reduce the influence of high-frequency
# effects that are not represented by the simple lumped-parameter model.
# -------------------------------------------------------------------------
f_max_limit = 1000
f_idx_limit = (f_axis <= f_max_limit)
U_lim = U[f_idx_limit]
I_lim = I[f_idx_limit]
V_lim = V[f_idx_limit]
f_axis_lim = f_axis[f_idx_limit]

Re, Le, Bl, Mms, Rms, Kms = estimate_parameters(f_axis_lim, U_lim, I_lim, V_lim)
Z_model = Z_model_func(f_axis, Re, Le, Bl, Mms, Rms, Kms)


# -------------------------------------------------------------------------
# Parameter estimation restricted to the 80-320 Hz band.
#
# This frequency interval is selected around the loudspeaker's
# fundamental resonance, where the lumped mechanical model is expected
# to fit the measured data well. The resonance frequency was observed to be 
# around 160 Hz. The selected frequency range is therefore approximately 
# one octave below and above the resonance frequency.
# -------------------------------------------------------------------------
f_max_limits = (80, 320)
f_idx_limit = (f_axis >= f_max_limits[0]) & (f_axis <= f_max_limits[1])
U_lim = U[f_idx_limit]
I_lim = I[f_idx_limit]
V_lim = V[f_idx_limit]
f_axis_lim = f_axis[f_idx_limit]

Re, Le, Bl, Mms, Rms, Kms = estimate_parameters(f_axis_lim, U_lim, I_lim, V_lim)

print('----------------------')
print(f'Le = {1000*Le:.4f} mH')

# Override the fitted inductance with a fixed value for the final
# impedance-model comparison.
Le = 0.25e-3

Z_model = Z_model_func(f_axis, Re, Le, Bl, Mms, Rms, Kms)


# -------------------------------------------------------------------------
# Compare the measured electrical impedance with the impedance predicted
# by the estimated lumped-parameter model.
#
# The measured impedance is obtained directly from the measured voltage
# and current:
#
#     Z_measured = U / I
#
# Both magnitude and phase are plotted as a function of frequency.
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
