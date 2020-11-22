"""

                File containing functions for FD-domain OCT data reconstruction

        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 

"""

import os
import numpy as np
import matplotlib.pyplot as plt

################
### DATA I/O ###
################
def load_data_from_bin_file(path, dtype) :
    pass

def load_image(path, dims, dtype) :
    pass

def load_data_from_images(path, dims, dtype) :
    pass

def save_data_as_images(path, data, dims, dtype) :
    pass

def save_data_as_bin_file(path, data, save_dtype=np.uint8) :
    pass

#########################
### PRE-FFT FUNCTIONS ###
#########################
def subtract_background(data) :
    pass

def apply_windowing(data, window='gauss') :
    pass

###########
### FFT ###
###########
def apply_fft(data) :
    pass

def apply_cropped_fft(data, ratio=0.5) :
    pass

##########################
### POST-FFT FUNCTIONS ###
##########################
def rescale_grey_values(data, black_lvl, scale_factor) :
    shape = np.shape(data)
    aLen = shape[2]
    out_data = np.zeros_like(data, dtype=np.uint8)
    out_data = np.asarray(255 * np.divide((np.subtract(data, black_lvl)), scale_factor))
