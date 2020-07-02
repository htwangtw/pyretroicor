import numpy as np

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
        cardiac_phase[i] = 2 * np.pi * (t - t1) / (t2 - t1) # Eq 2

    regr = np.zeros((num_time, M * 2))
    for i in range(M):
        regr[:,i * 2] = np.cos((i + 1) * cardiac_phase)
        regr[:,(i * 2) + 1] = np.sin((i + 1) * cardiac_phase)

    return regr


def retroicor_respiratory(resp, M=3):
    '''
    need doc
    '''
    num_time = len(resp)
    resp_phase = np.zeros(num_time)

    # the algorithm
    nb = 500
    val, edges = np.histogram(resp, bins=nb)

    for i in range(num_time):
        v = resp[i]
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
    for i in range(M):
        regr[:,i * 2] = np.cos((i + 1)  * resp_phase)
        regr[:,(i * 2) + 1] = np.sin((i + 1)  * resp_phase)

    return regr
