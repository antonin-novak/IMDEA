import numpy as np
from scipy.optimize import least_squares


class Electrical_Impedance:
    ''' 
    Model of loudspeaker Electrical Impedance

    Estimated the parameters of a selected model (Leach, R2L2, or R3L3)
    based on the provided estimated impedance and estimated Re.

    Usage
    --------------------------------------------------
    # estimated Re from DC measurement
    Re = 2.9 # [Ohms]

    # angular frequency
    omega = 2*np.pi*f_axis

    # measured blocked impedance
    # Ze = ...

    # model of the electrical impedance
    my_model = Electrical_Impedance(omega, Ze, Re_estimated=Re, model='Leach')

    # estimated parameters of Leach model
    print(my_model.params)

    # impedance from the estimated model
    Zmodel = my_model.Ze_model(omega)

    fig, ax = plt.subplots()
    ax.semilogx(f_axis, np.real(Ze))
    ax.semilogx(f_axis, np.real(Zmodel))
    ax.set(xlabel='Frequency [Hz]', ylabel='real(Ze) [Ohm]')
    --------------------------------------------------


    Attributes
    ----------
    Re : float
        estimated Re (from previous measurement)
    params: list
        list of estimated parameters corresponding to the selected model


    Methods
    -------
    costFunction(parameters, omega, Ze_measured)
        calculates the error between the model and the measured data
    Leach(omega)
        estimate the impedance from the Leach model
    R2L2Model(omega)
        estimate the impedance from the R2L2 model
    R3L3Model(omega)
        estimate the impedance from the R3L3 model

    Antonin Novak - 04.10.2022
    '''

    def __init__(self, omega, Ze_measured, Re_estimated, model, guess=False, bounds=False):

        self.Re = Re_estimated
        self.params = guess

        # select the model function
        if model == 'Leach':
            self.Ze_model = self.Leach
            self.guess = guess if guess else [1, 1]
            self.bounds = bounds if bounds else [10, 10]

        if model == 'R2L2':
            self.Ze_model = self.R2L2Model
            self.guess = guess if guess else [1e-3, 1e-3, 0.01]
            self.bounds = bounds if bounds else [10e-3, 10e-3, 10]

        if model == 'R3L3':
            self.Ze_model = self.R3L3Model
            self.guess = guess if guess else [1e-3, 1e-3, 0.1, 1e-3, 1]
            self.bounds = bounds if bounds else [1e-2, 1e-2, 10, 1e-2, 10]

        self.params = least_squares(self.costFunction,
                                    self.guess,
                                    bounds=(0, self.bounds),
                                    args=(omega, Ze_measured)).x

    def costFunction(self, parameters, omega, Ze_measured):
        self.params = parameters
        Fit = self.Ze_model(omega)
        return (np.abs(Ze_measured) - np.abs(Fit))

    def Leach(self, omega):

        s = 1j*omega

        K = self.params[0]
        beta = self.params[1]

        return self.Re + K*s**beta

    def R2L2Model(self, omega):

        s = 1j*omega

        Le = self.params[0]
        L2 = self.params[1]
        R2 = self.params[2]

        return self.Re + Le*s + s*R2*L2/(R2 + s*L2)

    def R3L3Model(self, omega):

        s = 1j*omega

        Le = self.params[0]
        L2 = self.params[1]
        R2 = self.params[2]
        L3 = self.params[3]
        R3 = self.params[4]

        return self.Re + Le*s + s*R2*L2/(R2 + s*L2) + s*R3*L3/(R3 + s*L3)
