import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd


# Set the audio device used for both playback and recording.
sd.default.device = ('Fireface', 'Fireface')

# Display the list of available audio devices and their corresponding
# device indices.
print(sd.query_devices())


# Generate a multi-tone test signal composed of sine waves
# logarithmically spaced between 20 Hz and 20 kHz.
fs = 48000 # Sample rate in Hz.
frequencies = np.unique(np.round(np.logspace(np.log10(20), np.log10(20e3), num=200)))   # Frequencies of the individual sine waves.
print(frequencies)

T = 3 # Duration of the test signal in seconds.
t = np.arange(0, T, 1/fs) # Time vector

# Initialize the output signal to zero.
# The individual sine waves will be added to this array.
x = np.zeros(len(t))

# Generate and sum the sine waves.
# A random phase is assigned to each frequency to reduce the effect
# of coherent phase relationships between the different components.
# It avoids beating effects and imrpoves the crest factor of the resulting multi-tone signal.
for f in frequencies:
    random_phase = np.random.rand() * 2 * np.pi # Random phase between 0 and 2π.
    x += np.sin(2 * np.pi * f * t + random_phase) # Add the sine wave at frequency f to the test signal.

# Normalize the signal so that its maximum absolute amplitude is 1.
# This prevents the generated signal from exceeding the nominal
# full-scale range of [-1, 1].
x = x / np.max(np.abs(x))


# Play the generated signal while recording the input channels
# simultaneously.
y = sd.playrec(x,           # Signal sent to the audio output.
    samplerate=fs,          # Sampling rate used for playback and recording.
    channels=2,             # Record two input channels.
    input_mapping=(1, 2),   # Select input channels
    blocking=True           # Wait for playback and recording to finish before continuing.
)


# Select the first recorded channel.
# The signal corresponds to the microphone input.
y1 = y[:, 0]

# Remove the first second of the recording.
# This is intended to exclude the initial transient and
# playback/recording latency effects before performing the FFT.
y1 = y1[fs:]


# Compute the one-sided FFT of the recorded signal.
# Division by the signal length converts the FFT to the Fourier Series
# result, while multiplication by 2 accounts for the energy that
# would otherwise be present in the corresponding negative-frequency
# components.
Y = np.fft.rfft(y1)/len(y1)*2

# Generate the frequency axis corresponding to the FFT bins.
f_axis = np.fft.rfftfreq(len(y1), 1/fs)


# Determine the FFT-bin locations corresponding to the frequencies
# used to generate the test signal. 
freq_idx = frequencies * len(y1) / fs

# Extract the complex FFT values at the selected frequency bins.
Y_idx = Y[freq_idx.astype(int)]


# Plot the magnitude spectrum of the recorded signal.
fig, ax = plt.subplots()

# Convert the FFT magnitude to dB SPL.
# 20 µPa (2e-5 Pa) is the conventional reference sound pressure
# used for SPL measurements. The additional division by sqrt(2)
# converts to RMS quantities (the reference pressure is defined in RMS terms).
ax.semilogx(f_axis, 20*np.log10(np.abs(Y/2e-5/np.sqrt(2))))

# Plot the FFT magnitudes corresponding specifically to the generated
# test frequencies. These points make it easier to identify and compare
# the response at the frequencies used in the excitation signal.
ax.semilogx(frequencies, 20*np.log10(np.abs(Y_idx/2e-5/np.sqrt(2))))

ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude')
ax.set_title('FFT of the recorded signal')
ax.set_xlim([20, 20e3])
ax.grid()


# Display the figures.
plt.show()

