import numpy as np
import matplotlib.pyplot as plt

# -- import measured data
data = np.load('meas_data.npz')
print(list(data.keys()))

f_axis = data['f_axis']

f_mask = (f_axis > 20) & (f_axis < 18e3)

U = data['U'][f_mask]
I = data['I'][f_mask]
V = data['V'][f_mask]
f_axis = data['f_axis'][f_mask]

jw = 2j*np.pi*f_axis

V[f_axis > 1e3] = 0

# fig, ax = plt.subplots()
# ax.semilogx(f_axis, np.abs(V))

''' Fit the electrical part '''
A = np.array([I, jw*I, V]).T
solution_re = np.linalg.lstsq(np.real(A), np.real(U), rcond=None)[0]
solution_im = np.linalg.lstsq(np.imag(A), np.imag(U), rcond=None)[0]
Re, Le, Bl = solution_re
print('--- real solution (el part) ----')
print(f'Re = {Re:.3e}')
print(f'Le = {Le:.3e}')
print(f'Bl = {Bl:.3e}')
# Re, Le, Bl = solution_im
print('--- imag solution (el part) ----')
print(f'Re = {Re:.3e}')
print(f'Le = {Le:.3e}')
print(f'Bl = {Bl:.3e}')

print('--------------------------')

''' Fit the mechanical part '''
A = np.array([jw*V, V, V/jw]).T
solution_re = np.linalg.lstsq(np.real(A), np.real(Bl*I), rcond=None)[0]
solution_im = np.linalg.lstsq(np.imag(A), np.imag(Bl*I), rcond=None)[0]
Mms, Rms, Kms = solution_re
print('--- real solution (mech part) ----')
print(f'Mms = {Mms:.3e}')
print(f'Rms = {Rms:.3e}')
print(f'Kms = {Kms:.3e}')
# Mms, Rms, Kms = solution_im
print('--- imag solution (mech part) ----')
print(f'Mms = {Mms:.3e}')
print(f'Rms = {Rms:.3e}')
print(f'Kms = {Kms:.3e}')

Ze_model = Re + jw*Le
Zm_model = jw*Mms + Rms + Kms/jw

Z_model = Ze_model + Bl**2 / Zm_model

fig, ax = plt.subplots()
ax.semilogx(f_axis, np.abs(U/I))
ax.semilogx(f_axis, np.abs(Z_model))
ax.set(xlabel='Frequency [Hz]', ylabel='Impedance [Ohms]')
ax.grid()


plt.show()
