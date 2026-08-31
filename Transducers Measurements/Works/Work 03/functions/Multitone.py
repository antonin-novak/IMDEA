import numpy as np


class Multitone:
    ''' 
    Multitone Signal for FRF measurement

    A multitone signal allows to measure the Device Under Test (DUT)
    over a range of frequencies with a single measurement. The multitone
    consists of N integer frequencies logarithmically spaced between
    the defined frequencies f1 and f2. The time-length of the signal must be
    an at least two seconds. At least one second is omitted from the signal
    to deal with the latency of the system at to let the DUT to come to
    a steady state.


    Usage
    ----------
    # create the Multitone object
    multitone = Multitone(f1=20, f2=20e3, N=100, T=3, fs=fs)

    # multitone.frequencies contains the array of freqencies

    # generate the multitone signal
    x = multitone.signal

    #                              -------
    # then do the measurement x -> | DUT | -> y
    #                              -------

    # get the output spectra relative to the input signal
    # (FRF-like between fft(y)/fft(x) provided onl)
    # Hy has the same size as multitone.frequencies
    Hy = multitone.extract_spectra(y)


    Attributes
    ----------
    f1 : float
        start frequency
    f2 : float
        end frequency
    N : int
        number of frequencies
    T : float
        length of the signal (in seconds)
    fs : int
        sample rate
    frequencies : numpy array
        integer frequencies
    random_phase : numpy array
        random phase of each frequency


    Methods
    ----------
    set_frequencies()
        set the actual frequencies
    extract_spectra(y)
        get the spectra of the output signal y relative to input signal
        (similar to FRF = Y/X)

    Antonin Novak - 04.10.2022
    '''

    def __init__(self, f1=20, f2=20e3, N=100, T=2, fs=48000, Tx=1):
        """
        Parameters
        ----------
        f1 : float
            start frequency
        f2 : float
            end frequency
        N : int
            number of frequencies
        T : float
            length of the signal (in seconds)
        fs : int
            sample rate
        Tx : int
            length of the signal to calculate the 
            (T-Tx) is removed from the beginning of signal

        """
        if not isinstance(Tx, int):
            raise TypeError(f"Tx must be an integer.")

        if (Tx > T):
            raise ValueError("Time T must be longer than time Tx")

        self.f1 = f1  # start frequency
        self.f2 = f2
        self.T = T
        self.N = N
        self.fs = fs
        self.frequencies = self.set_frequencies()
        self.random_phase = 2*np.pi*np.random.rand(len(self.frequencies))
        self.Tx = Tx

    def set_frequencies(self):
        # creat the frequencies
        f1_log = np.log10(self.f1)
        f2_log = np.log10(self.f2)
        frequencies = np.logspace(f1_log, f2_log, self.N, endpoint=True)
        return np.unique(np.round(frequencies)).astype(np.uint)

    @property
    def signal(self):
        t = np.arange(0, self.T, 1/self.fs)
        x = np.zeros(int(self.T*self.fs))
        for f0, random_phase in zip(self.frequencies, self.random_phase):
            x += np.sin(2*np.pi*f0*t + random_phase)

        # return normalized signal
        return x / np.max(np.abs(x))

    def extract_spectra(self, y):

        # full output spectra
        y = y[-self.Tx*self.fs:]
        Yall = np.fft.rfft(y)/len(y)*2

        # full input spectra
        x = self.signal[-self.Tx*self.fs:]
        Xall = np.fft.rfft(x)/len(x)*2

        X = Xall[self.Tx*self.frequencies]
        Y = Yall[self.Tx*self.frequencies]

        return Y/X
