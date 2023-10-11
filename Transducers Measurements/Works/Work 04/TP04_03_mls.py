import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import max_len_seq
from functions.measurement_NI import measurement_NI
from TP04_00_parameters import Dev, fs, mic_sens

""" Filename of the numpy zip file """
filename = 'results_part_3/mls.npz'

""" Generate a Maximum Length Sequnce (MLS) signal"""

N_bits = 18                 # Number of bits for the MLS
L_sequence = 2**N_bits-1    # Length of the MLS sequence
N_periods = 1               # Number of periods the MLS signal will be repeated

# Generate the MLS sequence using the specified number of bits N_bits.
# The max_len_seq function returns both the MLS sequence and its state.
# We only need the sequence here ([0] extracts the sequence)
mls_sequence = max_len_seq(nbits=N_bits)[0]

# Convert the binary MLS sequence (0s and 1s) to bipolar (-1s and 1s) for audio processing
x = 2*mls_sequence-1

# Repeat the bipolar MLS signal for the N_periods periods using the numpy's tile function.
out_signal = np.tile(x, N_periods)


""" Add one second of a signal at the beginning to achieve steady state when measuring """

# If out_signal has more than fs samples, take the last fs samples
if len(out_signal) >= fs:
    one_second_signal = out_signal[-fs:]

# If out_signal has fewer than fs samples, repeat it until we have fs samples
else:
    # Compute how many times x needs to be repeated to exceed fs samples
    required_repeats = fs // len(out_signal)
    # Take only the last fs samples after tiling
    one_second_signal = np.tile(x, required_repeats+1)[-fs:]

# Concatenate one second of the signal with the repeated signal for N_periods
out_signal = np.concatenate((one_second_signal, np.tile(x, N_periods)))


""" Measurement using a National Instruments device  """
y = measurement_NI(out_signal, fs, Dev, iepe=[True])

# Extract signals from measured data (voltage)
u = np.array(y)

""" SAVE  """
np.savez(filename, u=u, x=x, N_bits=N_bits, L_sequence=L_sequence,
         N_periods=N_periods, mic_sens=mic_sens, fs=fs)


""" PLOT the results  """
fi, ax = plt.subplots()  # figure for displacement over voltage
ax.plot(u)
