import numpy as np

#####################################################
#
# Filter functions from Will Pirkle's FX book
#
#####################################################


def one_zero_filter(samples, a0, a1):
    """ equation 9.1 - first order feed-forward filter """
    out = []
    x1 = 0

    for xn in samples:
        yn = a0 * xn + a1 * x1
        out.append(yn)
        x1 = xn

    return out


def one_pole_filter(samples, a0, b1):
    """ equation 9.2 - first order feedback filter """
    out = []
    y1 = 0

    for xn in samples:
        yn = a0 * xn - b1 * y1
        out.append(yn)
        y1 = yn

    return out


def simple_resonator_coefficients(fs, fc, q):
    """ Coefficients for Ch11 Simple Resonator """
    theta_c = 2.0 * np.pi * fc / fs
    bw = fc / q
    b2 = np.e ** (-2 * np.pi * (bw / fs))
    b1 = ((-4 * b2) / (1 + b2)) * np.cos(theta_c)
    a0 = (1 - b2) * np.sqrt(1 - ((b1 ** 2) / (4 * b2)))

    return theta_c, bw, b2, b1, a0


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


def bi_quad(signal, params):
    """ Simple biquad implementation
    :param signal: The input signal
    :param params: Filter coefficients in a list like [a0, a1, a2, b1, b2]
    :return: The filtered signal (out)
    """
    out = np.zeros(signal.shape)
    yz1 = 0
    yz2 = 0
    xz1 = 0
    xz2 = 0

    for i in range(len(signal)):
        out[i] = signal[i] + params[0] * signal[i] + params[1] * xz1 + params[2] * xz2 - \
                 params[3] * yz1 - params[4] * yz2
        yz2 = yz1
        yz1 = out[i]
        xz2 = xz1
        xz1 = signal[i]

    return out


#####################################################
#
# Utility filter classes
#
#####################################################


class DcBlocker:
    """
    DC blocking filter from https://ccrma.stanford.edu/~jos/filters/DC_Blocker.html
    Defaults to pole = 0.995 - see website for rationale.
    """
    def __init__(self):
        self.pole = 0.995
        self.x1 = 0
        self.y1 = 0
        self.output_signal = []

    def __str__(self):
        return f"pole = {self.pole}, x1 = {self.x1}, y1 = {self.y1}, out = {self.output_signal}"

    def reset(self):
        self.pole = 0.995
        self.x1 = 0
        self.y1 = 0
        self.output_signal = []

    def set_pole(self, pole):
        self.pole = pole

    def process(self, input_signal):
        for x in input_signal:
            y = x - self.x1 + self.pole * self.y1
            self.output_signal.append(y)
            self.x1 = x
            self.y1 = y

        return self.output_signal
