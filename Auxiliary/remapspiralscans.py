
import os
import sys
import glob
import numpy as np
from tqdm import tqdm
from scipy import signal
from natsort import natsorted
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(r"C:\Users\phili\Documents\Coding\Repositories\OctProcessingAndDisplay\BackEnd"))

from octreconstructionmanager import OctReconstructionManager as REC
from octdatafilemanager import __return_volume_dims_string
R = REC()

    
def reconstruct_and_remap_volume(file_path: str, in_vol_shape: tuple, split_fac: int, offset: int=4805, is_debug: bool=False, filter_kernel: tuple=(3,3,3)):
    ReconManager = REC()
    with open (file_path, 'r') as f:
        buffer = np.fromfile(f, dtype=np.uint16)
    buffer = buffer.reshape(in_vol_shape[2], in_vol_shape[1], in_vol_shape[0])
    print( "\nReconstructing...")
    mean = np.mean(buffer, axis=(0,1)) # BG vector
    buffer = buffer - mean[np.newaxis, np.newaxis, :] # BG subtraction
    buffer = np.asarray(buffer, dtype=np.complex64) # recast as complex array
    buffer.real = buffer.real * -disp_vec.real[np.newaxis, np.newaxis, :] # complex disp correction
    buffer.imag = buffer.imag * disp_vec.imag[np.newaxis, np.newaxis, :] # complex disp correction
    buffer = buffer.reshape(in_vol_shape[2], in_vol_shape[1]*split_fac, in_vol_shape[0]//split_fac) # reshape -> spectral splitting
    window = np.asarray(np.hanning(704), dtype=np.float32) # create spectral shaping vector
    buffer = buffer * window[np.newaxis, np.newaxis, :] # spectral shaping 
    buffer = buffer.swapaxes(0,-1)
    buffer = ReconManager.perform_fft(buffer, l_pad=704)
    buffer = ReconManager.perform_post_fft_functions(buffer, 64, 85, 10, 0, True)
    buffer = buffer.swapaxes(1,2)
    buffer = buffer.reshape(694, buffer.size//694)
    remapped_vol = np.zeros((694, table_size+1, table_size+1))
    print("Remapping...")
    if is_debug:
        for j in range(4800, 4900, 10): # debug
            offset = j
            for pos in range(buffer.shape[1]):
                for i in range(3):
                    if table[pos, i+i] != 0 and table[pos, i+i+1] != 0:
                        remapped_vol[:, table[pos, i+i], table[pos, i+i+1]] = buffer[:, (pos+offset)%buffer.shape[1]]
            fig, ax = plt.subplots(1, 3, figsize=(20,10))
            fig.suptitle(f"Offset = {offset}", fontsize=30)
            ax[0].imshow(np.mean(remapped_vol, axis=0), cmap='gray')
            ax[1].imshow(remapped_vol[...,391//2], cmap='gray')
            ax[2].imshow(remapped_vol[:,391//2,:], cmap='gray')
            plt.show()
        
    else:
        for pos in range(buffer.shape[1]):
            for i in range(3):
                if table[pos, i+i] != 0 and table[pos, i+i+1] != 0:
                    remapped_vol[:, table[pos, i+i], table[pos, i+i+1]] = buffer[:, (pos+offset)%buffer.shape[1]]
    print("Filtering volume...")
    filtered_vol = signal.medfilt(remapped_vol, filter_kernel)
    return remapped_vol, filtered_vol

# def load

if __name__ == '__main__':
    
    ### Ramapping Table 
    path_remapping_file = r"C:\Users\phili\Downloads\04_Spiral_600_2_10.bin"
    with open(path_remapping_file, 'r') as f:    
        table = np.fromfile(f, dtype=np.uint32)
    table = table.reshape(6, table.size//6) # check if reshaping and loading make sense  
    table = table.transpose()
    table_size = np.max(table) 
    
    ### Dispersion Correction
    filepath_disp_vec = r"C:\Users\phili\Desktop\PhillyScripts\Dispersion_704_1_2_600kHz.bin"
    with open(filepath_disp_vec, 'r') as f_disp:
        disp_vec = np.fromfile(f_disp, dtype=np.complex64)
        disp_vec = disp_vec.reshape(1, 1408)

    ### Folders with raw OCT volume data
    all_glob_files = [
        r"E:\VolumeRegistration\Eye2_M5_RawVols",
        r"E:\VolumeRegistration\Eye1_M1_RawVols",
        r"E:\VolumeRegistration\Eye1_M2_RawVols",
        r"E:\VolumeRegistration\Eye1_M3_RawVols",
        r"E:\VolumeRegistration\Eye1_M4_RawVols",
        r"E:\VolumeRegistration\Eye1_M5_RawVols"
        ]

    ### Files with raw OCT volume data
    for folder in all_glob_files:
        path_to_binaries = folder
        all_files = glob.glob(path_to_binaries + "/*.bin")
        raster_vol_list = [file for file in all_files if "rasterVol" in file]
        raster_vol_list = natsorted(raster_vol_list)         

    ### main processing loop
    for vol_file in tqdm(raster_vol_list):
        remapped, filtered = reconstruct_and_remap_volume(file_path=vol_file, in_vol_shape=(1408, 2352, 25), split_fac=2, offset=4845, is_debug=False) 
        post_fix_unfiltered = __return_volume_dims_string(remapped.shape)
        post_fix_filtered =  __return_volume_dims_string(filtered.shape)
        file_path_saving_unfiltered = os.path.join(os.path.dirname(vol_file), os.path.basename(vol_file).split('_')[0] + '_remapped' + post_fix_unfiltered + ".bin")
        file_path_saving_filtered = os.path.join(os.path.dirname(vol_file), os.path.basename(vol_file).split('_')[0] + "_remapped_filtered" + post_fix_filtered + ".bin")
        print(file_path_saving_filtered)
        print(file_path_saving_unfiltered)
        remapped.astype(np.uint8).tofile(file_path_saving_unfiltered)
        filtered.astype(np.uint8).tofile(file_path_saving_filtered)