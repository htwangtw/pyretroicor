"""physio data preprocessing"""

import numpy as np

def process_cardiac(cardiac, fs):
    '''
    preprocess cardiac signal and get R peaks times
    '''
    # clean outliers
    cardiac = smooth(cardiac, fs)
    outliers = rolling_mad(cardiac, int(0.5 * fs))
    time = np.arange(0, cardiac.shape[0])
    clean = np.interp(time, time[~outliers], cardiac[~outliers])
    # get peaks
    peak_idx = detect_peaks(clean, mpd=int(0.5 * fs))
    return peak_idx

def zscore(x):
    m = np.mean(x)
    sd = np.std(x)
    return (x - m) / sd

def detect_peaks(x, mpd):
    # standardlize signal 
    x = zscore(x)
    dx = np.diff(x)
    # find the edges of raises (proximate peaks)
    idx = np.where((np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
    if idx[0] == 0:  # first and least location must not be peak
        idx = idx[1:]
    if idx[-1] == (x.size - 1):
        idx = idx[:-1]

    # remove peak smaller than average signal
    idx = idx[x[idx] >= 0]

    # remove peaks closer than mpd
    idx = idx[np.argsort(x[idx])][::-1]  # sort idx by peak height
    idel = np.zeros(idx.size, dtype=bool)
    for i in range(idx.size):
        if not idel[i]:
            idel = idel | (idx >= idx[i] - mpd) & (idx <= idx[i] + mpd)
            idel[i] = 0  # Keep current peak
    # remove the small peaks and sort back the indices by their occurrence
    idx = np.sort(idx[~idel])
    return idx


def process_resp(resp, fs):
    '''
    process respiratory data
    '''
    resp_f = smooth(resp, fs)
    resp_der = np.diff(resp_f)
    resp_der = np.append(resp_der, resp_der[-1])
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


def smooth(a, winsize):
    '''
    a: NumPy 1-D array containing the data to be smoothed
    winsize: smoothing window size needs, which must be odd number,
            as in the original MATLAB implementation
    '''
    winsize = int(winsize)
    if winsize % 2 != 1:
        winsize += 1
    out0 = np.convolve(a, np.ones(winsize, dtype=int),'valid') / winsize
    r = np.arange(1, winsize - 1, 2)
    start = np.cumsum(a[: winsize - 1])[::2] / r
    stop = (np.cumsum(a[: -winsize:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))