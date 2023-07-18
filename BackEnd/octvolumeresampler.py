"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2023 
                                        ******
                                         
        >>> Contains methods and functionality for OCT volume resampling      
                                
"""

# global imports
import os
import sys
import numpy as np
from tqdm import tqdm
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
# import cv2 # debug

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend')))

from octreconstructionmanager import OctReconstructionManager as REC

class OctVolumeResmapler():
    def __init__(self, vol: np.array) -> None:
        assert vol.ndim == 3
        self.vol = vol        

    def resample_volume(self, scaling: tuple, is_crop: bool, crop: tuple):
        assert len(scaling) == 3, "Wrong dimension of crop-index tuple -> expected 3 enties tuple"
        assert len(crop) == 6, "Wrong dimension of crop-index tuple -> expected 6 enties tuple"
        if scaling[1] != scaling[2]:
            print(f"[WARNING:] You are about to rescale the lateral dimensions with different factors (b={scaling[1]}, c={scaling[2]})")
        out_size = [int(np.rint(a * b)) for a, b in zip(self.vol.shape, scaling)]
        out_size = tuple(out_size)
        print(f"[INFO:] Resizing input volume of size={self.vol.shape} to output size={out_size}")
        print("Busy...")
        out_vol = np.zeros((out_size))
        out_vol = zoom(self.vol, (scaling))
        print("Done reshaping volume!")
        print(out_vol.shape)
        fig, ax = plt.subplots(1,3)
        ax[0].imshow(np.mean(out_vol, axis=0), cmap='gray')
        ax[1].imshow(out_vol[:,out_vol.shape[1]//2,:], cmap='gray')
        ax[2].imshow(out_vol[:,:,out_vol.shape[2]//2], cmap='gray')
        plt.show()
        # if is_crop:
        #     x_min = crop[0]
        #     x_max = crop[1]
        #     y_min = crop[2]
        #     y_max = crop[3]
        #     z_min = crop[4]
        #     z_max = crop[5]
        #     assert x_max-x_min >= 0, f"Dimension mismatch for x-cropping -> {x_max}-{x_min}<0"
        #     assert y_max-y_min >= 0, f"Dimension mismatch for y-cropping -> {y_max}-{y_min}<0"
        #     assert z_max-z_min >= 0, f"Dimension mismatch for z-cropping -> {z_max}-{z_min}<0"

        


if __name__ == '__main__' :
    print("[INFO:] Running from < octvolumeresampler.py > ...")
    
    path = r"/home/zeiss/Data_Tachyoptes/rasterVol3xAVG_4000x512x511_recon.bin"
    with open(path, 'r') as f:
        vol = np.fromfile(f, dtype=np.uint8)
        vol = vol.reshape((511,512,4000))
    
    vol = vol.swapaxes(0,2)
    
    
    RESAMPLE = OctVolumeResmapler(vol)
    RESAMPLE.resample_volume((6.9/15.6, 1, 1), is_crop=False, crop=(0,0,0,0,0,0))