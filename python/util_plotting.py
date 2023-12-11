import numpy as np
from scipy.fft import fft, fftshift
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import patches


def plot_waveform(title, x_label, y_label, x, y):
    """
    Call like
        plot_waveform('My Title', 'my x label', 'my y label', t, X)
    """
    fig, ax1 = plt.subplots(1)
    ax1.set_title(title)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.plot(x, y)
    plt.tight_layout()
    plt.show()


def plot_fft_mag_phs(signal,
                     mtitle='Magnitude response', mx_label='frequencies (f)', my_label='Magnitude',
                     ptitle='Phase response', px_label='frequencies (f)', py_label='Phase',
                     width=100, fs=41000, fft_size=41000):
    """
    Call like
        plot_fft_mag_phs('freq domain', 'frequencies (f)', 'Magnitude',
                         'phase response', 'frequencies (f)', 'phase', fs, fs, X)
    """
    fig, (ax1,ax2) = plt.subplots(2)
    df = fs / fft_size                                              # frequency resolution
    X_fft = 1/fft_size * fftshift(fft(signal,fft_size))             # fft of the signal
    sample_index = np.arange(start=-fft_size//2, stop=fft_size//2)  # raw index for FFT plot
    xf = sample_index * df                                          # x-axis converted to freq
    phase = np.arctan2(np.imag(X_fft), np.real(X_fft)) * 180/np.pi
    ax1.set_title(mtitle)
    ax1.set_xlabel(mx_label)
    ax1.set_ylabel(my_label)
    ax1.stem(xf, abs(X_fft))
    ax1.set_xlim(-width,width)
    ax2.set_title(ptitle)
    ax2.set_xlabel(px_label)
    ax2.set_ylabel(py_label)
    ax2.plot(xf, phase)
    plt.tight_layout()
    plt.show()


def freqz(num, den, input_name):
    """ An attempt to recreate the output of freqz in Matlab.

        Parameters
        ----------
        num : (b) array-like
              Numerator coefficients of discrete time system
        den : (a) array-like, optional
              Denominator coefficients of discrete time system
        input_name : name on output chart
    """
    # np.seterr(divide = 'ignore')  # hide warnings related to division with 0
    w, h = signal.freqz(num, den)

    # define min and max values for the y axis
    y_phase = np.degrees(np.unwrap(np.angle(h)) * 180 / np.pi)
    mina, max_a = np.min(y_phase), np.max(y_phase)

    if np.isnan(mina):
        mina = 0.0
    if np.isnan(max_a):
        max_a = 0.0

    # determine difference between y axis actual values
    if max_a > mina:
        diff = (max_a - mina) / 5
    elif mina > max_a:
        diff = (mina - max_a) / 5
    else:
        diff = 0

    # fill the value list
    val_list = [mina]
    for x in range(1, 6):
        val_list.append(mina + diff * x)

    # define min and max values for the y-axis labels
    print("mina, mina = " + str(mina))
    if mina == 0:
        des_lower = 0
        print("mina, des_lower = 0")
    elif mina < 0:
        des_lower = -100
        print("mina, des_lower = -100")
    else:
        des_lower = 100
        print("mina, des_lower = 100")

    print("max_a, max_a = " + str(max_a))
    if max_a == 0:
        des_upper = 0
        print("max_a, des_upper = 0")
    elif max_a > 0:
        des_upper = 100
        print("max_a, des_upper = 100")
    else:
        des_upper = -100
        print("max_a, des_upper = -100")

    # fix if these values are equal - avoid 0 in yorm calc - FIX: This is probably not the right way to do this.
    if max_a == mina:
        max_a = 1
        mina = 0

    # fix if these values are equal - avoid 0 in yorm calc - FIX: This is probably not the right way to do this.
    if des_upper == des_lower:
        des_upper = 1
        des_lower = 0

    y_norm = [des_lower + (x - mina) * (des_upper - des_lower) / (max_a - mina) for x in y_phase]
    minn, max_n = np.min(y_norm), np.max(y_norm)

    if np.isnan(minn):
        minn = 0.0
    if np.isnan(max_n):
        max_n = 0.0

    # determine difference between y axis normalized values
    if max_n > minn:
        diff_n = (max_n - minn) / 5
    elif minn > max_n:
        diff_n = (minn - max_n) / 5
    else:
        diff_n = 0

    # fill the string list
    str_list = [str(int(minn))]
    for xn in range(1, 6):
        val = minn + diff_n * xn
        res = str(round(val, 2))
        str_list.append(str(res))

    # do plots
    plt.figure(figsize=(6, 2))
    plt.suptitle('Magnitude and Phase Responses - ' + str(input_name))
    plt.plot(w, 20 * np.log10(abs(h)))
    plt.xlabel(r'Normalized Frequency ($\times \pi$ rad/sample)')
    plt.ylabel(r'Magnitude (dB)', fontsize=14)
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3],
               ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"])

    plt.figure(figsize=(6, 2))
    plt.plot(w, y_phase)
    plt.xlabel(r'Normalized Frequency ($\times \pi$ rad/sample)')
    plt.ylabel(r'Phase (degrees)', fontsize=14)
    plt.grid(which='both', linestyle='-', color='grey')
    plt.xticks([0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3],
               ["0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"])
    plt.yticks(val_list, str_list)
    np.seterr(divide='warn')


def zplane(b, a):
    """ Plot the complex z-plane given a transfer function.
        Adapted from https://www.dsprelated.com/showcode/244.php
    """

    # get a figure/plot
    plt.figure(figsize=(8, 4))
    ax_zp = plt.subplot(111)
    plt.suptitle('Zeros (O) and Poles (X)')

    # create the unit circle
    uc = patches.Circle((0, 0), radius=1, fill=False, color='black', ls='dashed')
    ax_zp.add_patch(uc)

    # The coefficients are less than 1, normalize the coefficients
    if np.max(b) > 1:
        kn = np.max(b)
        b = b / float(kn)
    else:
        # kn = 1
        pass

    if np.max(a) > 1:
        kd = np.max(a)
        a = a / float(kd)
    else:
        # kd = 1
        pass

    # Get the poles and zeros
    p = np.roots(a)
    z = np.roots(b)
    # k = kn / float(kd)

    # Plot the zeros and set marker properties
    t1 = plt.plot(z.real, z.imag, 'go', ms=10)
    plt.setp(t1, markersize=10.0, markeredgewidth=1.0, markeredgecolor='k', markerfacecolor='g')

    # Plot the poles and set marker properties
    t2 = plt.plot(p.real, p.imag, 'rx', ms=10)
    plt.setp(t2, markersize=12.0, markeredgewidth=3.0, markeredgecolor='r', markerfacecolor='r')

    ax_zp.spines['left'].set_position('center')
    ax_zp.spines['bottom'].set_position('center')
    ax_zp.spines['right'].set_visible(False)
    ax_zp.spines['top'].set_visible(False)

    # set the ticks
    r = 1.5
    plt.axis('scaled')
    plt.axis([-r, r, -r, r])
    ticks = [-1, 1]
    plt.xticks(ticks)
    plt.yticks(ticks)


def plot_magnitude_spectrum(sig, title, fs, freq_ratio=0.5):
    """
    TODO: (1) need to center output around 0
          (2) need to reduce so don't see both positive and negative parts of the mirrored spectrum
          (3) consider if this will work for non-periodic data
    """
    ft = np.fft.fft(sig)
    magnitude_spectrum = np.abs(ft)
    plt.figure(figsize=(18,5))
    frequency = np.linspace(0, fs//2, len(magnitude_spectrum))
    num_frequency_bins = int(len(frequency) * freq_ratio)

    plt.plot(frequency[:num_frequency_bins], magnitude_spectrum[:num_frequency_bins])
    plt.xlabel('Frequency (Hz)')
    plt.title(title)
    plt.show()
