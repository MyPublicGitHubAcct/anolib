"""
TODO - below is the starting point for writing functions to handle things that may not be needed...
"""

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

duration = 3.0
f0 = 220
f1 = 360
fs = 48000

t = np.arange(0, duration, 1.0/float(fs))
left = np.cos(2.0 * np.pi * f0 * t)
right = np.cos(2.0 * np.pi * f1 * t)

# make 2D array
tone_y_stereo = np.vstack((left, right))

# Reshape 2D array so that the left and right are in their respective columns
tone_y_stereo = tone_y_stereo.transpose()

# write the stereo wave file
wavfile.write('python/wave-files/stereoAudio.wav', fs, tone_y_stereo)

# read teh stereo wave file
fs, data = wavfile.read('python/wave-files/stereoAudio.wav')

#  plot the results
plt.plot(t, data[:, 0], label="Left channel")
plt.plot(t, data[:, 1], label="Right channel")
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
