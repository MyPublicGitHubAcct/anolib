import numpy as np
from scipy import signal

#####################################################
#
# Test waveforms
#    :param fs:   sample rate
#    :param t:    time in seconds
#    :param freq: desired frequency of waveform
#
#####################################################


def wv_sine(fs, t, freq):
    """ an array of values representing a sine wave """
    samples = np.arange(t * fs) / fs
    out = np.sin(2 * np.pi * freq * samples)
    return out


def wv_cosine(fs, t, freq):
    """ an array of values representing a cosine wave """
    samples = np.arange(t * fs) / fs
    out = np.cos(2 * np.pi * freq * samples)
    return out


def wv_sawtooth(fs, t, freq):
    """ an array of values representing a sawtooth wave """
    samples = np.arange(t * fs) / fs
    out = signal.sawtooth(2 * np.pi * freq * samples)
    return out


def wv_square(fs, t, freq):
    """ an array of values representing a square wave """
    samples = np.arange(t * fs) / fs
    out = signal.square(2 * np.pi * freq * samples)
    return out


#####################################################
#
# Other test waveforms
#
#####################################################


def two_sines(fs, f1, f2, mag1, mag2, time):
    """
    Returns a signal made of two sines
    :param fs: Sampling frequency
    :param f1:  of the first sine
    :param f2: frequency of the second sine
    :param mag1: magnitude of the first sine
    :param mag2: magnitude of the second sine
    :param time: time in seconds of the returned waveform
    :return:
    """
    fs = fs
    t_lims = [0, time]
    f = [f1, f2]
    mag = [mag1, mag2]
    t = np.linspace(t_lims[0], t_lims[1], (t_lims[1] - t_lims[0]) * fs)
    y = mag[0] * np.sin(2 * np.pi * f[0] * t) + mag[1] * np.sin(2 * np.pi * f[1] * t)
    y_hat = np.fft.fft(y)
    f_cycles = np.fft.fftfreq(len(t), d=1.0 / fs)  # the frequencies in cycles
    return t, y, y_hat, f_cycles
