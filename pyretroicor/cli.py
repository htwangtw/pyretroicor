"""Console script for pyretroicor."""
import sys
import argparse
from pathlib import Path
import json

import numpy as np
import nibabel as nb

from pyretroicor.retroicor import retroicor_cardiac, retroicor_respiratory
from pyretroicor.prepro import process_resp, process_cardiac
from pyretroicor.util import bids_load_meta, bids_output_name, tr_reference, save_tsv

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
    M = 3

    # check all files neesed exist: nifti, physio, accompanied jsons
    physio_meta, func_meta = bids_load_meta(PHYSIO_FILE, NII_FILE)
    func = nb.load(NII_FILE)  # nibabel should do the test itself
    physio = np.loadtxt(PHYSIO_FILE) 

    # load some parameters
    tr = func_meta["RepetitionTime"]
    n_vol = func.shape[0]

    # create time reference for physio
    time, physio = physio_time(physio, 
                               physio_meta["SamplingFrequency"], 
                               physio_meta["StartTime"])

    # create time stamps for each TR
    tr_idx, _ = tr_reference(n_vol)

    # load physio files 
    cardiac = physio[:, physio_meta["Columns"].index("cardiac")]
    respiratory = physio[:, physio_meta["Columns"].index("respiratory")]

    # peak detection and cleaning, run retroicor
    r_peak = process_cardiac(cardiac, sampling_freq)  # r peak index
    r_peak = time[r_peak]  # r peak time point
    retro_card = retroicor_cardiac(time, r_peak, M)

    # cleaning and run retroicor
    respiratory = process_resp(respiratory, sampling_freq)
    retro_resp = retroicor_respiratory(respiratory, M)

    # extract value per TR
    retroicor_regressors = np.hstack((retro_card, retro_resp))[tr_idx, :]

    # create output dir
    filepath = bids_output_name(PHYSIO_FILE)

    # save tsv
    save_tsv(retroicor_regressors, filepath)

if __name__ == "__main__":
    main()
