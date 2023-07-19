"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality for OCT data reconstruction     
                                
"""

# global imports
import os
import sys
import numpy as np
from tqdm import tqdm
from scipy import signal
import matplotlib.pyplot as plt

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))
from configdatamanager import ConfigDataManager

import octdatafilemanager as IO

class OctReconstructionManager(IO.OctDataFileManager) :
    def __init__(self, dtype_loading='<u2') -> None:
        super().__init__(dtype_loading=dtype_loading)
        self.dtype_raw = np.uint16
        self.dtype_recon = np.uint8
        
    ###########################################                     
    # ***** high-level processing methods *****
    ###########################################
    # ***** Pre-Processing *****  
    def perform_pre_fft_functions(self, buffer: np.ndarray, coeffs: tuple, key: str, is_sub_bg: bool=False) -> np.ndarray :
        """applies pre-FFT operations, with an option for Background Subtraction of OCT raw buffer
        Args:
            buffer (np.ndarray): OCT buffer (A-, B-, or C-scan)
            coeffs (tuple): dispersion correction polynominla coefficients
            key (str): windowing key to shape OCt envelope
            is_sub_bg (bool, optional): Flag enable backgorund subtraction. Defaults to False.
        Returns:
            np.ndarray: 0-padded complex pre-shaped OCT data, ready for the Fourier Transform
        """
        if is_sub_bg :
            buffer = self.calculate_background_sub(buffer)
        return self.apply_dispersion_correction(buffer, coeffs=coeffs, key=key)
    
    # ***** Fast Fourier-Transform *****
    def perform_fft(self, buffer: np.ndarray, l_pad: int=None) -> np.ndarray :
        """apply fast fourier transform to the entire OCT data buffer
        Args:
            buffer (np.ndarray): OCT data, ready to be Fourier Transfpormed 
            l_pad (int): number of zeros to be added along A-scan. Defaults to None.

        Returns:
            np.ndarray: _description_
        """
        # TODO: check if it can be optimized, so that the FFT length of an A-scan is always powers of 2
        if l_pad == 0 :
            l_pad = buffer.shape[0]
        elif l_pad == 1:
            l_pad = OctReconstructionManager.diff_to_next_power_of_2(buffer.shape[0])
        assert l_pad >= 0, "Padding values must be positve integer values"
        return np.asarray( np.fft.fft( self.pad_buffer_along_axis(buffer, l_pad + buffer.shape[0]), axis=0 ), dtype=np.complex64 )
    
    # ***** Post-Processing ***** ---------------------------------------------
    def perform_post_fft_functions(self, buffer: np.ndarray, fac_scale: int, black_lvl: int, 
                                   crop_lf_samples: int, crop_hf_samples: int, is_scale_data_for_disp: bool) -> np.ndarray:
        """applies all neccessary post-FFT operations 
        >>> FFT has to be perfomed first (not iFFT(! due to values/dtype-conversions and log10)
        Args:
            buffer (np.ndarray): OCT data 
            fac_scale (int): scaling factor to scale in uint8 value-space
            black_lvl (int): constant to be substrated from signal
            crop_lf_samples (int): DC samples to be cropped out of the signal
            crop_hf_samples (int): high frequency samples to be cropped out of the signal
            is_scale_data_for_disp (bool): flag to deterine wether of not the data should be scaled to uint8 value space
        Returns:
            np.ndarray: final reconstructed OCT signal
        """
        data = self.return_abs_val_in_log_scale( self.crop_fft_buffer(buffer) ) # already cropped compl.-conj.
        data = self.perform_aScan_cropping( data, crop_lf_samples, crop_hf_samples )
        if is_scale_data_for_disp :
            return self.return_scaled( data, black_lvl=black_lvl, disp_scale=fac_scale ) 
        return data
   
    # ***** HIGH-LEVEL METHODs that performs entire OCT-RECONSTRUCTION *****
    #-----------------------------------------------------------------
    def _run_reconstruction(self, buffer: np.ndarray, disp_coeffs: tuple, wind_key: str, samples_hf_crop: int=0, samples_dc_crop: int=0, 
                           scale_fac: int=65, blck_lvl: int=77, is_bg_sub: bool=False, show_scaled_data: bool=True) -> np.ndarray : 
        """performs reconstruction on entire passed-in OCT data buffer 
        created as high level method call for easy accessability of OCT capabilities from GUI
        Args:
            buffer (np.ndarray): raw OCT data
            disp_coeffs (tuple): coefficients of polynominal for dispersion correction 
            wind_key (str): key for windowing function for spectral shaping
            samples_hf_crop (int, optional): HF smaspels to be cropped. Defaults to 0.
            samples_dc_crop (int, optional): DC samples to be cropped. Defaults to 0.
            scale_fac (int, optional): scale factore for display in log10 - uint8 value range. Defaults to 65.
            blck_lvl (int, optional): constant to be subtracted from recon signal. Defaults to 77.
            is_bg_sub (bool, optional): flag to enable background subtraction. Defaults to False.
            show_scaled_data (bool, optional): flag to enable scaling of data to 8 Bit uint8 display range. Defaults to True.
        Returns:
            np.ndarray: reconstructed OCT data
        """
        pre_ = self.perform_pre_fft_functions( buffer, disp_coeffs, wind_key, is_bg_sub)
        post_ = self.perform_fft( pre_ )
        return self.perform_post_fft_functions( post_, scale_fac, blck_lvl,
                                               samples_dc_crop, samples_hf_crop, show_scaled_data )

    # -----------------------------------------------------------------------------------------------------
    def _run_reconstruction_from_json(self, buffer: np.ndarray, json_config_file_path: str) -> np.ndarray : 
        """same functionality as _run_reconstruction(), 
        only that the reconstruction-parameters are parsed from JSON-congig-file
        Args:
            buffer (np.ndarray): raw OCT data
            json_config_file_path (str): path to the JSON-file containing the reconstruction params
        Returns:
            np.ndarray: reconstructed OCT data
        """
        JSON = ConfigDataManager(filename=json_config_file_path).load_json_file()
        pre_ = self.perform_pre_fft_functions( buffer=buffer, 
                                               coeffs=JSON['dispersion_coefficients'], 
                                               key=JSON['windowing_key'], 
                                               is_sub_bg=JSON['is_substract_background'])
        post_ = self.perform_fft( pre_, l_pad=JSON["zeros_to_pad"] )
        return self.perform_post_fft_functions( buffer=post_, 
                                                fac_scale=JSON['disp_scale_factor'], 
                                                black_lvl=JSON['black_lvl_for_dis'], 
                                                crop_lf_samples=JSON['dc_crop_samples'], 
                                                crop_hf_samples=JSON['hf_crop_samples'], 
                                                is_scale_data_for_disp=JSON['is_scale_data_for_display'] )
        
    # -----------------------------------------------------------------------------------------------------
    # TODO: check if this is necessary 
    def _run_reconstruction_no_log_scale_from_json(self, buffer: np.ndarray, json_config_file_path: str) -> np.ndarray :
        """same functionality as _run_reconstruction(), only that no steps after cropping abs of FFTed signal -> no log10 scaling
        only that the reconstruction-parameters are parsed from JSON-congig-file 
        AArgs:
            buffer (np.ndarray): raw OCT data
            json_config_file_path (str): path to the JSON-file containing the reconstruction params
        Returns:
            np.ndarray: reconstructed (non log10_scaled) OCT data
        """
        JSON = ConfigDataManager(filename=json_config_file_path).load_json_file()
        pre_ = self.perform_pre_fft_functions(buffer=buffer, 
                                              coeffs=JSON['dispersion_coefficients'], 
                                              key=JSON['windowing_key'], 
                                              is_sub_bg=JSON['is_substract_background'])
        post_ = self.perform_fft( pre_ )
        post_ = self.return_abs_val_in_log_scale( post_ ) # already cropped compl.-conj.
        return self.perform_aScan_cropping( post_, lf_smpls_crop=JSON['dc_crop_samples'], hf_smpls_crop=JSON['hf_crop_samples'] )

    ##########################################
    # ***** low-level processing methods *****
    ##########################################-------------------------------------------------------------
    # Static methods mark the ones that do not depend on class or instace variabels and are more "abstract"
    @staticmethod
    def diff_to_next_power_of_2(n: int) -> int:
        j = 0
        while 2**j <= n:
            j += 1
        return 2**j - n
    @staticmethod
    def create_3rd_order_polynominal(a_len: int, coeffs: tuple) -> np.ndarray :
        """creates real-valued polynominal to correct for dispersion mismatches
        Args:
            a_len (int): lenght of expected A-scan
            coeffs (tuple): coefficients of 3rd order polynominal
        Returns:
            np.ndarray: polyninominal evlaluated on origin-symmetric linspace of length of A-scan
        """
        return np.asarray( np.polyval( coeffs, np.linspace(-0.5, 0.5, a_len) ) )
    
    @staticmethod
    def create_windowing_function(a_len: int, key='hann', sigma: int=None, is_show_info_prints: bool=False) -> np.ndarray :
        """creates a real-valued vector for i.e. spectrally shaping an A-scan
        Args:
            a_len (int): length of expected A-scan
            key (str, optional): key to indicate the selected windowing function. Defaults to 'hann'.
            sigma (int, optional): sigma-param for Gaussian windowing function. Defaults to None.
            is_show_info_prints (bool, optional): flag for debugging. Defaults to False.
        Raises:
            ValueError: if key for requested windowing function is not implemented (yet)
        Returns:
            np.ndarray: returns windowing function of the same length as the raw A-scan
        """
        if is_show_info_prints:
            print(f"[INFO:] Using {key.upper}-Window...")
        if sigma is None:
            sigma = a_len//10
        if key.lower() == 'hann' :
            return np.asarray( np.hanning(a_len), dtype=np.float32 )
        elif key.lower() == 'hamm' :
            return np.asarray( np.hamming(a_len), dtype=np.float32 ) 
        elif key.lower() == 'kaiser' :
            return np.asarray( np.kaiser(a_len, beta=sigma), dtype=np.float32 )
        elif key.lower() == 'gauss' :
            return np.asarray( signal.gaussian(a_len, sigma), dtype=np.float32 )
        else :  
            raise ValueError("You have passed an unrecognized key for the windowing-parameter")
    
    @staticmethod
    def create_comp_disp_vec(a_len: int, coeffs: tuple, key: str='hann', sigma: int=None) -> np.ndarray :
        """generate complex-valued dispersion vector (already windowed acc. to passed key-parameter)
        Args:
            a_len (int): length of expected A-scan
            coeffs (tuple): coefficients of 3rd order polynominal
            key (str, optional): indicating the kind of window with which the vector gets convoluted. Defaults to 'hann'.
            sigma (int, optional): sigma-value, if Gaussian-window is chosen. Defaults to None.
        Returns:
            np.ndarray: returns complex-valued windowing function to shape spectra interference signal (raw A-scan)
        """
        poly_disp = OctReconstructionManager.create_3rd_order_polynominal( a_len, coeffs )
        window = OctReconstructionManager.create_windowing_function( a_len, key=key, sigma=sigma )
        x = np.multiply( poly_disp, window )
        y = np.multiply( np.cos( poly_disp ), window )
        return np.asarray( x + 1j * y, dtype=np.complex64 )
        
    # handling dimensionality
    def adjust_dim_for_processing(self, buffer: np.ndarray, vector: np.ndarray) -> np.ndarray :
        """ evaluate and prepare buffer and vector for numpy matrix-vector operations """
        if buffer.ndim == 1 :
            return np.asarray( buffer ), np.asarray( vector )     
        elif buffer.ndim == 2 :
            return np.asarray( buffer ), np.asarray( vector[:, np.newaxis] )
        elif buffer.ndim == 3 :
            return np.asarray( buffer ), np.asarray( vector[:, np.newaxis, np.newaxis] )
        else : 
            print("[DIMENSIONALITY WARNING:] returning empty array (dimensionality neither 1,2 nor 3)")
            return []
    
    # subtract noise floor from scan -> TODO: Review - produces negative values...
    def calculate_background_sub(self, buffer: np.ndarray, background: np.ndarray=None) -> np.ndarray :
        """ returns denoised OCT buffer (corresponding to sampling) """
        if background is None :  
                background = self.calculate_nDim_independant_ascan_avg( buffer )
        return np.asarray( np.subtract( *self.adjust_dim_for_processing(np.asarray(buffer, dtype=np.float32),
                                                                        np.asarray(background, dtype=np.float32)) 
                                       ), dtype=np.float32 )
    
    def calculate_nDim_independant_ascan_avg(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns averaged A-scan for i.e. background subtraction """
        return np.asarray( np.mean(buffer, axis=tuple(range(1, buffer.ndim))) )
    
    def calculate_nDim_independant_ascan_median(self, buffer: np.ndarray) -> np.ndarray :
        """ calculates and returns median A-scan for i.e. background subtraction """
        return np.asarray( np.median(buffer, axis=tuple(range(1, buffer.ndim)), dtype=self.dtype_raw) )
       
                
    def apply_windowing(self, buffer: np.ndarray, key: str) -> np.ndarray :
        """ apply windowing function to the entire OCT data buffer """
        window = self.create_windowing_function(buffer.shape[0], key=key)
        return np.asarray( np.multiply( *self.adjust_dim_for_processing(buffer, window), dtype=np.float32 ) )
    
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
    def return_abs_val_in_log_scale(self, buffer: np.ndarray) -> np.ndarray :
        """ returns absoulte values of a complex OCT data buffer 
        !! CAUTION!! Since we use FFT and NOT iFFT (for log10 to work) return type is a float """
        return np.asarray( 20 * np.log10( np.abs(buffer) ), dtype=np.float64 )
    
    def return_abs_val(self, buffer: np.ndarray) -> np.ndarray :
        """ post-FFT function: returns absoulte values of a complex OCT data buffer """
        return np.asarray( np.abs(buffer ), dtype=np.float )
    
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


    def process_large_volumes(self, raw_dims: tuple, json_file_name: str,  full_file_path_raw: str, 
                              bScan_start_idx: int=0, full_file_path_recon: str=None, is_save_volume_2disk: bool=False) -> np.ndarray:
        """Asserting an OCT C-Scan saved as one big-ass *.BIN-file, 
        this function reconstructs the entire volume, buffer by buffer along the c-axis

        Args:
            raw_dims (np.ndarray): expexcted dimensions from OCt data in raw file 
            json_file_name (str): json-file with all params for reconstruction
            full_file_path_raw (str): path to raw-/*.BIN-file
            bScan_start_idx (int, optional): start index (in case the volume is shifted). Defaults to 0.
            full_file_path_recon (str, optional): path to where the should be saved 
            - if safe flag is True -> appends '_recon' to file name and saves it as this. Defaults to None.
            is_save_vol_2disk (bool, optional): flag to chose wether or not volume should be saved to disk. Defaults to False.

        Returns:
            np.ndarray: reconstructed OCT-volume
        """
        # Pre-allocations and sanity checks for function params
        assert len(raw_dims) == 3, "Expecting a large (3D) volume when invoking this function"
        JSON = ConfigDataManager(filename=json_file_name).load_json_file()
        aLen_raw, bLen, cLen = raw_dims
        if JSON["zeros_to_pad"] == 0 :
            aLen_rec = aLen_raw - JSON["dc_crop_samples"] - JSON["hf_crop_samples"]
        elif JSON["zeros_to_pad"] == 1 :
            aLen_rec = (aLen_raw + OctReconstructionManager.diff_to_next_power_of_2(aLen_raw))//2 - JSON["dc_crop_samples"] - JSON["hf_crop_samples"]
        else :
            raise ValueError("unrecognized vlaue for zeros_to_pad - so far only 0 and 1 are implemted") #TODO: add arbitrary num of 0 
        raw_full_file_size_bytes = os.path.getsize(full_file_path_raw)
        raw_bScan_file_size = aLen_raw * bLen
        assert raw_full_file_size_bytes % (raw_bScan_file_size * 2 * cLen) == 0, f"Dims ({aLen_raw}, {bLen}, {cLen}): Either the dimensions or the data type are mismatched"
        if full_file_path_recon is None:
            full_file_path_recon = full_file_path_raw.split('.bin')[0] + '_recon.bin'
        out_vol = np.zeros((aLen_rec, bLen, cLen))
        # loop though volume and reconstruct (optional: and safe) BUFFER-WISE
        for c in tqdm(range(cLen)):
            with open(full_file_path_raw, 'rb') as f_raw:
                offset = ((c + bScan_start_idx) % cLen) * raw_bScan_file_size * np.dtype(self.dtype_loading).itemsize # offset in bytes
                raw_buffer = np.fromfile(f_raw, dtype=self.dtype_raw, count=raw_bScan_file_size, offset=offset) # load buffer
                raw_buffer = np.reshape(raw_buffer, (bLen, aLen_raw)) # reshape to size A * B
                raw_buffer = raw_buffer.swapaxes(0,1) # swap axis (A is 0th axis, by convention)
                recon_buffer = self._run_reconstruction_from_json(buffer=raw_buffer,
                                                                  json_config_file_path=json_file_name) # reconstruct
                if is_save_volume_2disk: # save-/append reconstructed buffer, if flag is True
                    with open(full_file_path_recon, 'a+b') as f: # Save to file in binary append mode
                        recon_buffer.astype(self.dtype_recon).tofile(f)
                out_vol[:, :, c] = recon_buffer # write current buffer in out volume buffer 
        return np.asarray(out_vol, dtype=self.dtype_recon)
    

# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from < octreconstructionmanager.py > ...")

    # path = r"/home/zeiss/Data_Tachyoptes/rasterVol04_13312x512x512.bin"
    # recon = OctReconstructionManager().process_large_volumes((13312,512,512), 'DefaultReconParams', path, is_save_volume_2disk=True)
    
    # plt.imshow(np.mean(recon, axis=0), cmap='gray')
    # plt.show()
