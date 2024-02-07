import scipy.signal as signal
import numpy as np

# Function to generate the coefficients for a 2nd order IIR filter
# f_type: Type of the filter (Low-pass, High-pass, etc.)
# Fc: Cutoff frequency of the filter
# Q: Quality factor of the filter, representing the bandwidth at the cutoff frequency
# dBgain: Gain of the filter in decibels
# fs: Sampling frequency of the digital system


def get_filter_coefficients(f_type, Fc, Q, dBgain, fs):

    # Normalized cutoff frequency calculation
    wc = 2*np.pi*Fc/fs

    # Calculation of alpha, related to the bandwidth of the filter
    alpha = np.sin(wc)/(2*Q)

    # Linear gain calculation from decibels
    A = 10**(dBgain/40)

    # Coefficients for Low-pass filter
    if f_type == "Low-pass":

        b0 = (1 - np.cos(wc))/2
        b1 = 1 - np.cos(wc)
        b2 = (1 - np.cos(wc))/2
        a0 = 1 + alpha
        a1 = -2*np.cos(wc)
        a2 = 1 - alpha

    # Coefficients for High-pass filter
    elif f_type == "High-pass":

        b0 = (1 + np.cos(wc))/2
        b1 = -(1 + np.cos(wc))
        b2 = (1 + np.cos(wc))/2
        a0 = 1 + alpha
        a1 = -2*np.cos(wc)
        a2 = 1 - alpha

    # Coefficients for Band-pass filter
    elif f_type == "Band-pass":

        b0 = alpha
        b1 = 0
        b2 = -alpha
        a0 = 1 + alpha
        a1 = -2*np.cos(wc)
        a2 = 1 - alpha

    # Coefficients for Peaking filter
    elif f_type == "Peaking":

        b0 = 1 + alpha*A
        b1 = -2*np.cos(wc)
        b2 = 1 - alpha*A
        a0 = 1 + alpha/A
        a1 = -2*np.cos(wc)
        a2 = 1 - alpha/A

    # Coefficients for Low Shelf filter
    elif f_type == "Low Shelf":

        b0 = A*((A+1) - (A-1)*np.cos(wc) + 2*np.sqrt(A)*alpha)
        b1 = 2*A*((A-1) - (A+1)*np.cos(wc))
        b2 = A*((A+1) - (A-1)*np.cos(wc) - 2*np.sqrt(A)*alpha)
        a0 = (A+1) + (A-1)*np.cos(wc) + 2*np.sqrt(A)*alpha
        a1 = -2*((A-1) + (A+1)*np.cos(wc))
        a2 = (A+1) + (A-1)*np.cos(wc) - 2*np.sqrt(A)*alpha

    # Coefficients for High Shelf filter
    elif f_type == "High Shelf":

        b0 = A*((A+1) + (A-1)*np.cos(wc) + 2*np.sqrt(A)*alpha)
        b1 = -2*A*((A-1) + (A+1)*np.cos(wc))
        b2 = A*((A+1) + (A-1)*np.cos(wc) - 2*np.sqrt(A)*alpha)
        a0 = (A+1) - (A-1)*np.cos(wc) + 2*np.sqrt(A)*alpha
        a1 = 2*((A-1) - (A+1)*np.cos(wc))
        a2 = (A+1) - (A-1)*np.cos(wc) - 2*np.sqrt(A)*alpha

    # Coefficients for Notch filter
    elif f_type == "Notch":

        b0 = 1
        b1 = -2*np.cos(wc)
        b2 = 1
        a0 = 1 + alpha
        a1 = -2*np.cos(wc)
        a2 = 1 - alpha

    else:
        raise ValueError('The filtre type {} is incorrect'.format(f_type))

    # Return the filter coefficients normalized by a0
    b = [b0/a0, b1/a0, b2/a0]
    a = [1, a1/a0, a2/a0]

    return b, a


if __name__ == "__main__":
    fs = 48000
    b, a = get_filter_coefficients("Low-pass", Fc=1000, Q=1, dBgain=0, fs=fs)

    import matplotlib.pyplot as plt
    f_axis = np.logspace(np.log10(20), np.log10(20e3), 1000)
    _, H = signal.freqz(b, a, worN=f_axis, fs=fs)

    fig, ax = plt.subplots()
    ax.semilogx(f_axis, 20*np.log10(np.abs(H)))
    ax.set(xlim=(20, 20e3), ylim=(-60, 10))
    ax.set(xlabel='Frequency [Hz]', ylabel='Amplitude [dB]')
    ax.grid()

    plt.show()
