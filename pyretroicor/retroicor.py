import numpy as np

from pyretroicor.prepro import rolling_mad

def retroicor_cardiac(time, r_peak, M=3):
    '''
    we need documentations
    translated from matlab code

    r_peak - time of the r peaks
    time - tr time stamp?
    M - Mth order of fourier series
    '''

    # the algorithm
    num_time = len(time)
    cardiac_phase = np.zeros(num_time)
    for i, t in enumerate(time):
        closest_peak = np.abs(r_peak - t)
        peak_idx = np.where(closest_peak == np.amin(closest_peak))[0][0]
        min_left = (t - r_peak[peak_idx]) > 0  # check if the peak is the first or last

        if peak_idx == 0 and not min_left:
            t2 = r_peak[peak_idx]
            t1 = t2 - 1
        elif peak_idx == (len(r_peak) - 1) and min_left:
            t1 = r_peak[peak_idx]
            t2 = t1 + 1
        elif min_left:
            t1 = r_peak[peak_idx]
            t2 = r_peak[peak_idx + 1]
        else:
            t1 = r_peak[peak_idx - 1]
            t2 = r_peak[peak_idx]
        cardiac_phase[i] = 2 * np.pi * (t - t1) / (t2 - t1)  # Eq. 2

    regr = np.zeros((num_time, M * 2))
    for i in range(M):  # Eq. 1
        regr[:,i * 2] = np.cos((i + 1) * cardiac_phase)
        regr[:,(i * 2) + 1] = np.sin((i + 1) * cardiac_phase)

    return regr


def retroicor_respiratory(resp, fs, M=3):
    '''
    need doc
    '''
    num_time = len(resp)
    resp_phase = np.zeros(num_time)

    # Histogram-equalized transfer function between 
    # respiratory amplitude and respiratory phase
    nb = 500
    val, edges = np.histogram(resp, bins=nb)
    
    # dR/dT
    diff_resp = np.diff(resp)
    diff_resp = np.append(diff_resp, diff_resp[-1])

    time = np.arange(0, diff_resp.shape[0])
    outliers = rolling_mad(diff_resp, int(0.5 * fs))
    diff_resp = np.interp(time, time[~outliers], diff_resp[~outliers])

    for i in range(num_time):  # Eq 3
        v = diff_resp[i]
        closest_peak = np.abs(v - edges)
        edge = np.where(closest_peak == np.amin(closest_peak))[0][0]
        if (edge - v) > 0:
            edge = edge - 1
        area = np.sum(val[0: edge])
        sign_resp = np.sign(resp[i])
        if sign_resp == 0:
            sign_resp = 1
        resp_phase[i] = np.pi * area * sign_resp / num_time

    regr = np.zeros((num_time, M * 2))
    for i in range(M):  # Eq.4
        regr[:,i * 2] = np.cos((i + 1)  * resp_phase)
        regr[:,(i * 2) + 1] = np.sin((i + 1)  * resp_phase)

    return regr
