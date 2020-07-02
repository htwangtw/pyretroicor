"""physio data preprocessing"""

import numpy as np

from scipy import signal
from scipy import interpolate
from scipy.ndimage import median_filter


def process_cardiac(cardiac, fs):
    '''
    preprocess cardiac signal and get R peaks times
    the peak detection will be used to calculate rr interval 
    so it doesn't need to be too precise.
    '''
    # use 2.5 hz window (~=150 bpm) for peak detection
    win_hz = 2.5
    win_unit = int(fs / win_hz)

    # butter bandpass filter
    sos = signal.butter(2, [0.3, 10], 'bandpass',  fs=fs, output='sos')
    cardiac = signal.sosfilt(sos, zscore(cardiac))

    # linear detrend
    cardiac = signal.detrend(zscore(cardiac))

    # despike with median filter
    cardiac = median_filter(cardiac, int(win_unit / 5))

    # clean outliers > 2.5 SD
    outliers = np.abs(zscore(cardiac)) > 2.5
    time = np.arange(0, cardiac.shape[0]) * 1 / fs
    f = interpolate.interp1d(time[~outliers], 
                             cardiac[~outliers], 
                             "cubic", fill_value="extrapolate")
    cardiac_clean = f(time)  # update

    # get peaks
    peak_idx = detect_peaks(cardiac_clean, mpd=win_unit)
    peak_t = time[peak_idx] 

    return peak_idx, peak_t

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
    # idx = idx[x[idx] >= -1]

    # remove peaks closer than minimum peak distance (unit: sample)
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
    # low pass filter
    sos = signal.butter(2, 5, 'low',  fs=fs, output='sos')
    resperation = signal.sosfilt(sos, zscore(resperation))
    # linear detrend
    resp = signal.detrend(zscore(resperation))

    # despike with median filter
    resp = median_filter(resp, int(win_unit / 5))

    # clean outliers > 2.5 SD
    outliers = np.abs(zscore(resp)) > 2.5
    time = np.arange(0, resp.shape[0]) * 1 / fs
    f = interpolate.interp1d(time[~outliers], 
                             resp[~outliers], 
                             "cubic", fill_value="extrapolate")
    resp = f(time)  # update
    return resp


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

def lowpass_smooth(a, winsize):
    '''
    a: NumPy 1-D array containing the data to be smoothed
    winsize: smoothing window size needs, which must be odd number,
            as in the original MATLAB implementation
    '''
    winsize = int(winsize)
    if winsize % 2 != 1:  # the window must be a odd number
        winsize += 1
    out0 = np.convolve(a, np.ones(winsize, dtype=int),'valid') / winsize
    r = np.arange(1, winsize - 1, 2)
    start = np.cumsum(a[: winsize - 1])[::2] / r
    stop = (np.cumsum(a[: -winsize:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))