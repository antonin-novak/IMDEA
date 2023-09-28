import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


def cm_to_inches(cm_tuple):
    inches_tuple = tuple(cm / 2.54 for cm in cm_tuple)
    return inches_tuple


fs = 8000   # sample rate
T = 0.1     # duration of the signal
f0 = 400    # frequency of the sine wave [Hz]

t = np.arange(0, T, 1/fs)   # time array

# Create a sine signal with a noise
x = np.sin(2*np.pi*f0*t)+0.01*np.random.randn(len(t))

# Calculate FFT of the signal
X = np.fft.rfft(x)/len(x)*2

# Generate frequency axis
f_axis = np.fft.rfftfreq(len(x), 1/fs)

# Create a figure and axes with given size (17x7 cm)
fig, ax = plt.subplots(figsize=cm_to_inches((17, 7)))
ax.plot(f_axis/1000, 20*np.log10(np.abs(X)))
ax.set(xlabel='Frequency [kHz]', ylabel='Power spectrum of Voltage [dBV]')
ax.set(xlim=(0, 3), ylim=(-70, 10))
ax.grid()

# Adjust the layout of the plot
fig.tight_layout()

# Save the figure as a jpg file
fig.savefig('fig_exported.jpg')

# Display the plot
plt.show()
