# %% 
import cv2
import os, sys
import numpy as np
import matplotlib.pyplot as plt

in_dims = (13262, 512, 512)
in_data_dtype = np.uint8
in_data_bytes = 1
path_to_data_file = r"P:\Data(NonBackuppable)\PhD_Data\OctVolumeRegistration\data_aux\rasterVol01_recon_13312x512x512.bin"

def tuple_prod(val) :
    res = 1
    for ele in val:
        res *= ele
    return res 

def load_entire_oct_volume(path: str, dims: tuple, dtype: str) -> np.array:
    file_expect_bytes = tuple_prod(dims) * in_data_bytes
    assert os.path.getsize(path) == file_expect_bytes, f"Size mismatch between expected ({os.path.getsize(path)} bytes) and actual file size ({file_expect_bytes} bytes)"
    with open(path) as f:
        in_buffer = np.fromfile(f, dtype=dtype)
    in_buffer = np.reshape(in_buffer, dims)
    return np.swapaxes(in_buffer, 0, -1)

in_buffer = load_entire_oct_volume(path_to_data_file, in_dims, in_data_dtype)

# %%
in_buffer = np.swapaxes(in_buffer, 0, 1)

plt.figure(figsize=(10,20))
plt.imshow(in_buffer[:,255,:])

def display_loaded_buffer(buffer) -> None:
    _, ax = plt.subplots(1,3, figsize=(20,10))
    ax[0].imshow(np.mean(buffer, axis=0), cmap="gray")
    ax[0].axis("off")
    ax[1].imshow(buffer[:,buffer.shape[1]//2,:], cmap="gray")
    ax[2].imshow(buffer[...,buffer.shape[2]//2], cmap="gray")
    plt.show()
    return

# display_loaded_buffer(in_buffer)

# %% LIVE SCRIPT TO RECONSTRUCT LARGE OCT VOLUMES

# global imports
import os, sys
import numpy as np

# local imports
module_path = r"C:\Users\phili\Documents\Coding\Repositories\OctProcessingAndDisplay\BackEnd"
sys.path.append(module_path)
from octreconstructionmanager import OctReconstructionManager


REC = OctReconstructionManager()

# self, raw_dims: tuple, json_file_name: str,  full_file_path_raw: str, 
                            #   bScan_start_idx: int=0, full_file_path_recon: str=None, is_save_volume_2disk: bool=False
                            
file_name_path_raw = r"P:\Data(NonBackuppable)\PhD_Data\OctVolumeRegistration\data_aux\rasterVol01_13312x512x512.bin"
file_name_path_saving = r"P:\Data(NonBackuppable)\PhD_Data\OctVolumeRegistration\data_aux\rasterVol01_recon_13262x512x512.bin"
file_name_path_json = r"C:\Users\phili\Desktop\DefaultReconParams"

out_vol = REC.process_large_volumes((13312, 512, 512), 
                                    json_file_name=file_name_path_json, 
                                    full_file_path_raw=file_name_path_raw, 
                                    full_file_path_recon=file_name_path_saving, 
                                    is_save_volume_2disk=True)
# %%
