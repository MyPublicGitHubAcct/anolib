import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#####################################################
#
# Test signal functions from Will Pirkle's FX book
#
#####################################################


def nyq():
    """ nyquist """
    out = np.ones(500) * -1
    out[::2] *= -1
    return out


def half_nyquist():
    """ half nyquist """
    out = []
    for n in range(0, 125):
        out.append(0)
        out.append(1)
        out.append(0)
        out.append(-1)
    return np.asarray(out)


def qtr_nyquist():
    """ quarter nyquist """
    out = []
    for n in range(0, 62):
        out.append(0)
        out.append(0.707)
        out.append(1)
        out.append(0.707)
        out.append(0)
        out.append(-0.707)
        out.append(-1)
        out.append(-0.707)
    # because 62 * 8 = 496, need to add four samples to make a list of 500
    out.append(0)
    out.append(0.707)
    out.append(1)
    out.append(0.707)
    return np.asarray(out)


def impls():
    """ impulse """
    out = np.zeros(500)
    out[1] = 1
    return out


def step():
    """ step function """
    out = np.ones(500)
    out[0] = 0
    return out


#####################################################
#
# Test waveforms from Will Pirkle's FX book
#
#####################################################


def wv_sine(freq, time):
    """ sine at freq for a period of time """
    return np.sin(2 * np.pi * freq * time)


def wv_cosine(freq, time):
    """ cosine at freq for a period of time """
    return np.cos(2 * np.pi * freq * time)


def wv_sawtooth(freq, time):
    """ saw at freq for a period of time """
    return signal.sawtooth(2 * np.pi * freq * time)


def wv_square(freq, time):
    """ square at freq for a period of time """
    return signal.square(2 * np.pi * freq * time)


#####################################################
#
# Functions for printing the results of something
#
#####################################################


def print_signal_function_output(title, x, y):
    """ printing function for input and output of test signal functions """
    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle(title)
    ax1.stem(x[0:10])
    ax1.set_title('input (x)')
    ax1.locator_params(axis="x", nbins=16)
    ax1.locator_params(axis="y", nbins=7)
    ax2.stem(y[0:10])
    ax2.set_title('output (y)')
    ax2.locator_params(axis="x", nbins=16)
    ax2.locator_params(axis="y", nbins=7)
    fig.tight_layout(pad=1.0)
    return ax1, ax2


#####################################################
#
# Filters from Will Pirkle's FX book & other places
#
#####################################################


def first_order_feed_forward(x, xn1, a0, a1):
    """ equation 9.1 - feed-forward filter """
    result = a0 * x + a1 * xn1
    return result


def first_order_feedback(x, yn1, a0, b1):
    """ equation 9.2 - feedback filter """
    result = a0 * x - b1 * yn1
    return result


def simple_resonator_coeffs(fs, fc, q):
    """ coeffs for Ch11 Simple Resonator """
    theta_c = 2.0 * np.pi * fc / fs
    bw = fc / q
    b2 = np.e ** (-2 * np.pi * (bw / fs))
    b1 = ((-4 * b2) / (1 + b2)) * np.cos(theta_c)
    a0 = (1 - b2) * np.sqrt(1 - ((b1 ** 2) / (4 * b2)))

    print("theta_c = " + str(theta_c))
    print("bw      = " + str(bw))
    print("b2      = " + str(b2))
    print("b1      = " + str(b1))
    print("a0      = " + str(a0))


def simple_resonator(samples, fs, fc, q):
    """ simple resonator filter """
    y = np.zeros(samples.shape)
    yz1 = 0
    yz2 = 0

    theta_c = 2.0 * np.pi * fc / fs
    bw = fc / q
    b2 = np.e ** (-2 * np.pi * (bw / fs))
    b1 = ((-4 * b2) / (1 + b2)) * np.cos(theta_c)
    a0 = (1 - b2) * np.sqrt(1 - ((b1 ** 2) / (4 * b2)))

    for i in range(len(samples)):
        y[i] = a0 * samples[i] - b1 * yz1 - b2 * yz2
        yz2 = yz1
        yz1 = y[i]

    return y


def second_order_lowpass(samples, fs, fc, q):
    """ second order LPF (kLPF2), page 271 """
    y = np.zeros(samples.shape)
    yz1 = 0
    yz2 = 0
    xz1 = 0
    xz2 = 0

    theta_c = 2.0 * np.pi * fc / fs
    d = 1.0 / q
    beta_numerator = 1.0 - ((d / 2.0) * (np.sin(theta_c)))
    beta_denominator = 1.0 + ((d / 2.0) * (np.sin(theta_c)))
    beta = 0.5 * (beta_numerator / beta_denominator)
    gamma = (0.5 + beta) * (np.cos(theta_c))
    alpha = (0.5 + beta - gamma) / 2.0

    a0 = alpha
    a1 = 2.0 * alpha
    a2 = alpha
    b1 = -2.0 * gamma
    b2 = 2.0 * beta
    c0 = 1.0
    d0 = 0.0

    for i in range(len(samples)):
        y[i] = d0 * samples[i] + c0 * (a0 * samples[i] + a1 * xz1 + a2 * xz2 - b1 * yz1 - b2 * yz2)
        yz2 = yz1
        yz1 = y[i]
        xz2 = xz1
        xz1 = samples[i]

    return y


def bi_quad(samples, params):
    """ simple biquad implementation, with 'a' in numerator
        based on https://www.earlevel.com/main/2012/11/26/biquad-c-source-code/
        params = [a0, a1, a2, b1, b2]
    """
    out = np.zeros(samples.shape)

    Xz1 = 0.0
    Xz2 = 0.0
    Yz1 = 0.0
    Yz2 = 0.0

    for i in range(len(samples)):
        yn = params[0]*samples[i] + params[1]*Xz1 + params[2]*Xz2 - params[3]*Yz1 - params[4]*Yz2
        Yz2 = Yz1
        Yz1 = yn
        Xz2 = Xz1
        Xz1 = samples[i]

    return out


def bi_quad_coeffs(kind, fc, fs, q, peak_gain):
    """ generate coefficients before calling bi_quad(samples, params)
        based on https://www.earlevel.com/main/2011/01/02/biquad-formulas/

    :param: kind (see kind_dict for kinds)
    :param: fc (corner frequency, a.k.a, cutoff)
    :param: fs (sample rate)
    :param: q (resonance, a.k.a, quality factor)
    :param: peak_gain (for shelving filters, gain @ peak)
    :return: list of coefficients for requested filter kind
    """
    kind_dict = {
        '1': 'one pole LP', '2': 'one pole HP',
        '3': 'lowpass 1p1z', '4': 'highpass 1p1z',
        '5': 'LP', '6': 'HP', '7': 'BP', '8': 'notch', '9': 'peak',
        '10': 'low_shelf', '11': 'high_shelf',
        '12': 'low_shelf 1st', '13': 'high_shelf 1st',
        '14': 'allpass', '15': 'allpass 1st'
    }

    a0, a1, a2, b1, b2 = 0, 0, 0, 0, 0

    v = np.power(10, np.abs(peak_gain) / 20)
    k = np.tan(np.pi * fc/fs)

    sqrt_two = 2 ** 2
    sqrt_v = 2 ** v

    if kind == 1:
        b1 = np.exp(-2.0 * np.pi * fc / fs)
        a0 = 1.0 - b1
        b1 = -b1
        a1 = 0
        a2 = 0
        b2 = 0
    elif kind == 2:
        b1 = -np.exp(-2.0 * np.pi * (0.5 - fc / fs))
        a0 = 1.0 + b1
        b1 = -b1
        a1 = 0
        a2 = 0
        b2 = 0
    elif kind == 3:
        norm = 1 / (1 / k + 1)
        a0 = norm
        a1 = norm
        b1 = (1 - 1 / k) * norm
        a2 = 0
        b2 = 0
    elif kind == 4:
        norm = 1 / (k + 1)
        a0 = norm
        a1 = -norm
        b1 = (k - 1) * norm
        a2 = 0
        b2 = 0
    elif kind == 5:
        norm = 1 / (1 + k / q + k * k)
        a0 = k * k * norm
        a1 = 2 * a0
        a2 = a0
        b1 = 2 * (k * k - 1) * norm
        b2 = (1 - k / q + k * k) * norm
    elif kind == 6:
        norm = 1 / (1 + k / q + k * k)
        a0 = 1 * norm
        a1 = -2 * a0
        a2 = a0
        b1 = 2 * (k * k - 1) * norm
        b2 = (1 - k / q + k * k) * norm
    elif kind == 7:
        norm = 1 / (1 + k / q + k * k)
        a0 = k / q * norm
        a1 = 0
        a2 = -a0
        b1 = 2 * (k * k - 1) * norm
        b2 = (1 - k / q + k * k) * norm
    elif kind == 8:
        norm = 1 / (1 + k / q + k * k)
        a0 = (1 + k * k) * norm
        a1 = 2 * (k * k - 1) * norm
        a2 = a0
        b1 = a1
        b2 = (1 - k / q + k * k) * norm
    elif kind == 9:
        if peak_gain >= 0:
            norm = 1 / (1 + 1 / q * k + k * k)
            a0 = (1 + v / q * k + k * k) * norm
            a1 = 2 * (k * k - 1) * norm
            a2 = (1 - v / q * k + k * k) * norm
            b1 = a1
            b2 = (1 - 1 / q * k + k * k) * norm
        else:
            norm = 1 / (1 + v / q * k + k * k)
            a0 = (1 + 1 / q * k + k * k) * norm
            a1 = 2 * (k * k - 1) * norm
            a2 = (1 - 1 / q * k + k * k) * norm
            b1 = a1
            b2 = (1 - v / q * k + k * k) * norm
    elif kind == 10:
        if peak_gain >= 0:
            norm = 1 / (1 + sqrt_two * k + k * k)
            a0 = (1 + sqrt_v * k + v * k * k) * norm
            a1 = 2 * (v * k * k - 1) * norm
            a2 = (1 - sqrt_v * k + v * k * k) * norm
            b1 = 2 * (k * k - 1) * norm
            b2 = (1 - sqrt_two * k + k * k) * norm
        else:
            norm = 1 / (1 + sqrt_v * k + v * k * k)
            a0 = (1 + sqrt_two * k + k * k) * norm
            a1 = 2 * (k * k - 1) * norm
            a2 = (1 - sqrt_two * k + k * k) * norm
            b1 = 2 * (v * k * k - 1) * norm
            b2 = (1 - sqrt_v * k + v * k * k) * norm
    elif kind == 11:
        if peak_gain >= 0:
            norm = 1 / (1 + sqrt_two * k + k * k)
            a0 = (v + sqrt_v * k + k * k) * norm
            a1 = 2 * (k * k - v) * norm
            a2 = (v - sqrt_v * k + k * k) * norm
            b1 = 2 * (k * k - 1) * norm
            b2 = (1 - sqrt_two * k + k * k) * norm
        else:
            norm = 1 / (v + sqrt_v * k + k * k)
            a0 = (1 + sqrt_two * k + k * k) * norm
            a1 = 2 * (k * k - 1) * norm
            a2 = (1 - sqrt_two * k + k * k) * norm
            b1 = 2 * (k * k - v) * norm
            b2 = (v - sqrt_v * k + k * k) * norm
    elif kind == 12:
        if peak_gain >= 0:
            norm = 1 / (k + 1)
            a0 = (k * v + 1) * norm
            a1 = (k * v - 1) * norm
            a2 = 0
            b1 = (k - 1) * norm
            b2 = 0
        else:
            norm = 1 / (k * v + 1)
            a0 = (k + 1) * norm
            a1 = (k - 1) * norm
            a2 = 0
            b1 = (k * v - 1) * norm
            b2 = 0
    elif kind == 13:
        if peak_gain >= 0:
            norm = 1 / (k + 1)
            a0 = (k + v) * norm
            a1 = (k - v) * norm
            a2 = 0
            b1 = (k - 1) * norm
            b2 = 0
        else:
            norm = 1 / (k + v)
            a0 = (k + 1) * norm
            a1 = (k - 1) * norm
            a2 = 0
            b1 = (k - v) * norm
            b2 = 0
    elif kind == 14:
        norm = 1 / (1 + k / q + k * k)
        a0 = (1 - k / q + k * k) * norm
        a1 = 2 * (k * k - 1) * norm
        a2 = 1
        b1 = a1
        b2 = a0
    elif kind == 15:
        a0 = (1 - k) / (1 + k)
        a1 = -1
        a2 = 0
        b1 = -a0
        b2 = 0

    print("kind == " + str(kind_dict[str(kind)]))

    print(
        "a0 = " + str(a0) + ", " +
        "a1 = " + str(a1) + ", " +
        "a2 = " + str(a2) + ", " +
        "b1 = " + str(b1) + ", " +
        "b2 = " + str(b2)
    )

    return [a0, a1, a2, b1, b2]
