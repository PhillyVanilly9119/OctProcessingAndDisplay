"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                         
        >>> Contains methods and functionality for OCT data reconstruction     
                                
"""

###################################################################################
# DEPRECATED FUNCTIONS - RECONSTRUCTION WILL BE THE SCRIPT CONTAINING ALL FUNCTIONS
###################################################################################

# global imports
import os
import time
import numpy as np
from scipy import signal
from random import random
import matplotlib.pyplot as plt

# custom imports
import data_io as DataIO

class OctReconstructionManagager(DataIO.OctDataFileManager) :
    def __init__(self, is_user_file_selection: bool, file_path_main: str, dtype) -> None:
        super().__init__(is_user_file_selection=is_user_file_selection, file_path_main=file_path_main, dtype=dtype)
        self.dtype_raw = dtype
        self.dtype_recon = 'uint8'
    
    def adjust_dim_for_processing(self, buffer, vector) -> np.array :
        """ evaluate and prepare buffer and vector for numpy matrix-vector operations """
        if buffer.ndim == 1 :
            return np.asarray(buffer), np.asarray(vector)     
        elif buffer.ndim == 2 :
            return np.asarray(buffer), np.asarray(vector[:, np.newaxis])
        elif buffer.ndim == 3 :
            return np.asarray(buffer), np.asarray(vector[:, np.newaxis, np.newaxis])
        else : 
            print("[DIMENSIONALITY WARNING:] returning empty array (dimensionality neither 1,2 or 3)")
            return []
            
    def return_nDim_indepentent_averaged_vec(self, buffer) -> np.array :
        """ returns 1D-vector of with the length of an a-Scan containing averaged samples (for i.e. BG-Sub.)"""
        if buffer.ndim == 1 : 
            print("[CAUTION] return vector is equivalent to input/a-Scan (1D array)")
            return buffer
        elif buffer.ndim == 2 :
            return np.average(buffer, axis=1)
        elif buffer.ndim == 3 :
            return np.average(buffer, axis=(1,2))
        else : # TODO: check if necessary, since preprocessing should take care of that
            raise ValueError("[DIMENSION ERROR] of OCT array")
    
    def substract_background(self, buffer, background=None) :
            """ Returns denoised OCT buffer (corresponding to sampling) """
            if not background : # calculate background from buffer, if it is None
                background = self.average_nDim_independent(buffer)
            return np.subtract( *self.adjust_dim_for_processing(buffer, background), dtype=self.dtype_raw )
        
    # TODO: Think which reconstruction parameters are needed
    



### OCT RECONSTRUCTION OPERATIONS ###

def create_disperion(a_len, coeffs) :
        """
        >>> creates real-valued polynominal to correct for dispersion mismatches 
        """
        return np.asarray(np.polyval(coeffs, np.linspace(-0.5, 0.5, a_len)))

def create_window(a_len, key=None) :
        """
        >>> Creates a real-valued vector to spectrally shape a raw OCT A-Scan
        """
        if key.lower() == 'hann' :
                print("Using Hann-Window")
                return np.hanning(a_len)
        elif key.lower() == 'hamm' :
                print("Using Hamming-Window")    
                return np.hamming(a_len)
        elif key.lower() == 'kaiser' :
                print("Using Kaiser-Window")
                return np.kaiser(a_len)
        elif key.lower() == 'gauss' :
                print("Using Gaussian-Window")
                return signal.gaussian(a_len, round(a_len/10))
        else :
                raise ValueError("You have passed an unrecognized key for the windowing-parameter")

def apply_dispersion_correction(scan, coeffs) :
        """
        >>> Creates and applies (complex-valued) dispersion correction to OCT data
        """
        # error handling
        assert np.size(coeffs) == 4, "[DIMENSION ERROR] the disperison coefficients must be a tuple of 4 values"
        # create windowing-function
        disp_poly = create_disperion(np.shape(scan)[0], coeffs)
        disp = np.exp(1j*disp_poly) 
        # apply vectorized windowing 
        _, disp = DataIO.preprocess_dimensionality(scan, disp)
        return np.asarray(np.multiply(scan, disp), 
                          dtype=np.complex64)      

def apply_windowing(scan, key='hann') :
        """
        >>> Apply filter windows to spectrally shape OCT raw signals
        -> returns windowed OCT-scan
        """
        dims = np.shape(scan)
        disp_wind = np.asarray(np.zeros_like(scan), dtype=np.complex64)
        a_len = dims[0]       
        print(a_len)
        window = create_window(a_len, key=key)
        return window
        _, window = DataIO.preprocess_dimensionality(scan, window)
        # TODO: Which return is more valid
        disp_wind.real = np.asarray(np.multiply(scan, np.cos(window)), dtype=np.complex64)
        disp_wind.imag = np.asarray(np.multiply(scan, np.sin(window)), dtype=np.complex64)
        assert np.dtype(disp_wind) == np.complex64, "Wrong data type before return in apply_windowing"
        return np.asarray(disp_wind)
        # return np.asarray(np.multiply(scan, np.exp(1j*window)), 
        #                   dtype=np.complex64)  
        
def create_and_save_dispersion(path, a_len, coeffs) :
        """
        >>> Creates and saves a dispersion vector to the specified path 
        """
        disp = create_disperion(a_len, coeffs)
        full_path = os.path.join(path, ('dispersion_' + a_len + '.bin'))
        try :
                disp.tofile(full_path).astype(np.complex64)
        except TypeError as err :
                print("Dispersion vector is not a numpy-ndarray ", err)
        finally:
                np.asarray(disp, dtype=np.complex64).tofile(full_path).astype(np.complex64)
                print(f"Saved dispersion vector in <{full_path}>")        

def apply_spectral_shaping(scan, disp_coeffs, key=None) :
        a_len = np.shape(scan)[0]
        if key is not None :
                print(f"Applying {key}-windowed spectral shaping and dispersion correction") 
                window = np.asarray(np.multiply(create_window(a_len, key=key), 
                                                create_disperion(a_len, disp_coeffs)), 
                                    dtype=np.complex64) # create and dot the window- and dispersion-vector
                _, window = DataIO.preprocess_dimensionality(scan, create_disperion(a_len, disp_coeffs)) 
                return np.asarray(np.multiply(scan, np.exp(1j*window)), 
                                  dtype=np.complex64)  
        else :
                print("Applying dispersion correction")
                _, window = DataIO.preprocess_dimensionality(scan, create_disperion(a_len, disp_coeffs)) # create dispersion vector
                return np.asarray(np.multiply(scan, np.exp(1j*window)), 
                        dtype=np.complex64)  

def apply_spectral_splitting(data, split_factor, dtype=np.complex64) :
        """
        >>> Reshapes B-Scan like data buffer according to spectral splitting requirements
        """
        dims = np.shape(data)
        return np.asarray(np.reshape(data, ((int(dims[0]/split_factor)), 
                                            int(split_factor*dims[1]))), dtype=dtype)

def perform_fft(scan) :
        """
        >>> Apply IDFT to pre-processed OCT data and return result of transform
        -> Zero-Padding and cropping are applied  
        """
        a_len = np.shape(scan)[1]
        if np.size(np.shape(scan)) == 1 : 
                transformed_scan = np.zeros(shape=(np.shape(scan)), 
                                            dtype=np.complex64)
                transformed_scan = np.asarray(np.pad(scan, 
                                                     ((a_len, 0)), 
                                                     mode='constant'))
                transformed_scan[a_len:] = scan
        elif np.size(np.shape(scan)) == 2 :
                transformed_scan = np.zeros(shape=(np.shape(scan)), 
                                            dtype=np.complex64)
                transformed_scan = np.asarray(np.pad(scan, 
                                                     ((a_len, 0), (0, 0)), 
                                                     mode='constant'))
        elif np.size(np.shape(scan)) == 3 :
                transformed_scan = np.zeros(shape=(np.shape(scan)), 
                                            dtype=np.complex64)
                transformed_scan = np.asarray(np.pad(scan, 
                                                     ((a_len, 0), (0, 0), (0, 0)), 
                                                     mode='constant'))
        else : # TODO: check if necessary, since preprocessing should take care of that
                raise ValueError("[DIMENSION ERROR] of OCT volume")
        return np.asarray(np.abs(np.fft.ifft(transformed_scan, axis=0))[a_len:],
                          dtype=np.uint8)
        
def abs_and_log(scan, is_scale_dynamic_range=False) :
        """
        >>> Rescale the reconstructed OCT scans 
        """
        if is_scale_dynamic_range :
                # Why doesnt this work in Python if value>0 ?
                BLACK_LVL = 0
                RECON_RNG = 64
                return np.asarray(255 * np.true_divide(np.nan_to_num(20*np.log10(scan) - BLACK_LVL), RECON_RNG), dtype=np.uint8)
        else :
                return np.asarray(20*np.log10(np.abs(scan)), dtype=np.uint8)

def reconstruct(disp_coeffs,
                file_name=None, 
                key=None, 
                cropped_range=100, 
                spectral_split_factor=1, 
                is_apply_windowing=False, 
                is_substract_background=True) :
        """
        >>> MACRO for function calls that perform SS OCT-reconstruction 
        """
        # Load data file
        if file_name is not None :
                path = os.path.join(f"{file_name.split('/')[0]}\\", *file_name.split('/')[1:-1])
                folder = file_name.split('/')[-1]
        else :
                path, folder = DataIO.get_usr_selected_file()
        raw_buffer = DataIO.load_data_from_bin(path, folder, is_dim_appendix=True, is_reshaping_array=True)
        return raw_buffer
        # Pre-Processing options
        if is_substract_background:
                raw_buffer = substract_background(raw_buffer)
        if is_apply_windowing :
                raw_buffer = apply_spectral_shaping(raw_buffer, disp_coeffs, key=key)
        else :
                raw_buffer = apply_dispersion_correction(raw_buffer, disp_coeffs)
        if spectral_split_factor != 1 :
                raw_buffer = apply_spectral_splitting(raw_buffer, spectral_split_factor)
        # FFT
        oct_data = perform_fft(raw_buffer)
        # Scale for display
        oct_data = abs_and_log(oct_data, is_scale_dynamic_range=True)
        print(f"Reconstructed buffer with displayable size={np.shape(oct_data)}")
        return oct_data

# TODO: Check why background subtraction causes overflow... 
# -> Weird artifacts in A-Scans cause BG-Vector to look weird... Maybe BG should be calced differently
# TODO: Check handling of return data types
# TODO: Dispersion Compensation doesnt seem to be working

def main() :
        file_name = 'C:/Users/Philipp/Desktop/out_before_2048x1024.bin'
        coeffs = (-21,140,0,0)
        path = os.path.join(f"{file_name.split('/')[0]}\\", *file_name.split('/')[1:-1])
        folder = file_name.split('/')[-1]

        # data = reconstruct((coeffs), file_name=os.path.join(path, folder))

if __name__ == '__main__' :
        main()
        
# =============================================================================
# data = DataIO.load_data_from_bin(path, folder, is_dim_appendix=True, is_reshaping_array=True)
# =============================================================================

# vec = np.linspace(-300, 300, num=61)
# for _, num in enumerate(vec) :
#         data = reconstruct((0,num,0,0), file_name=file_name, key='hann', cropped_range=50, spectral_split_factor=1,  
#                         is_substract_background=False, is_apply_windowing=True)
#         plt.imshow(np.abs(data))
#         plt.show(block=False)  
#         plt.savefig(os.path.join(r'C:\Users\Philipp\Desktop\Dispersion', f'cube_{num}.bmp'))
#         plt.pause(1)
#         plt.close()

### APPENDIX ###    
# def consecutive(data, stepsize=1):
#     return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

# def rand(start, end, num): 
#     res = [] 
#     for _ in range(num): 
#         res.append(random.randint(start, end)) 
#     return np.array(res)