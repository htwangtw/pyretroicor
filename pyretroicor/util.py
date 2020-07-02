"""I/O and file path senity check"""
from pathlib import Path
import json

import numpy as np
import nibabel as nb


def physio_time(physio, sampling_freq, start_time):
    time = np.arange(0, physio.shape[0])  * (1 / sampling_freq) + start_time
    if start_time < 0:
        time_zero = np.where(time < 0)[0][-1] + 1
        time = time[time_zero:]
        physio = physio[time_zero:, :]

    return time, physio

def tr_reference(n_vol):
    tr_time = np.arange(1, n_vol + 1)  * tr
    tr_idx = []
    for t in tr_time:
        idx = np.where(time < t)[0][-1] + 1
        tr_idx.append(idx)
    return tr_time, tr_idx

def bids_metadata_path(physio, func):
    physio_json = physio.split(".tsv.gz")[0] + ".json"
    func_json = func.split(".nii.gz")[0] + ".json"

    if not Path(physio_json).is_file:
        raise ValueError("Missing json file for physiology data. Is data in BIDS format?")

    if not Path(func_json).is_file:
        raise ValueError("Missing json file for fMRI data. Is data in BIDS format?")
    return physio_json, func_json

def bids_load_meta(physio, func):
    physio_json, func_json = bids_metadata_path(physio, func)

    with open(func_json) as f:
        func_meta = json.load(f) 
    with open(physio_json) as f:
        physio_meta = json.load(f) 

    return physio_meta, func_meta

def bids_load_physio():
    with open(func_json) as f:
        func_meta = json.load(f) 

    if not Path(physio_json).is_file():
        raise ValueError("Missing json file for physiology data. Is data in BIDS format?")
    else:
        with open(physio_json) as f:
            physio_meta = json.load(f) 

        sampling_freq = physio_meta["SamplingFrequency"]
        start_time = physio_meta["StartTime"]
        columns = physio_meta["Columns"]

def bids_output_name(phsiyo_path):
    """
    Create file name based on BIDS
    """
    phsiyo_file = Path(phsiyo_path)
    filename_root = phsiyo_file.name.split("_physio")[0]
    subject = filename_root.name.split("_")[0].split("sub-")[-1]
    if "ses" in filename_root:
        session = filename_root.name.split("_")[1].split("ses-")[-1]
        output_dir = Path(OUTDIR) / "pyretroicor" / f"sub-{subject}" / f"ses-{session}" 
        out_name = f"{filename_root}_desc-retroicor_regressors.tsv"
    else:
        output_dir = Path(OUTDIR) / "pyretroicor" / f"sub-{subject}"
        out_name = f"{filename_root}_desc-retroicor_regressors.tsv"

    # create output dir if not exist
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / out_name
    return filepath

def save_tsv(regressors, filepath):
    """
    save the regressors
    """
    M = int(np.min(regressors.shape) / 2) # I forgot which axis is timeseries
    # save results as tsv
    header = [f"retroicor_cardiac_{i + 1}" for i in range(M * 2)] \
           + [f"retroicor_respiration_{i + 1}" for i in range(M * 2)]

    np.savetxt(filepath, regressors, 
               delimiter="\t", header="\t".join(header), 
               comments="")

