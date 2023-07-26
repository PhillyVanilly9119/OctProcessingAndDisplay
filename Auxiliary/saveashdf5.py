
import h5py
import os, sys
import numpy as np
import matplotlib.pyplot as plt

def load_entire_volume_from_binary(path: str, dims: tuple, dtype: np.dtype) -> np.array:
    # assert np.prod(dims) == os.path.getsize(path), f"File size mismatch {np.prod(dims)} is not equal to {os.path.getsize(path)}" # to avoid unessary lloading times if mismatch
    with open(path, 'r') as f:
        vol = np.fromfile(f, dtype=dtype)
    return np.reshape(vol, dims).swapaxes(0, -1)

def save_volume_to_file(volume: np.array, filename: str, volume_name: str) -> None:
    filename = os.path.splitext(filename)[0] + '.h5'
    h5f = h5py.File(filename, 'w')
    h5f.create_dataset(volume_name, data=volume)
    h5f.close()

def run():
    file_path = r"C:\Users\phili\Desktop\flow_1536x2048x2045x2_187.bin"
    vol = load_entire_volume_from_binary(file_path, (2044, 2048, 1536), np.uint8)
    plt.imshow(vol[...,1024])
    plt.show()
    save_volume_to_file(vol, file_path, "test_volume")

if __name__ == "__main__":
    run()