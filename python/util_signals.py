import numpy as np

#####################################################
#
# Test signal functions from Will Pirkle's FX book
#
#####################################################


def nyq():
    # Nyquist - 500 samples
    res = np.ones(500) * -1
    res[::2] *= -1
    return np.asarray(res)


def half_nyq():
    # Half Nyquist - 500 samples
    res = []
    for n in range(0, 125):
        res.append(0)
        res.append(1)
        res.append(0)
        res.append(-1)
    return np.asarray(res)


def qtr_nyq():
    # Quarter Nyquist - 500 samples
    res = []
    for n in range(0, 62):
        res.append(0)
        res.append(0.707)
        res.append(1)
        res.append(0.707)
        res.append(0)
        res.append(-0.707)
        res.append(-1)
        res.append(-0.707)
    # because 62 * 8 = 496, need to add four samples to make a list of 500
    res.append(0)
    res.append(0.707)
    res.append(1)
    res.append(0.707)
    return np.asarray(res)


def impls():
    # Impulse - 500 samples
    res = np.zeros(500)
    res[1] = 1
    return np.asarray(res)


def step():
    # Step function
    res = np.ones(500)
    res[0] = 0
    return np.asarray(res)
