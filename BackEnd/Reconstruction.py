"""

                File containing functions for FD-domain OCT data reconstruction

        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 

"""

import os
import numpy as np
import matplotlib.pyplot as plt

##############
### MACROS ###
##############
def reshape_data_after_dims(data, file_name, is_dims_in_file_name=True) :
    """
    reshapes data according to its supposed dimensionality
    -> flag assumes a file name in the format <name_ZxXxY.bin> (in optical dimensions) 
    """
    if is_dims_in_file_name :
        intermediate_name = file_name.split('_')[-1].split('.bin')
        string_dims = intermediate_name[0]
        dims = string_dims.split('x')
    else :
        print("[CAUTION:] Logic not yet implemented!")
        pass
    print(tuple(dims))

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
    shape = np.shape(data)
    aLen = shape[2]
    out_data = np.zeros_like(data, dtype=np.uint16)

##########################
### POST-FFT FUNCTIONS ###
##########################
def abs_and_log(data) :
    out_data = np.zeros_like(data)
    # Continue here
    out_data = np.asarray(20 * np.log10(data), dtype=np.uint16)

def rescale_grey_values(data, black_lvl, scale_factor) :
    shape = np.shape(data)
    aLen = shape[2]
    out_data = np.zeros_like(data, dtype=np.uint8)
    out_data = np.asarray(255 * np.divide((np.subtract(data, black_lvl)), scale_factor))



# TODO: Copy and adapt all reconstruction functions to the scheme developed above 

### Testing ###
if __name__ == "__main__" :
    string = "data_1024x512x128.bin"
    reshape_data_after_dims(np.zeros((1,1,1)), string)


# def substract_background(scan, background=None) :
#         """
#         >>> Returns noise-reduced OCT-data as uint16 (corresponding to sampling)
#         """
#         if background is not None : 
#                 background = background
#         else :   
#                 background = DataIO.average_nDim_independent(scan)
#         _, background = DataIO.preprocess_dimensionality(scan, background)
#         return np.asarray(np.subtract(scan, background), 
#                           dtype=np.uint16)

# def create_disperion(a_len, coeffs) :
#         """
#         >>> creates real-valued polynominal to correct for dispersion mismatches 
#         """
#         return np.asarray(np.polyval(coeffs, np.linspace(-0.5, 0.5, a_len)))

# def create_window(a_len, key=None) :
#         """
#         >>> Creates a real-valued vector to spectrally shape a raw OCT A-Scan
#         """
#         if key.lower() == 'hann' :
#                 print("Using Hann-Window")
#                 return np.hanning(a_len)
#         elif key.lower() == 'hamm' :
#                 print("Using Hamming-Window")    
#                 return np.hamming(a_len)
#         elif key.lower() == 'kaiser' :
#                 print("Using Kaiser-Window")
#                 return np.kaiser(a_len)
#         elif key.lower() == 'gauss' :
#                 print("Using Gaussian-Window")
#                 return signal.gaussian(a_len, round(a_len/10))
#         else :
#                 raise ValueError("You have passed an unrecognized key for the windowing-parameter")

# def apply_dispersion_correction(scan, coeffs) :
#         """
#         >>> Creates and applies (complex-valued) dispersion correction to OCT data
#         """
#         # error handling
#         assert np.size(coeffs) == 4, "[DIMENSION ERROR] the disperison coefficients must be a tuple of 4 values"
#         # create windowing-function
#         disp_poly = create_disperion(np.shape(scan)[0], coeffs)
#         disp = np.exp(1j*disp_poly) 
#         # apply vectorized windowing 
#         _, disp = DataIO.preprocess_dimensionality(scan, disp)
#         return np.asarray(np.multiply(scan, disp), 
#                           dtype=np.complex64)      

# def apply_windowing(scan, key='hann') :
#         """
#         >>> Apply filter windows to spectrally shape OCT raw signals
#         -> returns windowed OCT-scan
#         """
#         dims = np.shape(scan)
#         disp_wind = np.asarray(np.zeros_like(scan), dtype=np.complex64)
#         a_len = dims[0]       
#         print(a_len)
#         window = create_window(a_len, key=key)
#         return window
#         _, window = DataIO.preprocess_dimensionality(scan, window)
#         # TODO: Which return is more valid
#         disp_wind.real = np.asarray(np.multiply(scan, np.cos(window)), dtype=np.complex64)
#         disp_wind.imag = np.asarray(np.multiply(scan, np.sin(window)), dtype=np.complex64)
#         assert np.dtype(disp_wind) == np.complex64, "Wrong data type before return in apply_windowing"
#         return np.asarray(disp_wind)
#         # return np.asarray(np.multiply(scan, np.exp(1j*window)), 
#         #                   dtype=np.complex64)  
        
# def create_and_save_dispersion(path, a_len, coeffs) :
#         """
#         >>> Creates and saves a dispersion vector to the specified path 
#         """
#         disp = create_disperion(a_len, coeffs)
#         full_path = os.path.join(path, ('dispersion_' + a_len + '.bin'))
#         try :
#                 disp.tofile(full_path).astype(np.complex64)
#         except TypeError as err :
#                 print("Dispersion vector is not a numpy-ndarray ", err)
#         finally:
#                 np.asarray(disp, dtype=np.complex64).tofile(full_path).astype(np.complex64)
#                 print(f"Saved dispersion vector in <{full_path}>")        

# def apply_spectral_shaping(scan, disp_coeffs, key=None) :
#         a_len = np.shape(scan)[0]
#         if key is not None :
#                 print(f"Applying {key}-windowed spectral shaping and dispersion correction") 
#                 window = np.asarray(np.multiply(create_window(a_len, key=key), 
#                                                 create_disperion(a_len, disp_coeffs)), 
#                                     dtype=np.complex64) # create and dot the window- and dispersion-vector
#                 _, window = DataIO.preprocess_dimensionality(scan, create_disperion(a_len, disp_coeffs)) 
#                 return np.asarray(np.multiply(scan, np.exp(1j*window)), 
#                                   dtype=np.complex64)  
#         else :
#                 print("Applying dispersion correction")
#                 _, window = DataIO.preprocess_dimensionality(scan, create_disperion(a_len, disp_coeffs)) # create dispersion vector
#                 return np.asarray(np.multiply(scan, np.exp(1j*window)), 
#                         dtype=np.complex64)  

# def apply_spectral_splitting(data, split_factor, dtype=np.complex64) :
#         """
#         >>> Reshapes B-Scan like data buffer according to spectral splitting requirements
#         """
#         dims = np.shape(data)
#         return np.asarray(np.reshape(data, ((int(dims[0]/split_factor)), 
#                                             int(split_factor*dims[1]))), dtype=dtype)

# def perform_fft(scan) :
#         """
#         >>> Apply IDFT to pre-processed OCT data and return result of transform
#         -> Zero-Padding and cropping are applied  
#         """
#         a_len = np.shape(scan)[1]
#         if np.size(np.shape(scan)) == 1 : 
#                 transformed_scan = np.zeros(shape=(np.shape(scan)), 
#                                             dtype=np.complex64)
#                 transformed_scan = np.asarray(np.pad(scan, 
#                                                      ((a_len, 0)), 
#                                                      mode='constant'))
#                 transformed_scan[a_len:] = scan
#         elif np.size(np.shape(scan)) == 2 :
#                 transformed_scan = np.zeros(shape=(np.shape(scan)), 
#                                             dtype=np.complex64)
#                 transformed_scan = np.asarray(np.pad(scan, 
#                                                      ((a_len, 0), (0, 0)), 
#                                                      mode='constant'))
#         elif np.size(np.shape(scan)) == 3 :
#                 transformed_scan = np.zeros(shape=(np.shape(scan)), 
#                                             dtype=np.complex64)
#                 transformed_scan = np.asarray(np.pad(scan, 
#                                                      ((a_len, 0), (0, 0), (0, 0)), 
#                                                      mode='constant'))
#         else : # TODO: check if necessary, since preprocessing should take care of that
#                 raise ValueError("[DIMENSION ERROR] of OCT volume")
#         return np.asarray(np.abs(np.fft.ifft(transformed_scan, axis=0))[a_len:],
#                           dtype=np.uint8)
        
# def abs_and_log(scan, is_scale_dynamic_range=False) :
#         """
#         >>> Rescale the reconstructed OCT scans 
#         """
#         if is_scale_dynamic_range :
#                 # Why doesnt this work in Python if value>0 ?
#                 BLACK_LVL = 0
#                 RECON_RNG = 64
#                 return np.asarray(255 * np.true_divide(np.nan_to_num(20*np.log10(scan) - BLACK_LVL), RECON_RNG), dtype=np.uint8)
#         else :
#                 return np.asarray(20*np.log10(np.abs(scan)), dtype=np.uint8)

# def reconstruct(disp_coeffs,
#                 file_name=None, 
#                 key=None, 
#                 cropped_range=100, 
#                 spectral_split_factor=1, 
#                 is_apply_windowing=False, 
#                 is_substract_background=True) :
#         """
#         >>> MACRO for function calls that perform SS OCT-reconstruction 
#         """
#         # Load data file
#         if file_name is not None :
#                 path = os.path.join(f"{file_name.split('/')[0]}\\", *file_name.split('/')[1:-1])
#                 folder = file_name.split('/')[-1]
#         else :
#                 path, folder = DataIO.get_usr_selected_file()
#         raw_buffer = DataIO.load_data_from_bin(path, folder, is_dim_appendix=True, is_reshaping_array=True)
#         return raw_buffer
#         # Pre-Processing options
#         if is_substract_background:
#                 raw_buffer = substract_background(raw_buffer)
#         if is_apply_windowing :
#                 raw_buffer = apply_spectral_shaping(raw_buffer, disp_coeffs, key=key)
#         else :
#                 raw_buffer = apply_dispersion_correction(raw_buffer, disp_coeffs)
#         if spectral_split_factor != 1 :
#                 raw_buffer = apply_spectral_splitting(raw_buffer, spectral_split_factor)
#         # FFT
#         oct_data = perform_fft(raw_buffer)
#         # Scale for display
#         oct_data = abs_and_log(oct_data, is_scale_dynamic_range=True)
#         print(f"Reconstructed buffer with displayable size={np.shape(oct_data)}")
#         return oct_data

# # TODO: Check why background subtraction causes overflow... 
# # -> Weird artifacts in A-Scans cause BG-Vector to look weird... Maybe BG should be calced differently
# # TODO: Check handling of return data types
# # TODO: Dispersion Compensation doesnt seem to be working
