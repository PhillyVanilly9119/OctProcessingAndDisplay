"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality for OCT data reconstruction     
                                
"""

# global imports
import numpy as np
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import _calculate_shapes
from numpy.lib.type_check import imag
from scipy import signal
import matplotlib.pyplot as plt

# custom imports
import data_io as IO


class OctReconstructionManager(IO.OctDataFileManager) :
    def __init__(self, dtype_loading='<u2') -> None:
        super().__init__(dtype_loading=dtype_loading)
        self.dtype_raw = np.uint16
        self.dtype_recon = np.uint8
        
    ###########################################                     
    # ***** high-level processing methods *****
    ###########################################
    # ***** Pre-Processing *****  
    def perform_pre_fft_functions(self, 
                                  buffer: np.ndarray, 
                                  coeffs: tuple, 
                                  key: str, 
                                  is_sub_bg: bool=False) -> np.ndarray :
        """ method that applies pre-FFT operations, with an option for Background Subtraction of OCT raw buffer """
        if is_sub_bg :
            buffer = self.calculate_background_sub(buffer)
        return self.apply_dispersion_correction(buffer, coeffs=coeffs, key=key)
    
    # ***** Fast Fourier-Transform *****
    def perform_fft(self, 
                    buffer: np.ndarray, 
                    l_pad=None) -> np.ndarray :
        """ apply fast fourier transform to the entire OCT data buffer """
        # TODO: check if it can be optimized, so that the FFT length of an A-scan is always powers of 2
        if l_pad is None :
            l_pad = buffer.shape[0]
        assert l_pad >= 0, "Padding values must be positve integer values"
        return np.asarray( np.fft.fft( self.pad_buffer_along_axis(buffer, l_pad + buffer.shape[0]), axis=0 ), dtype=np.complex64 )
    
    # ***** Post-Processing *****
    def perform_post_fft_functions(self, 
                                   buffer: np.ndarray, 
                                   fac_scale: int, 
                                   black_lvl: int, 
                                   crop_lf_samples: int, 
                                   crop_hf_samples: int, 
                                   is_scale_data_for_disp: bool) -> np.ndarray:
        """ method that applies all neccessary post-FFT operations 
        >>> FFT has to be perfomed first (not iFFT(! due to values/dtype-conversions and log10) """
        data = self.return_absolute( self.crop_fft_buffer(buffer) ) # already cropped compl.-conj.
        data = self.perform_aScan_cropping( data, crop_lf_samples, crop_hf_samples )
        if is_scale_data_for_disp :
            return self.return_scaled( data, black_lvl=black_lvl, disp_scale=fac_scale ) 
        return data
   
    # ***** HIGH-LEVEL METHOD that performs entire OCT-RECONSTRUCTION *****
    def _run_reconstruction(self, 
                           buffer: np.ndarray, 
                           disp_coeffs: tuple, 
                           wind_key: str, 
                           samples_hf_crop: int=0, # gets set to max A-scan sampling in method
                           samples_dc_crop: int=0, 
                           scale_fac: int=65, 
                           blck_lvl: int=77,
                           is_bg_sub: bool=False,
                           show_scaled_data: bool=True) -> np.ndarray : 
        """ performs reconstruction on entire passed-in OCT data buffer 
        created as high level method call for easy accessability of OCT capabilities from GUI """
        pre_ = self.perform_pre_fft_functions( buffer, disp_coeffs, wind_key, is_bg_sub)
        post_ = self.perform_fft( pre_ )
        return self.perform_post_fft_functions( post_, scale_fac, blck_lvl,
                                               samples_dc_crop, samples_hf_crop, show_scaled_data )
    
    ##########################################
    # ***** low-level processing methods *****
    ##########################################
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
    
    # subtract noise floor from scan -> TODO: Review - produces negative values...
    def calculate_background_sub(self, buffer: np.ndarray, background: np.ndarray=None) -> np.ndarray :
        """ Returns denoised OCT buffer (corresponding to sampling) """
        if background is None :  
                background = self.calculate_nDim_independant_ascan_avg( buffer )
        return np.asarray( np.subtract( *self.adjust_dim_for_processing(buffer, background) ), dtype=self.dtype_raw )
    
    # handling dimensionality
    def calculate_nDim_independant_ascan_avg(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns averaged A-scan for i.e. background subtraction """
        return np.asarray( np.mean(buffer, axis=tuple(range(1, buffer.ndim))) )
    
    def calculate_nDim_independant_ascan_median(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns median A-scan for i.e. background subtraction """
        return np.asarray( np.median(buffer, axis=tuple(range(1, buffer.ndim)), dtype=self.dtype_raw) )
       
    def create_3rd_order_polynominal(self, a_len: int, coeffs: tuple) -> np.ndarray :
        """ creates real-valued polynominal to correct for dispersion mismatches """
        return np.asarray( np.polyval( coeffs, np.linspace(-0.5, 0.5, a_len) ) )
    
    # generate complex-valued dispersion vector (already windowed acc. to passed key-parameter)
    def create_comp_disp_vec(self, a_len: int, coeffs: tuple, key: str='hann', sigma: int=None) -> np.ndarray :
        """ apply (windowed) disperison vector to the entire OCT data buffer """
        poly_disp = self.create_3rd_order_polynominal( a_len, coeffs )
        window = self.create_windowing_function( a_len, key=key, sigma=sigma )
        x = np.multiply( poly_disp, window )
        y = np.multiply( np.cos( poly_disp ), window )
        return np.asarray( x + 1j * y, dtype=np.complex64 )
        
    # returns a windowing function to convolute raw OCT data with
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
        else :  
            raise ValueError("You have passed an unrecognized key for the windowing-parameter")
                
    def apply_windowing(self, buffer: np.ndarray, key: str) -> np.ndarray :
        """ apply windowing function to the entire OCT data buffer """
        window = self.create_windowing_function(buffer.shape[0], key=key)
        return np.asarray( np.multiply( *self.adjust_dim_for_processing(buffer, window) ) )
    
    def apply_dispersion_correction(self, buffer: np.ndarray, coeffs: tuple=(0,0,0,0), key: str='hann') -> np.ndarray : 
        """ apply windowing function to the entire OCT data buffer """
        disp = self.create_comp_disp_vec( buffer.shape[0], coeffs=coeffs )
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
        """ returns absoulte values of a complex OCT data buffer 
        !! CAUTION!! Since we use FFT and NOT iFFT (for log10 to work) return type is a float """
        return np.asarray( 20 * np.log10( np.abs(buffer) ), dtype=np.float )
    
    def return_scaled(self, buffer: np.ndarray, black_lvl: int=77, disp_scale: int=66) -> np.ndarray :
        """ returns scaled version of OCT data buffer """
        buffer = np.asarray( 255 * ( (buffer - black_lvl) / disp_scale ) )
        buffer[buffer < 0] = 0
        return np.asarray(buffer , dtype=self.dtype_recon )
    
    def perform_aScan_cropping(self, buffer: np.ndarray, lf_smpls_crop: int, hf_smpls_crop: int) -> np.ndarray :
        """ returns (reconstructed) buffer which has low- and high-frequency components/samples cropped """
        assert lf_smpls_crop < buffer.shape[0], "DC pixels to crop must be less than A-scan sampling length"
        assert hf_smpls_crop < buffer.shape[0], "High-Frequency pixels to crop must be less than A-scan sampling length"
        assert lf_smpls_crop + hf_smpls_crop < buffer.shape[0], "Amount of cropping pixels must be less than A-scan sampling length"
        return np.asarray( buffer[lf_smpls_crop:buffer.shape[0]-hf_smpls_crop] )
        
    #### Auxiliary functions ####
    def drop_every_nth_aScan(self, data: np.ndarray, n_drop: int) -> np.ndarray :
        """ reduces the A-scan sampling, via dropping out every n-th sample
        ATTENTION: method asserts that first dimension of array is A-scan-dimension
        NOTE: this happens at a loss of axial resolution in the x-space (reconstructed scan) """
        return np.asarray( data[::n_drop], dtype=data.dtype )
    
    # TODO: test the following functions
    def apply_spectral_splitting(self, buffer: np.ndarray, split_factor: int) : # WORKS only with B-scans / buffers
        """ Reshapes B-Scan-like data buffer according to spectral splitting requirements """
        # TODO: rework for general use case, aka for OCT volume data not just B-scans/buffer
        return np.asarray( np.reshape( buffer, (buffer.shape[0] // split_factor, 
                                               split_factor * buffer.shape[1]) ) )
        
    def calculate_enface_for_display(self, buffer: np.ndarray, map_key='max') -> np.ndarray:
        """ ... TBD """
        buffer = np.subtract( *self.adjust_dim_for_processing(buffer, np.mean(buffer, axis=(1,buffer.ndim-1))) )
        if map_key == 'max' :
            enface_map = np.amax(buffer, axis=(0))
        elif map_key == 'mean' :
            enface_map = np.mean(buffer, axis=(0))
        elif map_key == 'median' :
            enface_map = np.median(buffer, axis=(0))
        return np.asarray( enface_map, dtype=np.uint16 )


# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from < recon_funcs.py > ...")
    REC = OctReconstructionManager(dtype_loading='>u2')
    data = REC.load_oct_data()
    rec = REC.calculate_enface_for_display(data)
    # plt.imshow(rec)
    # plt.show()