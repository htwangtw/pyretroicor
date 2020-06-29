"""
Main entry point
"""

import argparse

import nibabel

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
    nii_file = args.filename
    physio_file = args.physio
    out_dir = args.output

    # check all files neesed exist: nifti, physio, accompanied jsons
    # create output dir if not exist
    # load imaging data and physio data
    # run retroicor
    # save results as tsv



if __name__ == "__main__":
    main()
