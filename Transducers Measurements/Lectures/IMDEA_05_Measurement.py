import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from functions.SynchSweptSine import SynchSweptSine

''' sample rate '''
fs = 48000  # [Hz]

''' Sensitivities '''
sound_card_sensitivity = 10   # V/units
voltage_sensitivuty = 1/1.014  # V/V
current_sensitivuty = 1/9.28  # A/V
velocity_sensitivuty = 25e-3  # m/s / V

''' Devices (Sounddevice) '''
print(sd.query_devices())
sd.default.device = (6, 6)

''' Synchronized Swept-Sine signal '''
sss = SynchSweptSine(f1=5, f2=22e3, fs=fs, T=5, fade=[int(fs), int(fs/10)])
x = np.concatenate((sss.signal(), np.zeros(15000)))

''' Playing and Recording '''
y = sound_card_sensitivity * sd.playrec(0.8*x,  # input signal
                                        samplerate=fs,
                                        channels=3,
                                        input_mapping=(8, 7, 6),
                                        output_mapping=(9),
                                        blocking=True)

# extract the signals
latency = 9400
u = voltage_sensitivuty * y[latency:, 0]  # voltage [V]
i = current_sensitivuty * y[latency:, 1]  # current [A]
v = velocity_sensitivuty * y[latency:, 2]  # velocity [m/s]

''' Synchronized Swept-Sine signal, FRF extraction'''
u_ir = sss.getIR(u)
i_ir = sss.getIR(i)
v_ir = sss.getIR(v)

U = np.fft.rfft(u_ir[:fs])
I = np.fft.rfft(i_ir[:fs])
V = np.fft.rfft(v_ir[:fs])
f_axis = np.fft.rfftfreq(fs, 1/fs)


''' Plot '''
fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U))
ax.set(title='Voltage Spectrum',
       xlabel='Frequency [Hz]', ylabel='[V/Hz]')
ax.set(xlim=(20, 20e3))

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(I))
ax.set(title='Current Spectrum',
       xlabel='Frequency [Hz]', ylabel='[A/Hz]')
ax.set(xlim=(20, 20e3))

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(V))
ax.set(title='Velocity Spectrum',
       xlabel='Frequency [Hz]', ylabel='[m/s / Hz]')
ax.set(xlim=(20, 20e3))

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U/I))
ax.set(title='Impedance',
       xlabel='Frequency [Hz]', ylabel='[Ohm]')
ax.set(xlim=(20, 20e3), ylim=(0, 50))

''' Save results '''
np.savez('meas_data.npz', f_axis=f_axis, fs=fs, U=U, I=I, V=V)

plt.show()
