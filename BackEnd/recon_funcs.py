"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2021 Medical University of Vienna 
                                        ******
                                         
        >>> Contains methods and functionality for OCT data reconstruction     
                                
"""

# global imports
import numpy as np
from numpy.lib.nanfunctions import nanmedian
from scipy import signal
import matplotlib.pyplot as plt

# custom imports
import data_io as IO

class OctReconstructionManager(IO.OctDataFileManager) :
    def __init__(self, dtype_loading='uint16') -> None:
        super().__init__(dtype_loading=dtype_loading)
        self.dtype_raw = dtype_loading
        self.dtype_recon = np.uint8

    #### "high-level" combined functions for testing and easy work flow (prob not applicable in GUI) ####   
    def reconstruct_buffer(self, buffer: np.ndarray, disp_coeffs: tuple=(0,0,0,0), wind_key: str='hann' ) -> np.ndarray : 
        """ performs reconstruction on entire passed-in OCT data buffer """
        pre_buffer = np.asarray( self.apply_pre_fft_functions(buffer, disp_coeffs, wind_key) )
        post_buffer = self.perform_fft(pre_buffer)
        return self.apply_post_fft_functions( post_buffer )
    
    def apply_pre_fft_functions(self, buffer: np.ndarray, coeffs: tuple, key: str) -> np.ndarray :
        """ method that applies all neccessary pre-FFT operations """
        data = self.substract_background(buffer)
        return self.apply_dispersion_correction(data, coeffs=coeffs, key=key)
        
    def apply_post_fft_functions(self, buffer: np.ndarray, samples_crop: int=0, is_scale_data_for_disp: bool=False) -> np.ndarray:
        """ method that applies all neccessary post-FFT operations """
        data = self.return_absolute( self.crop_fft_buffer(buffer) )
        data = self.crop_aScan_samples( data, samples_crop )
        if is_scale_data_for_disp :
            return self.return_scaled( data ) 
        return data
    
    def perform_fft(self, buffer: np.ndarray, l_pad=None) -> np.ndarray :
        """ apply fast fourier transform to the entire OCT data buffer """
        # TODO: check if it can be optimized, so that the FFT length of an A-scan is always powers of 2
        if l_pad is None :
            l_pad = buffer.shape[0]
        assert l_pad >= 0, "Padding values must be positve integer values"
        return np.asarray( np.fft.ifft( self.pad_buffer_along_axis(buffer, l_pad + buffer.shape[0]), axis=0 ), dtype=np.complex64 )
                      
    #### meta methods - methods adjust for dimensional mismatch of two arrays ####  
    def adjust_dim_for_processing(self, buffer: np.ndarray, vector: np.ndarray) -> np.ndarray :
        """ evaluate and prepare buffer and vector for numpy matrix-vector operations """
        if buffer.ndim == 1 :
            return np.asarray( buffer ), np.asarray( vector )     
        elif buffer.ndim == 2 :
            return np.asarray( buffer ), np.asarray( vector[:, np.newaxis] )
        elif buffer.ndim == 3 :
            return np.asarray( buffer ), np.asarray( vector[:, np.newaxis, np.newaxis] )
        else : 
            print("[DIMENSIONALITY WARNING:] returning empty array (dimensionality neither 1,2 or 3)")
            return []

    def calculate_nDim_independant_ascan_avg(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns averaged A-scan for i.e. background subtraction """
        return np.asarray( np.mean(buffer, axis=tuple(range(1, buffer.ndim)), dtype=self.dtype_raw) )
    
    def calculate_nDim_independant_ascan_median(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns median A-scan for i.e. background subtraction """
        return np.asarray( np.median(buffer, axis=tuple(range(1, buffer.ndim)), dtype=self.dtype_raw) )

    #### pre-FFT processing methods ####
    def substract_background(self, buffer: np.ndarray, background: np.ndarray=None) -> np.ndarray :
        """ Returns denoised OCT buffer (corresponding to sampling) """
        if background is None :  
                background = self.calculate_nDim_independant_ascan_avg( buffer )
        return np.asarray( np.subtract( *self.adjust_dim_for_processing(buffer, background), dtype=self.dtype_raw ) )
        
    def create_comp_disp_vec(self, a_len: int, coeffs: tuple, window: str='hann', sigma: int=None) -> np.ndarray :
        """ apply (windowed) disperison vector to the entire OCT data buffer """
        poly_disp = self.create_3rd_order_polynominal( a_len, coeffs )
        win = self.create_windowing_function( a_len, key=window, sigma=sigma )
        x = np.multiply( poly_disp, win )
        y = np.multiply( np.cos( poly_disp ), win )
        disp_vec = x + 1j * y
        return np.asarray( disp_vec, dtype=np.complex64 )
        
    def create_3rd_order_polynominal(self, a_len: int, coeffs: tuple) -> np.ndarray :
        """ creates real-valued polynominal to correct for dispersion mismatches """
        return np.asarray( np.polyval( coeffs, np.linspace(-0.5, 0.5, a_len) ) )
    
    def create_windowing_function(self, a_len: int, key='hann', sigma: int=None, is_show_info_prints: bool=False) -> np.ndarray :
        """ Creates a real-valued (float64) vector for i.e. spectrally shaping an A-scan """
        if sigma is None:
            sigma = a_len//10
        if key.lower() == 'hann' :
                return np.asarray( np.hanning(a_len) )
        elif key.lower() == 'hamm' :
            if is_show_info_prints :
                print("[INFO:] Using Hamming-Window - not Hanning-window")    
            return np.asarray( np.hamming(a_len) ) 
        elif key.lower() == 'kaiser' :
            if is_show_info_prints :
                print("[INFO:] Using Kaiser-Window - not Hanning-window")
            return np.asarray( np.kaiser(a_len, beta=sigma) )
        elif key.lower() == 'gauss' :
            if is_show_info_prints:
                print("[INFO:] Using Gaussian-Window - not Hanning-window")
            return np.asarray( signal.gaussian(a_len, sigma) )
        else : # TODO Check if this works well when it is called from i.e. the GUI 
                raise ValueError("You have passed an unrecognized key for the windowing-parameter")
                
    def apply_windowing(self, buffer: np.ndarray, key: str) -> np.ndarray :
        """ apply windowing function to the entire OCT data buffer """
        window = self.create_windowing_function(buffer.shape[0], key=key)
        return np.asarray( np.multiply( *self.adjust_dim_for_processing(buffer, window) ) )
    
    def apply_dispersion_correction(self, buffer: np.ndarray, coeffs: tuple, key: str) -> np.ndarray : 
        """ apply windowing function to the entire OCT data buffer """
        disp = self.create_comp_disp_vec( buffer.shape[0], coeffs=coeffs, window=key)
        return np.asarray( np.multiply( *self.adjust_dim_for_processing(buffer, disp) ), dtype=np.complex64 )
    
    #### FFT methods ####
    def pad_buffer_along_axis(self, buffer: np.ndarray, target_length: int, axis: int = 0) -> np.ndarray :
        """ pads zeros along a certain axis (default along A-scan axis) and returns padded array """
        pad_size = target_length - buffer.shape[axis]
        if pad_size <= 0:
            return buffer
        npad = [(0, 0)] * buffer.ndim
        npad[axis] = (pad_size, 0)
        return np.asarray( np.pad(buffer, pad_width=npad, mode='constant', constant_values=0) )
    
    def crop_fft_buffer(self, buffer: np.ndarray) -> np.ndarray :
        """ returns only first half of A-scan samples of complex buffer """
        return np.asarray( buffer[:buffer.shape[0]//2] )
    
    #### post-FFT methods ####
    def return_absolute(self, buffer: np.ndarray) -> np.ndarray :
        """ returns absoulte values of a complex OCT data buffer """
        abs_val_buffer = np.abs(buffer)
        return np.asarray( abs_val_buffer, dtype=np.uint16 )
    
    def return_scaled(self, buffer: np.ndarray, black_lvl: int=0, disp_scale: int=64) -> np.ndarray :
        """ returns scales version of OCT data buffer """
        buffer[buffer<=1] = 2
        return np.asarray( 255 * ( (20*np.log10(buffer) - black_lvl) / disp_scale), dtype=np.uint8 )
    
    def crop_aScan_samples(self, buffer: np.ndarray, samples_crop: int) -> np.ndarray :
        """ returns buffer which has the first n-th samples (samples_crop) removed ("remoce DC") """
        return np.asarray( buffer[samples_crop:], dtype=self.dtype_recon )
        
    #### Auxiliary functions ####
    # TODO: test the functions
    def apply_spectral_splitting(self, buffer: np.ndarray, split_factor: int) : # WORKS only buffers
        """ Reshapes B-Scan-like data buffer according to spectral splitting requirements """
        # TODO: rework for general use case, aka for OCT volume data not just B-scans/buffer
        return np.asarray( np.reshape( buffer, (buffer.shape[0] // split_factor, 
                                               split_factor * buffer.shape[1]) ) )

# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from recon_funcs...")
    REC = OctReconstructionManager()
    data = REC.load_oct_data()
    rec_d = REC.reconstruct_buffer(data)
    print(rec_d.shape)
    print(rec_d.dtype)
    plt.imshow(rec_d, cmap='gray', vmin=0, vmax=255)
    plt.show() 