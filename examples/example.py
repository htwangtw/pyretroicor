import json

import numpy as np
import nibabel as nb

from pyretroicor.retroicor import retroicor_cardiac, retroicor_respiratory
from pyretroicor.prepro import *
from pyretroicor.util import physio_time, tr_reference, save_tsv


cardiac = np.loadtxt("data/cardiac.txt")
resperation = np.loadtxt("data/resperation.txt")

with open("data/meta_data.json", "r") as f: 
    meta = json.load(f)
tr = meta["RepetitionTime"]
fs = meta["SamplingFrequency"]
time, _ = physio_time(cardiac,
                      meta["SamplingFrequency"],
                      start_time=0)

# use 3 hz window (~=180 bpm) for peak detection
win_hz = 3
win_unit = int(fs / win_hz)

# window for cleaning the signal needs to be smaller (1.5 hz)
cleaning_window = int(win_unit / 2)

# clean outliers
outliers = rolling_mad(cardiac, cleaning_window) 
t = np.arange(0, cardiac.shape[0])
interp_cardiac = np.interp(t, t[~outliers], cardiac[~outliers])
smooth_cardiac = smooth(interp_cardiac, cleaning_window)
# get peaks
peak_idx = detect_peaks(smooth_cardiac, mpd=win_unit)

r_peak = time[peak_idx]  # r peak time point

retro_card = retroicor_cardiac(time, r_peak, M=3)

resp_f = smooth(resperation, fs) # 1 second window for smooting 
time = np.arange(0, resp_f.shape[0])
outliers = rolling_mad(resp_f, int(0.5 * fs))
clean = np.interp(time, time[~outliers], resp_f[~outliers])

plt.plot(resp_f)
plt.plot(clean)
plt.show()

retro_resp = retroicor_respiratory(clean_resp, M=3)

tr_time, tr_idx = tr_reference(n_vol, tr, time)
