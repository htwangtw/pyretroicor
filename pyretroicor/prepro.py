"""physio data preprocessing"""

import numpy as np

def process_resp(resp, fs):
    '''
    process respiratory data
    '''
    resp_f = _smooth(resp, fs)
    resp_der = np.diff(resp_f)
    resp_der = np.append(resp_der, resp_der[-1])  # wtf
    time = np.arange(0, resp_der.shape[0])
    outliers = rolling_mad(resp_der, int(0.5 * fs))
    clean = np.interp(time, time[~outliers], resp_der[~outliers])
    return clean

def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    med = np.median(arr)
    return med, np.median(np.abs(arr - med))

def rolling_mad(a, win):
    '''
    Rolling MAD outlier detection
    '''
    outliers = []
    for i in range(win, len(a)):
        cur = a[(i - win):i]
        med, cur_mad = mad(cur)
        cur_out = cur > (med + cur_mad * 3)
        idx = list(np.arange((i - win), i)[cur_out])
        outliers += idx
    outliers = list(set(outliers))

    # turn index into boolean
    bool_outliers = np.zeros(a.shape[0], dtype=bool)
    bool_outliers[outliers] = True
    return bool_outliers


def _smooth(a, winsize):
    '''
    a: NumPy 1-D array containing the data to be smoothed
    winsize: smoothing window size needs, which must be odd number,
            as in the original MATLAB implementation
    '''

    out0 = np.convolve(a,np.ones(winsize, dtype=int),'valid') / winsize
    r = np.arange(1, winsize - 1 ,2)
    start = np.cumsum(a[: winsize - 1])[::2] / r
    stop = (np.cumsum(a[: -winsize:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))
