"""
Main entry point
"""
from pathlib import Path
import argparse
import json
import gzip

import numpy as np
import nibabel as nb

from pyretroicor.retroicor import retroicor_cardiac, retroicor_respiratory
from pyretroicor.prepro import process_resp, process_cardiac

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',  metavar='path',
        help="Path to fMRI nifti files."
        )
    parser.add_argument(
        'physio',  metavar='physio',
        help="Path to physiology files in BIDS standard. \
        Accept cardiac and/or respiratory recording."
        )
    parser.add_argument(
        'output',  metavar='output',
        help="Path to save calculated derivatives."
        )

    args = parser.parse_args()
    NII_FILE = args.filename
    PHYSIO_FILE = args.physio
    OUTDIR = args.output

    # check all files neesed exist: nifti, physio, accompanied jsons
    physio_json = PHYSIO_FILE.split(".tsv.gz")[0] + ".json"
    func_json = NII_FILE.split(".nii.gz")[0] + ".json"
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


    func = nb.load(NII_FILE)  # nibabel should do the test itself
    physio = np.loadtxt(PHYSIO_FILE) 
    # create time
    time = np.arange(0, physio.shape[0])  * (1 / sampling_freq) + start_time
    if start_time < 0:
        time_zero = np.where(time < 0)[0][-1] + 1
        time = time[time_zero:]
        physio = physio[time_zero:, :]

    cardiac = physio[:, columns.index("cardiac")]
    respiratory = physio[:, columns.index("respiratory")]
    
    # TR labels
    n_vol = func.shape[0]
    tr = func_meta["RepetitionTime"]
    tr_time = np.arange(1, n_vol + 1)  * tr
    tr_idx = []
    for t in tr_time:
        idx = np.where(time < t)[0][-1] + 1
        tr_idx.append(idx)

    # peak detection and cleaning
    r_peak = process_cardiac(cardiac, sampling_freq)  # r peak index
    r_peak = time[r_peak]  # r peak time point
    retro_card = retroicor_cardiac(time, r_peak)

    # run retroicor
    respiratory = process_resp(respiratory, sampling_freq)
    retro_resp = retroicor_respiratory(respiratory)
    # rextract value per TR
    retroicor_regressors = np.hstack((retro_card, retro_resp))[tr_idx, :]

    # create output dir
    nii_file = Path(NII_FILE)
    subject = nii_file.name.split("_")[0].split("sub-")[-1]
    filename_root = nii_file.name.split("_bold")[0]
    if "ses" in NII_FILE:
        session = nii_file.name.split("_")[1].split("ses-")[-1]
        filepath = Path(OUTDIR) / "pyretroicor" / f"sub-{subject}" / f"ses-{session}" 
        out_name = f"{filename_root}_desc-retroicor_regressors.tsv"
    else:
        filepath = Path(OUTDIR) / "pyretroicor" / f"sub-{subject}"
        out_name = f"{filename_root}_desc-retroicor_regressors.tsv"

    filepath.mkdir(parents=True, exist_ok=True)

    # save results as tsv
    header = [f"retroicor_cardiac_{i + 1}" for i in range(6)] \
        + [f"retroicor_respiration_{i + 1}" for i in range(6)]

    np.savetxt(filepath / out_name, retroicor_regressors, 
               delimiter="\t", header="\t".join(header), 
               comments="")

if __name__ == "__main__":
    main()
