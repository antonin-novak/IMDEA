import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

# 0 dBV ... 1 Vrms
# 0 dBu ... (1mW .. 600 Ohm) => U = sqrt(P*R) = sqrt(0.6) = 0.775 Vrms
# 0 dBFS ... Full Scale (-1 ... +1)

# Output Line Level (Hi Gain) ... +19 dBu ... 6.904 Vrms ... 9.763 V
# Output Line Level (+4 dBu) ...  +13 dBu ... 3.456 Vrms ... 4.893 V
# Output Line Level (-10 dBV) ...  +2 dBV ... 1.259 Vrms ... 1.780 V

# Input Line Level (Lo Gain) ... +19 dBu ... 6.904 Vrms ... 9.763 V
# Input Line Level (+4 dBu) ...  +13 dBu ... 3.456 Vrms ... 4.893 V
# Input Line Level (-10 dBV) ...  +2 dBV ... 1.259 Vrms ... 1.780 V

''' Output and Input sensitivities (calibrated) '''
output_sensitivity = 1.22*np.sqrt(2)  # units / Volt
input_sensitivity = 10  # Volts / unit

''' sample rate '''
fs = 48000  # [Hz]

''' Devices (Sounddevice) '''
print(sd.query_devices())
sd.default.device = (6, 6)

''' Sine-wave '''
f0 = 500  # [Hz]
T = 5  # duration of sine wave [s]
t = np.arange(0, T*fs) / fs

A = np.sqrt(2)  # [V]
x = A*np.sin(2*np.pi * f0 * t)

''' Playing and Recording '''
y = sd.playrec(0*x / output_sensitivity,  # input signal
               samplerate=fs,
               channels=1,
               input_mapping=(5),
               blocking=True)


# extract the 1st channel
# taking just the last 1 second (fs samples)
y = input_sensitivity * y[int(-fs):, 0]

''' Plot '''
fig, ax = plt.subplots()
ax.plot(y)
ax.set(title=np.std(y))

plt.show()
