# import the modules
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# set the device numbers (input, output)
sd.default.device = (5, 5)

# show list of devices
print(sd.query_devices())

# play and record simultaneously
y = sd.playrec(x,  # x is the signal to play
               samplerate=48000,
               channels=2,
               output_mapping=(1),
               input_mapping=(7, 8),  # input channels 7 and 8
               blocking=True  # wait until playback is finished
               )
