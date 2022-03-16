"""
                                        ******
            @author: @Philipp Matten
            @contact: philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2022 
                                        ******
                                         
                >>> main file for OCT Recon GUI creation, methods and handling     
                                
"""

# global imports
import cmath
import os
import sys
import cv2
import time
import numpy as np
from sympy import sring
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

from octreconstructionmanager import OctReconstructionManager 
from configdatamanager import ConfigDataManager 


def display_reconstructed_oct_volume( data_shape: tuple=(5312, 512, 512) ) -> np.array :
    ORM = OctReconstructionManager( dtype_loading='<u1' )
    data = np.asarray( np.fromfile(ORM._tk_file_selection(), dtype='>u1') )
    data = data.reshape( data_shape )
    fig, ax = plt.subplots(2,2)
    ax[1,0].imshow(data[:, :, data.shape[-1]//2], title="B-scan along \'fast scanning axis\'")
    ax[1,1].imshow(data[:, data.shape[-2]//2, :], title="B-scan along \'slow scanning axis\'")
    ax[0,1].imshow( np.mean(data, axis=0) )
    ax[0,1].imshow( np.mean(data, axis=0), title="En face of recon volume") 
    plt.show()
    return 

def reconstruct_and_save_volume_2disk(file_path: str, file_name_raw: str, bScan_strt_idx: int=110, is_return_enface: str=True, file_name_recon: str=None, file_name_json_recon_params: str="DefaultReconParams") -> np.array:
    """ @param: """
    # initialize file name for saving recon volume
    if file_name_recon is None:
        file_name_recon = "recon_" + file_name_raw
    else:
        print(f"[WARNING:] You've manually entered a target file name:\n{file_name_recon}\nCheck volume output dimensions (HF and DC cropping!)")
    # ----------- Import classes/objects for recon handling ------------
    # load recon parms from file into json-object
    JSON = ConfigDataManager(filename=file_name_json_recon_params).load_json_file()
    # recon functions
    REC = OctReconstructionManager()
    # ----------- Pre-Reconstruction steps ------------
    # create files and file paths
    full_file_path_raw = os.path.join(file_path, file_name_raw)
    dims, _ = REC.get_oct_volume_dims(full_file_path_raw)
    # get all underbar-seperated file name prefixes to generate file to save to
    def parse_prefixes_file_dims(file_name: str) -> str:
        prefix = ''
        pre_split_list = file_name.split('_')[:-1]
        for i, string in enumerate(pre_split_list):
            prefix += string + '_'
        return prefix
    # ----------- Save file prefix ------------
    # update cropped A-scan length
    dims_saving = (dims[0]-int(JSON['dc_crop_samples'])-int(JSON['hf_crop_samples']), dims[1], dims[2]) 
    # create file to save to
    full_file_path_recon = os.path.join(file_path, parse_prefixes_file_dims(file_name_recon) + str(dims_saving[0]) + 'x' + str(dims_saving[1]) + 'x' + str(dims_saving[2]) + '.bin')
    if is_return_enface:
        return process_buffer_wise(REC, JSON, dims, dims_saving, full_file_path_raw, full_file_path_recon, b_scan_start_idx=bScan_strt_idx)
    process_buffer_wise(REC, JSON, dims, dims_saving, full_file_path_raw, full_file_path_recon, is_return_enface=is_return_enface, b_scan_start_idx=bScan_strt_idx)
    return

def process_buffer_wise(REC, JSON, dims, dims_saving, full_file_path_raw, full_file_path_recon, b_scan_start_idx=500, is_return_enface=True) -> None:
    """ @param: """
    # pre-loop vars for data and proc.-time measurements 
    t1 = time.perf_counter()
    data_size = 0
    b_scan_raw_in_bytes = dims[0] * dims[1]
    if is_return_enface: # generate and return enface only if necessary
        enface = np.zeros((dims[-2], dims[-1]))
    print("Starting timer for processing...")
    print(f"[INFO:] Expected dimensions of one buffer/B-scan are {dims} (with {b_scan_raw_in_bytes} bytes)\nReturning a cropped, reconstructed B-scan with dims {dims_saving} (with {dims_saving[0]*dims_saving[1]} bytes)")
    # ----------- Loop through data (B-scan-wise), reconstruct and save to file ------------
    for c_len in tqdm(range(dims[-1])):
        # open raw file, move pointer to current B-scan and reconstruct
        with open(full_file_path_raw, 'rb') as f_raw:
            count = b_scan_raw_in_bytes # file size in bytes
            offset = ((c_len + b_scan_start_idx) % dims[-1]) * b_scan_raw_in_bytes # offset in bytes
            # print('\n', count, offset, offset//(dims[0]*dims[1]))
            raw_buffer = np.fromfile(full_file_path_raw, count=count, offset=offset, dtype='<u2')
            raw_buffer = np.reshape(raw_buffer, (dims[1],dims[0]))
            raw_buffer = raw_buffer.swapaxes(0,1)
            raw_buffer = np.roll(raw_buffer, 255, axis=1)
            if c_len % 2 == 0:
                raw_buffer = np.roll(raw_buffer, raw_buffer.shape[1]//2, axis=1)
            # print(f"{c_len} Size of raw buffer {raw_buffer.size} bytes in {raw_buffer.dtype}")
            recon_buffer = REC._run_reconstruction(buffer = raw_buffer,
                                                   disp_coeffs = JSON['dispersion_coefficients'], 
                                                   wind_key = JSON['windowing_key'],
                                                   samples_hf_crop = JSON['hf_crop_samples'], 
                                                   samples_dc_crop = JSON['dc_crop_samples'],
                                                   blck_lvl = JSON['black_lvl_for_dis'], 
                                                   scale_fac = JSON['disp_scale_factor']
                                                   )
            if c_len == 216:
                bIdx = 216
                print(f"Writing... {np.size(raw_buffer[:,bIdx-3:bIdx+3])} bytes for brightest A-scan")
                raw_buffer[:,bIdx-3:bIdx+3].tofile(full_file_path_raw.split('.bin')[0] + '_scans.bin')
            if c_len == dims[-1]//2:
                middle_bSacan = recon_buffer
            if is_return_enface: # append B-scan projection to enface array
                enface[:,c_len] = np.mean(recon_buffer, axis=0)
                # enface[:,c_len] = np.mean(recon_buffer[:recon_buffer.shape[0]//2], axis=0)
            data_size += raw_buffer.size * raw_buffer.itemsize # counter increment of current recon-buffer size 
        # Save to file in binary append mode
        with open(full_file_path_recon, 'a+b') as f:
            recon_buffer.tofile(f)
    # sanity check for file size - mostly debug
    if data_size is not int(dims_saving[0]*dims_saving[1]*dims_saving[2]):
        print(f"[WARNING:] Saved {data_size} bytes to disk (expected {int(dims_saving[0]*dims_saving[1]*dims_saving[2])} bytes)")
    # display processing time of entire volume
    print(f"Processing took {time.perf_counter()-t1}s")
    if is_return_enface:
        return enface, middle_bSacan
    return middle_bSacan

def create_raw_enface(path: str, dims: tuple, b_scan_start_idx: int) -> None:
    """ @param: """
    enface = []
    for c_len in range(dims[-1]):
    # open raw file, move pointer to current B-scan and reconstruct
        b_scan_raw_in_bytes = dims[0] * dims[1]
        count = b_scan_raw_in_bytes # file size in bytes
        offset = ((c_len + b_scan_start_idx) % dims[-1]) * b_scan_raw_in_bytes # offset in bytes
        # print('\n', count, offset, offset//(dims[0]*dims[1]))
        with open(path, 'rb') as f_raw:
            raw_buffer = np.fromfile(path, count=count, offset=offset, dtype='<u2')
            raw_buffer = np.reshape(raw_buffer, (dims[-1],dims[0]))
            raw_buffer = raw_buffer.swapaxes(0,1)
            # raw_buffer = np.roll(raw_buffer, 255, axis=1)
            # if c_len % 2 == 0:
            #     raw_buffer = np.roll(raw_buffer, raw_buffer.shape[1]//2, axis=1)
        enface.append(np.mean(raw_buffer, axis=0))
    return np.asarray(enface)

def run() -> None:
    bScan_strt_idx = 0
    enface, m_bScan = reconstruct_and_save_volume_2disk(r"D:\100kHz_RollOff", 
                                                        "rasterVol01_13312x512x512_01.bin", 
                                                        bScan_strt_idx=bScan_strt_idx)
    # enface = create_raw_enface(r"D:\100kHz_RollOff\rasterVol01_13312x512x512_00.bin", (13312, 512, 512), 0)
    print(np.where(enface == np.amax(enface)))
    fig, ax = plt.subplots(1,2)
    ax[0].imshow(enface)
    ax[1].imshow(m_bScan)
    plt.show()
    
# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from     < reconstructlargeoctvolumes.py >     ...")
    run()