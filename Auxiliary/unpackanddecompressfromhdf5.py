import os
import h5py
from tqdm import tqdm


def change_file_type(file_path, new_extension):
    """
    Change the file type (extension) of a file.

    Parameters:
    - file_path: str
        The path to the file.
    - new_extension: str
        The new file extension to assign to the file.
    """
    directory, old_name = os.path.split(file_path)
    base_name, _ = os.path.splitext(old_name)
    new_name = f"{base_name}.{new_extension}"
    return os.path.join(directory, new_name)
    

def unpack_hdf5(file_path, output_path):
    """
    Unpack a compressed HDF5 file.

    Parameters:
    - file_path: str
        Path to the compressed HDF5 file.
    - output_path: str
        Path to the output directory for unpacked data.
    """
    with h5py.File(file_path, 'r') as file:
        # Iterate through the items in the HDF5 file
        for _, data in file.items():
            # Save each dataset to a separate file in the output directory
            output_file_path = f"{output_path}"
            uncompressed_data = data[:]
            uncompressed_data.tofile(output_file_path)


if __name__ == "__main__":

    hdf_file_paths = [
        r"P:\Frankeneye\48\Water\09_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\08_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\07_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\06_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\05_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\04_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\03_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\02_6656x700x700.hdf5",
        r"P:\Frankeneye\48\Water\01_6656x700x700.hdf5"
        ]

    for file in tqdm(hdf_file_paths):
        unpack_hdf5(file, change_file_type(file, "bin"))