"""
philipp.matten@gmail.com

"""

import os
import h5py
import glob
import numpy as np
from tqdm import tqdm
from scipy import signal 
from natsort import natsorted
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter


def compress_and_save_to_hdf5(volume, file_path_saving):
    # Create an HDF5 file for writing
    file_path_hdf5_saving = f"{file_path_saving[:-4]}.hdf5"
    with h5py.File(file_path_hdf5_saving, 'w') as hf:
        # Create dataset name
        dataset_name = "oct_volume_" + os.path.basename(file_path_saving).split("_")[1]
        # Compress the data using gzip compression and save it to the dataset
        hf.create_dataset(dataset_name, data=volume, compression='gzip', compression_opts=4)
        print(f"[INFO:] Done saving {dataset_name} in {file_path_hdf5_saving}")
    if os.path.isfile(file_path_hdf5_saving):
        os.remove(file_path_saving)
        

def load_entire_volume_from_binary(path: str, dims: tuple, dtype: np.dtype=np.uint8) -> np.array:
    with open(path, 'rb') as f:
        vol = np.fromfile(f, dtype=dtype).reshape(dims)
    return vol 


def stack_n_numpy_arrays(file_list: str, dims: tuple):
    # Initialize an empty list to hold the arrays
    stacked_arrays = []
    # Iterate through the arrays and add them to the list
    for file in file_list:
        with open(file, 'r') as f:
            volume = np.fromfile(f, dtype=np.uint8)
            volume = volume.reshape(dims)
            stacked_arrays.append(volume)
    return stacked_arrays


def run():
    
    main_file_dir = [
        r"C:\Users\phili\Downloads\20240111_162642_binaries"
        ]
    
    # create list of all *.bin volumes that are to be compressed and replaced
    for b_file in main_file_dir:
        files = glob.glob(f"{b_file}/*.bin")
        files = natsorted(files)
        for file in tqdm(files):
            volume = load_entire_volume_from_binary(file, (644,391,391))
            volume = median_filter(volume, (3,3,3))
            compress_and_save_to_hdf5(volume, file)

if __name__ == "__main__":
    run()
