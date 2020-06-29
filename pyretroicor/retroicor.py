import numpy as np

def retroicor_cardiac(time, r_peak, M):
    '''
    we need documentations
    translated from matlab code

    r_peak - time of the r peaks
    time - tr time stamp?
    M - ??????
    '''

    # the algorithm
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


def retroicor_cardiac(resp, M):
    '''
    need doc
    '''
    nt = len(resp)
    resp_phase = np.zeros(nt)

    # the algorithm
    nb = 500
    val, edges = np.histogram(resp, bins=nb)

    for i in range(nt):
        v = resp[i]
        closest_peak = np.abs(v - t)
        edge = np.where(closest_peak == np.amin(closest_peak))[0]
        if (edge - v) > 0:
            edge = edge - 1
        area = np.sum(val[0:edge])
        sign_resp = np.sign(resp[i])
        if sign_resp == 0:
            sign_resp = 1
        resp_phase[i] = np.pi * area * sign_resp / nt

    regr = np.zeroes(num_vol, M * 2)
    for i in range(M):
        regr[:,i * 2 + 1] = np.cosin(i * resp_phase)
        regr[:, (i + 1) * 2] = np.sin(i * resp_phase)

    return regr