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
from distutils import file_util
from glob import glob
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

def reconstruct_and_save_volume_2disk(file_path: str, file_name_raw: str, file_name_recon: str=None, 
                                      file_name_json_recon_params: str="DefaultReconParams",
                                      bScan_strt_idx: int=110, 
                                      is_return_enface: str=True,
                                      is_save_2disk: bool=False, 
                                      is_save_brightest_aScan: bool=False, max_idxs: tuple=None) -> np.array:
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
    # returns tuple with middle B-scan and en face OR just enface, depending on flag "is_return_enface" 
    recon_data = process_buffer_wise(REC, file_name_json_recon_params, 
                                     dims, dims_saving, 
                                     full_file_path_raw, full_file_path_recon, 
                                     is_return_enface=is_return_enface, 
                                     b_scan_start_idx=bScan_strt_idx,
                                     is_save_2disk=is_save_2disk,
                                     is_save_brightest_aScan=is_save_brightest_aScan,
                                     max_idxs=max_idxs)
    return recon_data

def process_buffer_wise(REC, json_file_name, dims, dims_saving, full_file_path_raw, full_file_path_recon, 
                        b_scan_start_idx: int=0, is_save_2disk: bool=False, is_save_brightest_aScan: bool=False,
                        max_idxs: tuple=None, is_return_enface=True) -> None:
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
    for c_len in range(dims[-1]):
        # open raw file, move pointer to current B-scan and reconstruct
        with open(full_file_path_raw, 'rb') as f_raw:
            count = b_scan_raw_in_bytes # file size in bytes
            offset = ((c_len + b_scan_start_idx) % dims[-1]) * b_scan_raw_in_bytes # offset in bytes
            # print('\n', count, offset, offset//(dims[0]*dims[1]))
            raw_buffer = np.fromfile(full_file_path_raw, count=count, offset=offset, dtype='<u2')
            raw_buffer = np.reshape(raw_buffer, (dims[1],dims[0]))
            raw_buffer = raw_buffer.swapaxes(0,1)
            raw_buffer = np.roll(raw_buffer, (dims[1]//2)-1, axis=1)
            if c_len % 2 == 0:
                raw_buffer = np.roll(raw_buffer, raw_buffer.shape[1]//2, axis=1)
            # print(f"{c_len} Size of raw buffer {raw_buffer.size} bytes in {raw_buffer.dtype}")
            recon_buffer = REC._run_reconstruction_from_json(buffer=raw_buffer,
                                                             json_config_file_path=json_file_name)
            # option to save max-index scans to disk - needs max_idxs as tuple with pos. of brightest A-scans
            if is_save_brightest_aScan:
                assert len(max_idxs) == 2
                if c_len == max_idxs[0]:
                    print(f"\nWriting brightest A-scan with pos={max_idxs} and {np.size(raw_buffer[:,max_idxs[1]])*2} bytes to disk")
                    with open(full_file_path_raw.split('.bin')[0] + '_RawAscans.bin', 'a+b') as f_aScan: # Save to file in binary append mode
                        raw_buffer[:,max_idxs[1]].astype('<u2').tofile(f_aScan)
            # assign middle B-scan to return var @return=middle_bScan
            if c_len == (dims[-1]//2)-1:
                middle_bScan = recon_buffer
            # option to create enface for viewing: append B-scan projection to enface array
            if is_return_enface:
                enface[:,c_len] = np.max(recon_buffer, axis=0)
            # sanity check if processing size matches expected data size
            data_size += raw_buffer.size * raw_buffer.itemsize # counter increment of current recon-buffer size 
        # option to save current reconstructed buffer to disk (serialized, as one big *-BIN-file)
        if is_save_2disk:
            with open(full_file_path_recon, 'a+b') as f: # Save to file in binary append mode
                recon_buffer.tofile(f)
            # # sanity check for file size - mostly debug
            if int(recon_buffer.size) != int(dims_saving[0]*dims_saving[1]):
                print(f"[WARNING:] Saved {recon_buffer.size} bytes to disk (expected {int(dims_saving[0]*dims_saving[1])} bytes)")
    # display processing time of entire volume
    print(f"Processing took {time.perf_counter()-t1}s")
    # option to return middle B-scan and en face
    if is_return_enface:
        return middle_bScan, enface
    # return enface map only
    return middle_bScan

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
        enface.append(np.mean(raw_buffer, axis=0))
    return np.asarray(enface)


def crop_brightest_aScans(data: np.array, crop_radius: int=1) :
    """  """
    ## TODO: Continue here
    # sanity checks
    assert data.ndims == 3, "Data cube is not properly reshaped"
    # create vars and instances
    REC = OctReconstructionManager()
    cropped_scans = []
    t1 = time.perf_counter()
    print(f"[INFO:] Starting reconstruction of OCT volume...")
    recon_cube = REC._run_reconstruction_from_json(data, 'DefaultReconParams')
    print(f"Took {round(time.perf_counter(-t1), 1)} sec to reconstruct volume")
    enface = np.max(recon_cube, axis=0)
    max_col, max_row = np.amax()
    return cropped_scans

def run() -> None:
    pass

    
# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from     < reconstructlargeoctvolumes.py >     ...")
    # run()
    file_path = r"D:\100kHz_RollOff"
    file_names = glob(file_path + "/*.bin")
    print(file_names)
    for file_name in tqdm(file_names):
        print(file_name)
        file_name = file_name.split('\\')[-1]
        bScan, enface = reconstruct_and_save_volume_2disk(file_path, file_name, is_save_2disk=True)
        # plt.imshow(enface)
        # plt.show()
        # plt.imshow(cv2.resize(bScan, (1000,2000)))
        # plt.show()