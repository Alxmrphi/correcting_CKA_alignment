
import numpy as np
import os
import pandas as pd

from pathlib import Path
from torchvision import datasets, models, transforms
from torch.utils.data import Dataset, DataLoader

# ---------------------
# This file contains the following functions:
# 1. get_presentation_idx
# 2. get_presentation_idx_in_imgs_list
# 3. get_session_df
# 4. get_fMRI_data (main function)
# ---------------------

# -------------------
sub = "01"
#subject_folder = Path(f'/home/alxmrphi/Documents/THINGS/fMRI/table_format/')
subject_folder = Path(f'.')

stim_file = subject_folder / f'sub-{sub}_StimulusMetadata.csv'
voxel_file = subject_folder / f'sub-{sub}_VoxelMetadata.csv'
data_file = subject_folder / f'sub-{sub}_ResponseData.h5'

data_dir = Path('/home/amurphy3/nc/data/THINGS')

# --------------------


def get_presentation_idx(filename, df):
    """ This function looks up which index a particular 
        filename was presented at in stim_data."""

    idx = df.loc[ df['stimulus'] == filename].index.values
    if len(idx) == 0:
        raise Exception('Not Found')
    if len(idx) == 1:
        return idx[0]
    else:
        raise Exception('Found multiple - not sure what to do')

def get_presentation_idx_in_imgs_list(filename, imgs_list):
    """ This function looks at the filenames in `stim_data` and looks
    for where these occur in the `dataset.imgs` list for later alignment. """

    for i, (img, label) in enumerate(imgs_list):
        #print(Path(img).name)
        if Path(img).name == filename:
            return i
    return -1

def get_session_df(stim_data, imgs_list, voxel_responses, imgs_list_exclude):
    """
    With a list of `imgs_list` images, each one needs to have fMRI data or zeros array.
    Buid up over this list to capture all elements easily and for those filenames in 
    `imgs_list` for which there is no fMRI data, make a zeros array voxel data and for
    those that do have fMRI data, extract it from `voxel_responses`. The resulting df
    will have as many rows as there are entries in `imgs_list` subtracting out any that
    also appear in `imgs_list_exclude` and as many columns as there are voxels in the
    `voxel_responses` array. Approximately 60% of the rows will be zero vectors because
    fMRI data in THINGS only has a coverage of about 40% of the images.

    Args:
    ---------
        stim_data: stimulus information from the fMRI experiment
        imgs_list: a list of all image file paths to be extracted
        voxel_responses: voxel data loaded from the ResponseData.h5 file 
        imgs_list_excludes: a list of any images for which to exclude

    Returns:
    ------- 
        df: a pandas DataFrame with image-level voxel responses
    """

    df = pd.DataFrame()
    excluded_filenames = set(Path(x[0]).name for x in imgs_list_exclude)
    images_with_fMRI = set(stim_data['stimulus'])
    voxel_dimension = voxel_responses.shape[0]

    for i, file in enumerate(imgs_list):
        filename = Path(file[0]).name
        
        # check filename not imn imgs_val_list
        if filename in excluded_filenames:
            continue

        # some images are not part of each set, so need to skip these
        if filename not in images_with_fMRI:
            voxel_data = np.zeros(voxel_dimension)
        else:
            bool_mask = (stim_data['stimulus'] == filename)
            idx = stim_data['stimulus'][bool_mask].index[0]
            voxel_data = voxel_responses[idx].to_numpy()
        
        df = df.assign(**{f'{i}': voxel_data})

    return df

    

def get_fMRI_data(stim_file: Path,
                  voxel_file: Path,
                  data_file: Path,
                  subject_no: int,
                  subject_folder,
                  imgs_list_path: Path,
                  roi: str,
                  save_fname: str
                  ):

    # Extract the voxel ids for specified ROI
    voxdata = pd.read_csv(voxel_file)
    voxels = voxdata[voxdata[roi] == 1]
    voxel_ids = voxels['voxel_id'].to_numpy()

    # Extract data corresponding to desired voxel ids
    responses = pd.read_hdf(data_file); 
    responses = responses[responses.index.isin(voxel_ids)]

    # Get image list
    dataset = datasets.ImageFolder(imgs_list_path)
    imgs_list = dataset.imgs

    # Read stim data and generate dataframe
    stim_data = pd.read_csv(stim_file)
    df = get_session_df(stim_data, imgs_list, responses, [])

    np.save(save_fname, df.T.to_numpy())
    print(f'Saved: {save_fname}')