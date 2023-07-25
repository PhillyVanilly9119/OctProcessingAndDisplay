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


# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend'))) # TBD


class OctVolumeResmapler():
    """Class to reshape 3D OCT volumes 
    """
    def __init__(self, vol: np.array) -> None:
        assert vol.ndim == 3
        self.vol = vol        

    def resample_volume(self, scaling: tuple, is_crop: bool, crop: tuple) -> np.array:
        """Method that takes an OCT volume (reshaped properly with its optical axis notation (z,x,y))
        and interpolates its output size as (Z * scaling.z, X * scaling.x, Y * scaling.y), with an option 
        to crop (!!!) the reshaped volume, i.e. crops in voxels corresponding to output size and shape

        Args:
            scaling (tuple): 3-valued tuple, scaling as factors relative to input dimensional sizes (1,1,1)
            is_crop (bool): flag as to wether or not to crop the output volume
            crop (tuple): cropping values in voxels (z_min, z_max, x_min, x_max, y_min, y_max) 
            in output volume voxel sizes

        Returns:
            np.array: reshaped OCT volume array
        """
        in_vol_size = self.vol.shape
        assert len(scaling) == 3, "Wrong dimension of crop-index tuple -> expected 3 enties tuple"
        assert len(crop) == 6, "Wrong dimension of crop-index tuple -> expected 6 enties tuple"
        if scaling[1] != scaling[2]:
            print(f"[WARNING:] You are about to rescale the lateral dimensions with different factors (b={scaling[1]}, c={scaling[2]})")
        out_size = [int(np.rint(a * b)) for a, b in zip(self.vol.shape, scaling)]
        out_size = tuple(out_size)
        print(f"[INFO:] Resizing input volume of size={self.vol.shape} to output size={out_size}")
        print("Busy...")
        intermediate_vol = np.zeros((out_size[0], in_vol_size[1], in_vol_size[2]))
        # iterate through z-stack in input dimensions and only resample optical z-direction 
        for xy_slice in tqdm(range(in_vol_size[2])):
            intermediate_vol[...,xy_slice] = zoom(self.vol[...,xy_slice], (scaling[0], 1)) # use original volume data and onyl interpolate z-directions
        out_vol = np.zeros((out_size)) # allocate final output volume buffer
        # iterate through the z-stack and resize the cube laterally to new output dimensions
        for z_slice in tqdm(range(out_size[0])): 
             out_vol[z_slice,...] = zoom(intermediate_vol[z_slice,...], (scaling[1], scaling[2])) # use intermediate volume and scale laterally to output size
        del intermediate_vol # free memory
        print("Done reshaping volume!")
        print(out_vol.shape) # debug
        fig, ax = plt.subplots(1,3) # sanity check
        ax[0].imshow(np.mean(out_vol, axis=0), cmap='gray')
        ax[1].imshow(out_vol[:,out_vol.shape[1]//2,:], cmap='gray')
        ax[2].imshow(out_vol[:,:,out_vol.shape[2]//2], cmap='gray')
        plt.show()
        if is_crop: # crop boundaries (according to resized, i.e. output volume shape)
            x_min = crop[0]
            x_max = crop[1]
            assert x_max-x_min >= 0, f"Dimension mismatch for x-cropping -> {x_max}-{x_min} < 0 ..."
            assert x_max+x_min <= out_size[1], f"Dimension mismatch for x-cropping -> cropped area ({x_max}+{x_min}) larger than volume dim {out_size[1]} ..."
            y_min = crop[2]
            y_max = crop[3]
            assert y_max-y_min >= 0, f"Dimension mismatch for x-cropping -> {y_max}-{y_min} < 0 ..."
            assert y_max+y_min <= out_size[2], f"Dimension mismatch for x-cropping -> cropped area ({y_max}+{y_min}) larger than volume dim {out_size[2]} ..."
            z_min = crop[4]
            z_max = crop[5]
            assert z_max-z_min >= 0, f"Dimension mismatch for x-cropping -> {z_max}-{z_min} < 0 ..."
            assert z_max+z_min <= out_size[0], f"Dimension mismatch for x-cropping -> cropped area ({z_max}+{z_min}) larger than volume dim {out_size[0]} ..."
            return out_vol[z_min:out_size[0]-z_max, x_min:out_size[1]-x_max, y_min:out_size[2]-y_max]
        return out_vol
        


if __name__ == '__main__' :
    print("[INFO:] Running from < octvolumeresampler.py > ...")
    
    path = r"C:\Users\phili\Downloads\rasterVol01_4000x512x511_recon_denoised.bin"
    with open(path, 'r') as f:
        vol = np.fromfile(f, dtype=np.uint8)
        vol = vol.reshape((511, 512, 4000))
        print(vol.shape)
        vol = np.rollaxis(vol, 2)
        print(vol.shape)
        plt.imshow(np.mean(vol, axis=0), cmap="gray")
        plt.show()


    RESAMPLE = OctVolumeResmapler(vol)
    res_vol = RESAMPLE.resample_volume((6.9/15.6, 1, 1), is_crop=False, crop=(5,5,0,0,0,0))
    file_dims = f"_{res_vol.shape[0]}x{res_vol.shape[1]}x{res_vol.shape[2]}_"
    new_file_name = path.split("_")[0] + file_dims + '.bin'
    res_vol.astype(np.uint8).tofile(new_file_name)