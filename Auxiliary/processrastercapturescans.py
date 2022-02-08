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
import cv2
import time
from numpy.core.fromnumeric import shape
from numpy.core.numeric import roll
from tqdm import tqdm
from typing import List
import numpy as np
import matplotlib.pyplot as plt

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'FrontEnd')))

from octreconstructionmanager import OctReconstructionManager
# from guiconfigdatamanager import GuiConfigDataManager

def run_recon_on_raster_scan(d_coeffs, black_level, display_scale, wind_key, 
                             samples_dc_crop, samples_hf_crop) :
    """ Reconstructs an entire volume buffer from single *.BIN-file """    
    ORM = OctReconstructionManager( dtype_loading='<u2' )
    data = ORM.load_oct_data()
    new_dims = ( (data.shape[0]-samples_dc_crop-samples_hf_crop), data.shape[1], data.shape[2] )
    t1 = time.perf_counter()
    out_scan = np.zeros( (new_dims) )
    print(f" Data size of reconstructed cube = {out_scan.size//1024//1024} MBytes")
    for scan in tqdm(range(data.shape[-1])) :
        buffer = data[:,:,scan]
        bScan = ORM._run_reconstruction(buffer, wind_key=wind_key, 
                                        disp_coeffs=d_coeffs, blck_lvl=black_level, scale_fac=display_scale,
                                        samples_dc_crop=samples_dc_crop, samples_hf_crop=samples_hf_crop)
        out_scan[:,:,scan] = bScan
    plt.imshow(cv2.resize(out_scan[:,:,256], (400, 330)), cmap='gray')
    plt.show()
    print(f" Took {round((time.perf_counter()-t1) / 60)} mins to reconstruct volume")
    return np.asarray( out_scan ), np.asarray( buffer )

def check_display_size_and_bScan_offset(d_coeffs, black_level, display_scale, wind_key, 
                                        samples_dc_crop, samples_hf_crop) -> None :
    out_scan, buffer = run_recon_on_raster_scan(wind_key=wind_key, disp_coeffs=d_coeffs, blck_lvl=black_level, 
                                                scale_fac=display_scale, samples_dc_crop=samples_dc_crop,
                                                samples_hf_crop=samples_hf_crop)
    middle_bScan = OctReconstructionManager()._run_reconstruction(buffer=out_scan[:, :, out_scan.shape[-1//2]], 
                                                                  disp_coeffs=d_coeffs, wind_key=wind_key, 
                                                                  samples_hf_crop=0, samples_dc_crop=0, 
                                                                  scale_fac=display_scale, 
                                                                  blck_lvl=black_level)
    np.asarray( out_scan )
    plt.imshow( np.mean(out_scan, axis=0) )
    plt.show()
    plt.pause(10)
    plt.imshow( )
    plt.draw()
    plt.show()

def reconstruct_and_write_cropped_vol_2disk(path, d_coeffs=(8,-121,0,0), b_lvl=80, samples_dc_crop=100, samples_hf_crop=0, 
                                            index = 0, display_scale=63.75, roll_offset=35) -> None :
    cropped_aScans = 13312 - samples_dc_crop - samples_hf_crop
    print(f"")
    out_scan, _ = run_recon_on_raster_scan(d_coeffs=d_coeffs, black_level=b_lvl, wind_key='hann', display_scale=display_scale,
                                           samples_dc_crop=samples_dc_crop, samples_hf_crop=samples_hf_crop)
    out_scan = np.roll( np.asarray(out_scan), roll_offset, axis=-1 )
    save_file_name = f"ReconVol_{index}_{out_scan.shape[0]}x{out_scan.shape[1]}x{out_scan.shape[2]}_.bin"
    print(f"cropped samples = {cropped_aScans} and out a dims = {out_scan.shape[0]}")
    out_scan.astype('uint8').tofile( os.path.join(path, save_file_name) )

def load_reconstructed_oct_volume( data_shape=(5312, 512, 512) ) -> np.array :
    ORM = OctReconstructionManager( dtype_loading='<u1' )
    data = np.asarray( np.fromfile(ORM._tk_file_selection(), dtype='>u1') )
    data = data.reshape( data_shape )
    plt.imshow( np.mean(data, axis=0) )
    plt.show()
    plt.pause(10)
    plt.imshow( data[:, :, data.shape[-1]//2] )
    plt.show()
    return data

def resample_reconstruced_volume( in_shape, is_flip_aScnas=True ) -> np.array :
    ORM = OctReconstructionManager( dtype_loading='<u1' )
    in_data = np.asarray( np.fromfile(ORM._tk_file_selection(), dtype='>u1') )
    in_data = in_data.reshape( in_shape )
    # print(in_data.shape)
    plt.imshow( in_data[:, :, in_data.shape[-1]//2] )
    plt.show()
    re_dims = (in_data.shape[0]//4, in_data.shape[1], in_data.shape[-1])
    # print(re_dims)
    out_data = np.zeros( (re_dims), dtype='uint8' )
    for bScan in tqdm(range(in_data.shape[-1])) :
        out_data[:,:,bScan] = cv2.resize( in_data[:,:,bScan], (re_dims[1], re_dims[0]), cv2.INTER_CUBIC )
    if is_flip_aScnas :
        return np.asarray( out_data[::-1,:,:] )
    return np.asarray( out_data )    

def run() : 
    print("[INFO:] Running from processrastercapturescan.py")

       
if __name__ == '__main__':
    run()