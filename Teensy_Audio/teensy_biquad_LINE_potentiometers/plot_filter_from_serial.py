import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from python_functions.filters import get_filter_coefficients
import serial

SERIAL_SPEED = 9600   # Serial communication speed
SERIAL_PORT = "/dev/cu.usbmodem88092601"  # Serial port for Teensy board

# sample rate
fs = 48000

# 2nd order IIR filter
f, Q = 1000.0, 0.1  # filter frequency and quality factor
b, a = get_filter_coefficients("Low-pass", Fc=1000, Q=1, dBgain=0, fs=fs)

# Frequency Response Function
f_axis = np.logspace(np.log10(20), np.log10(20e3), 1000)
_, H = signal.freqz(b, a, worN=f_axis, fs=fs)

# prepare a graph
plt.ion()  # interactive on
fig, ax = plt.subplots()
ax.set(xlabel='Frequency [Hz]', ylabel='Filter Gain [dB]')
ax.set(xlim=(20, 20e3), ylim=(-60, 20))
ax.grid()

line1, = ax.semilogx(f_axis, 20*np.log10(np.abs(H)), 'b-')


# loop while the figure is opened
while plt.fignum_exists(fig.number):

    # Serial communication to send the coefficients in JSON format
    with serial.Serial(SERIAL_PORT, SERIAL_SPEED, timeout=1) as ser:
        line = ser.readline()     # read a '\n' terminated line
        # update variables f and Q (from serial command)
        exec(line[:-2])

    # update filter coefficients
    filter_type = "Low-pass" if type == 0 else "High-pass"
    b, a = get_filter_coefficients(filter_type, Fc=f, Q=Q, dBgain=0, fs=fs)

    # update the Frequency Response Function
    _, H = signal.freqz(b, a, worN=f_axis, fs=fs)
    line1.set_ydata(20*np.log10(np.abs(H)))

    ax.set(
        title=f'Frequency Response Function \n {filter_type} filter, f = {f:.1f} Hz, Q = {Q:.2f}')
    fig.canvas.draw()
    fig.canvas.flush_events()
