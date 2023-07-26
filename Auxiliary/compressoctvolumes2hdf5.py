import h5py
import glob
import numpy as np
from tqdm import tqdm
from natsort import natsorted

def compress_and_save_to_hdf5(arrays, file_path_saving):
    # Create an HDF5 file for writing
    with h5py.File(file_path_saving, 'w') as hf:
        for i, arr in tqdm(enumerate(arrays)):
            # Create a dataset in the HDF5 file for each array
            dataset_name = f'oct_volume_{i}'            
            # Compress the data using gzip compression and save it to the dataset
            hf.create_dataset(dataset_name, data=arr, compression='gzip')

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

if __name__ == "__main__":

    file_dir = r"C:\Users\phili\Desktop\20230221_110638_binaries\Resized"
    output_file = r"C:\Users\phili\Desktop\20230221_110638_binaries\Resized\compressed_arrays.hdf5"
    files = glob.glob(file_dir + "/*.bin")
    files = natsorted(files)

    volumes_to_compress = stack_n_numpy_arrays(files, (403,391,391))
    compress_and_save_to_hdf5(volumes_to_compress, output_file)

    print("OCT volumes compressed and saved to:", output_file)
