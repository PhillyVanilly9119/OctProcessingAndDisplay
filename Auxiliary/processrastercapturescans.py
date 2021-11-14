"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality to process raster capture scans  
                                
"""

# global imports
import os
import sys
import time
from numpy.core.fromnumeric import shape
from tqdm import tqdm
from typing import List
import numpy as np
import matplotlib.pyplot as plt

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'FrontEnd')))

from octreconstructionmanager import OctReconstructionManager
# from guiconfigdatamanager import GuiConfigDataManager

def check_display_size_and_bScan_offset(d_coeffs=(-8,121,0,0), b_lvl=80, scaling=63.75, 
                              samples_dc_crop=100, samples_hf_crop=7900) -> None :
    ORM = OctReconstructionManager(dtype_loading='<u2')
    data = ORM.load_oct_data()
    new_dims = ((data.shape[0]-samples_dc_crop-samples_hf_crop), data.shape[1], data.shape[2])
    out_scan = np.zeros((new_dims))
    for scan in tqdm(range(512)) :
        buffer = data[:,:,scan]
        bScan = ORM._run_reconstruction(buffer, wind_key='hann', 
        disp_coeffs=d_coeffs, blck_lvl=b_lvl, scale_fac=scaling, 
        samples_dc_crop=7900, samples_hf_crop=100)
        out_scan[:,:,scan] = bScan
    del data
    np.asarray(out_scan)
    # plt.imshow( np.mean(out_scan, axis=0 ))
    # plt.show()
    # plt.pause(1)
    plt.imshow(ORM._run_reconstruction(buffer, wind_key='hann', 
        disp_coeffs=d_coeffs, blck_lvl=b_lvl, scale_fac=scaling, 
        samples_dc_crop=0, samples_hf_crop=0))
    plt.show()
    plt.pause(0.25)
    plt.imshow(ORM._run_reconstruction(buffer, wind_key='hann', 
        disp_coeffs=d_coeffs, blck_lvl=b_lvl, scale_fac=scaling, 
        samples_dc_crop=0, samples_hf_crop=0))
    plt.show()


def reconstruct_and_write_cropped_vol_2disk(samples_dc_crop=100, samples_hf_crop=7900, index = 0, roll_offset=35) -> None :
    ORM = OctReconstructionManager(dtype_loading='<u2')
    data = ORM.load_oct_data()
    new_dims = ((data.shape[0]-samples_dc_crop-samples_hf_crop), data.shape[1], data.shape[2])
    out_scan = np.zeros((new_dims))
    print(f"Data size of reconstructed cube = {out_scan.size//1024//1024} MBytes")
    t1 = time.time()
    for scan in tqdm(range(512)) :
        buffer = data[:,:,scan]
        bScan = ORM._run_reconstruction(buffer, wind_key='hann', 
        disp_coeffs=(-8, 121, 0, 0), blck_lvl=80, 
        samples_dc_crop=samples_dc_crop, samples_hf_crop=samples_hf_crop)
        out_scan[:,:,scan] = bScan
    print(f"Took {round((time.time()-t1)/60)} mins to reconstruct volume")
    del data
    np.asarray(out_scan)
    out_scan = np.roll(np.asarray(out_scan), roll_offset, axis=-1)
    save_file_name = f"ReconVol_{index}_{out_scan.shape[0]}x{out_scan.shape[1]}x{out_scan.shape[2]}_.bin"
    print(f"Took {round((time.time()-t1)/60)} mins to process entire volume")
    out_scan.astype('uint8').tofile( os.path.join(ORM._tk_folder_selection, save_file_name) )

def load_reconstructed_oct_volume(data_shape=(5312, 512, 512)) -> np.array :
    ORM = OctReconstructionManager(dtype_loading='<u1')
    data = np.asarray(np.fromfile(ORM._tk_file_selection(), dtype='>u1'))
    data = data.reshape(data_shape)
    plt.imshow( data[:,:,256] )
    plt.show()
    return data


def run() :
    print("[INFO:] Running from processrastercapturescan.py")

    # check_display_size_and_bScan_offset()
    
    samples_dc_crop=100
    samples_hf_crop= 13313-samples_dc_crop-5699
    print(samples_hf_crop)

    reconstruct_and_write_cropped_vol_2disk(samples_dc_crop=samples_dc_crop, 
    samples_hf_crop=samples_hf_crop, index=1, roll_offset=29)

    # load_reconstructed_oct_volume()    

if __name__ == '__main__':
    run()