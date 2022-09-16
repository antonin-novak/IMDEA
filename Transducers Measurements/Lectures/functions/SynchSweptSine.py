import numpy as np


class SynchSweptSine():
    ''' Synchronous Swept Sine

    Description:
        The synchronized-swept-sine method is a nonlinear system
        identification that can analyze a nonlinear system in terms
        of Higher Harmonic Frequency Responses (HHFRs).

    Usage:
        sss = SynchSweptSine(f1, f2, fs, T) # !!! sss is an object
        x = sss.signal() # generates the swept-sine signal

        #                              -------
        # then do the measurement x -> | NLS | -> y
        #                              -------

        h = sss.getIR(y) # obtain the impulse response from signal y
        Hs = sss.separate_IR(h, N=3) # obtain HHFRs


    Author:
        Antonin Novak - 29.10.2021

    '''

    def __init__(self, f1=20, f2=20e3, fs=48e3, T=10, fade=[9600, 960]):
        self.f1 = f1
        self.f2 = f2
        self.fs = fs
        self.T = T
        self.fade = fade
        self.L = T/np.log(f2/f1)

    def t_axis(self):
        ''' creates the time axis '''
        return np.arange(0, np.round(self.fs*self.T-1)/self.fs, 1/self.fs)

    def signal(self):
        ''' generates the swept-sine signal '''
        t = self.t_axis()
        s = np.sin(2*np.pi*self.f1*self.L*np.exp(t/self.L))

        fade = self.fade
        # fade-in the input signal
        if self.fade[0] > 0:
            s[0:fade[0]] = s[0:fade[0]] * ((-np.cos(np.arange(fade[0])/fade[0]*np.pi)+1) / 2)

        # fade-out the input signal
        if self.fade[1] > 0:
            s[-fade[1]:] = s[-fade[1]:] * ((np.cos(np.arange(fade[1])/fade[1]*np.pi)+1) / 2)

        return s

    def f_axis(self, Npts):
        ''' creates the freuency axis '''
        return np.fft.rfftfreq(Npts, d=1.0/self.fs)

    def Xinv(self, Npts):
        ''' calculates Xinv = 1/X, where X is the Fourier Transform of the swept-sine  '''
        import warnings
        warnings.filterwarnings("ignore")
        # suppress warnings temporarily (log of zero in Xinv definition)

        # definition of the inferse filter in spectral domain
        # (Novak et al., "Synchronized swept-sine: Theory, application, and implementation."
        # Journal of the Audio Engineering Society 63.10 (2015): 786-798.
        # Eq.(43))
        f_axis = self.f_axis(Npts)
        Xinv = 2*np.sqrt(f_axis/self.L)*np.exp(-1j*2*np.pi*f_axis*self.L*(1-np.log(f_axis/self.f1)) + 1j*np.pi/4)
        Xinv[0] = 0j

        warnings.filterwarnings("default")
        return Xinv

    def getIR(self, y):
        ''' calculates the impulse repsonse from the measured signal y '''
        # FFT of the output signal
        Y = np.fft.rfft(y)/self.fs

        # complete FRF
        H = Y*self.Xinv(len(y))

        # iFFT to get IR
        return np.fft.irfft(H)

    def getFRF(self, y, N_samples=None):
        ''' Calculates the Frequency Response Function (linear one)
            of windowed impulse response.
            Usually used only for linear (or week nonlinear) systems.'''
        if N_samples == None:
            N_samples = self.fs
        h = self.getIR(y)
        return np.fft.rfft(h[:N_samples])

    def separate_IR(self, h, N=3, n_samples=2**13, latency=0):
        ''' Separates the nonlinear contributions in the impulse response h
            and calculates their Fourier Transform to get the Higher Harmonic
            Frequency Responses (HHFRs).'''
        dt = self.L*np.log(np.arange(1, N+1))*self.fs  # positions of higher orders up to N
        dt_rem = dt - np.around(dt)  # The time lags may be non-integer in samples, the non integer delay must be applied later

        shft = int(n_samples/2)  # number of samples to make an artificail delay
        h_pos = np.concatenate((h[latency:], h[0:shft + latency + n_samples - 1]))  # periodic impulse response

        # separation of higher orders
        hs = np.zeros((N, n_samples))

        w_normalized = np.fft.rfftfreq(n_samples, d=1.0/(2*np.pi))
        for k in range(N):
            hs[k, :] = h_pos[len(h)-int(round(dt[k]))-shft-1:len(h)-int(round(dt[k]))-shft+n_samples-1]
            H_temp = np.fft.rfft(hs[k, :])

            # Non integer delay application
            H_temp = H_temp * np.exp(-1j*dt_rem[k]*w_normalized)
            hs[k, :] = np.fft.irfft(H_temp)

        # Higher Harmonics
        return np.fft.rfft(hs)
