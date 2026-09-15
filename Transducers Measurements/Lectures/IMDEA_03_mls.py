import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


# Set the audio input and output devices.
sd.default.device = ('Fireface', 'Fireface')

# Display the list of available audio devices.
print(sd.query_devices())

# Sampling frequency [Hz]
fs = 48000

# Order of the Maximum Length Sequence (MLS).
# The resulting sequence contains 2**M - 1 samples.
M = 15
N = 2**M - 1

# Initialize the MLS sequence.
# The sequence will initially contain binary values (0 and 1).
mls_sequence = np.zeros(N)

# Initialize the M-bit linear feedback shift register (LFSR).
# Starting with all ones ensures that the register does not enter
# the all-zero state, which would prevent the MLS from evolving.
shift_register = np.ones(M, dtype=bool)

# Generate the Maximum Length Sequence (MLS).
# At each iteration:
#   1. The last bit of the shift register is output.
#   2. A new feedback bit is calculated using XOR.
#   3. The register is shifted by one position.
#   4. The feedback bit is inserted at the first position.
for n in range(N):
    mls_sequence[n] = shift_register[-1]

    # Calculate the feedback bit using XOR between two taps
    # of the shift register.
    temp = shift_register[7] ^ shift_register[-1]

    # Shift all register values by one position.
    shift_register = np.roll(shift_register, 1)

    # Insert the newly calculated feedback bit at the beginning.
    shift_register[0] = temp

# Convert the binary MLS sequence {0, 1} into a bipolar sequence {-1, +1}.
# This is the form typically used for acoustic system identification.
# Another common convention is x = mls_sequence**(-1), which produces a sequence of {+1, -1} values.
x = 2*mls_sequence - 1  # convert to bipolar (-1, 1)


# Calculate the single-sided FFT of the excitation signal.
X = np.fft.rfft(x)/len(x)*2

# Create the corresponding frequency axis [Hz].
f_axis = np.fft.rfftfreq(len(x), 1 / fs)

# Plot the magnitude spectrum of the MLS excitation signal.
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(X))
ax.set_xlim([20, 20000])
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [linear]')


# Play the excitation signal and record the system response simultaneously.
# The MLS is played twice:
#   - The first sequence allows transient (+latency) effects to settle.
#   - The second sequence is used for the frequency-response calculation.
#
y = sd.playrec(np.concatenate([x, x]),  # Signal sent to the audio output (twice).
    samplerate=fs,                      # Sampling rate used for playback and recording.
    channels=2,                         # Record two input channels.
    input_mapping=(1, 2),               # Select input channels
    blocking=True                       # Wait for playback and recording to finish before continuing.
)


# Extract the first recorded channel.
y1 = y[:, 0]

# Remove the first MLS period (N samples) from the recording.
y1 = y1[N:]

# Calculate the single-sided FFT of the recorded response.
Y = np.fft.rfft(y1)/len(y1)*2

# Create the frequency axis corresponding to the recorded signal.
f_axis = np.fft.rfftfreq(len(y1), 1 / fs)

# Estimate the Frequency Response Function (FRF).
# The system FRF is obtained as the ratio between
# the recorded output spectrum Y and the excitation spectrum X:
#
#                   FRF(f) = Y(f) / X(f)
#
# This gives the complex frequency response, including both magnitude
# and phase information.
FRF = Y/X

# Plot the magnitude of the FRF in decibels.
fig, ax = plt.subplots()
ax.semilogx(f_axis, 20*np.log10(np.abs(FRF)))
ax.set_xlim([20, 20000])
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude [dB]')
ax.set_title('Frequency Response Function (FRF)')


# Calculate the impulse response by taking the inverse FFT of the FRF.
h = np.fft.irfft(FRF)

# Create the time axis corresponding to the impulse response [s].
t_axis = np.arange(len(h))/fs

# Plot the estimated impulse response.
fig, ax = plt.subplots()
ax.plot(t_axis, h)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Impulse Response [linear]')


# Display all generated figures.
plt.show()