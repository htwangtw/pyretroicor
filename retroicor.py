import numpy as np

def retroicor_cardiac(time, r_peak, M):
    '''
    we need documentations
    translated from matlab code

    r_peak - time of the r peaks
    time - tr time stamp?
    M - ??????
    '''

    # need comments
    num_vol = len(time)
    cardiac_phase = np.zeros(num_vol)
    for i, t in enumerate(time):
        closest_peak = np.abs(r_peak - t)
        peak_idx = np.where(closest_peak == np.amin(closest_peak))[0]

        min_left = (t - r_peak[peak_idx]) > 0  # check if the peak is the first or last
        if peak_idx == 0 and not min_left:
            t2 = r_peak[min_left]
            t1 = t2 - 1
        elif peak_idx == (length(r_peak) - 1) and min_left:
            t1 = r_peak[min_left]
            t2 = t1 + 1
        elif min_left:
            t1 = r_peak[min_left]
            t2 = r_peak[min_left + 1]
        else:
            t1 = r_peak[min_left - 1]
            t2 = r_peak[min_left]

        cardiac_phase[i] = 2 * np.pi * (t - t1) / (t2 - t1) # Eq 2

    regr = np.zeroes(num_vol, M * 2)
    for i in range(M):
        regr[:,i * 2 + 1] = np.cosin(i * cardiac_phase)
        regr[:, (i + 1) * 2] = np.sin(i * cardiac_phase)

    return regr


def retroicor_cardiac(resp_f, M, fs):
    '''
    need doc
    '''
    nt = len(resp_f)
    resp_phase = np.zeros(nt)

    resp_f = _smooth(resp_f, fs)
    resp_der = np.diff(resp_f)
    resp_der = np.append(resp_der, resp_der[-1])  # wtf
    time = np.arange(0, resp_der.shape[0])

    # outliers fill method - linear; moving method - median absolute deviation, window size 0.5 * fs?
    outliers = rolling_mad(resp_der, int(0.5 * fs))
    clean = np.interp(time, time[~outliers], resp_der[~outliers])

    nb = 500
    val, edges = np.histogram(resp_f, bins=nb)

    for i in range(nt):
        v = resp_f[i]
        closest_peak = np.abs(v - t)
        edge = np.where(closest_peak == np.amin(closest_peak))[0]
        if (edge - v) > 0:
            edge = edge - 1
        area = np.sum(val[0:edge])
        sign_resp = np.sign(resp_der[i])
        if sign_resp == 0:
            sign_resp = 1
        resp_phase[i] = np.pi * area * sign_resp / nt

    regr = np.zeroes(num_vol, M * 2)
    for i in range(M):
        regr[:,i * 2 + 1] = np.cosin(i * resp_phase)
        regr[:, (i + 1) * 2] = np.sin(i * resp_phase)

    return regr

def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    med = np.median(arr)
    return med, np.median(np.abs(arr - med))

def rolling_mad(a, win):
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

