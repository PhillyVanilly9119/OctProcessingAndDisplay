"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                        
        >>> Contains methods and functionality for general OCT data input/output (I/O)     
                                        
"""

# global imports
import os
import time
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from typing import List
from tkinter.filedialog import Tk, askopenfilename 

# custom imports


class OctDataFileManager() :
    """
    >>> Data managememt class for handling OCT-data I/O
    Constructor variables:
            ...
            ...
    """
    def __init__(self, is_user_file_selection: bool=False, file_path_main: str='', dtype=np.uint16) -> None:
        if is_user_file_selection :
                self.file_path_main = self.tk_file_selection()
        else :
                self.file_path_main = file_path_main                        
        self.dir_main = self.get_main_dir()
        self.dims = self.get_oct_volume_dims(self.file_path_main)
        self.dtype = dtype
    
    def get_main_dir(self) -> str :
        """ returns the directory in which the selected file self.file_path_main is located""" 
        return os.path.join( *(os.path.split(self.file_path_main)[:-1]) )
    
    def get_list_of_only_files(self) -> None :
        """ returns a list of all files in the self.main_dir """
        self.file_list_full = [f for f in os.listdir(self.dir_main) if os.path.isfile(os.path.join(self.dir_main, f))]
    
    def tk_file_selection(self) -> str:
        """ returns full path of a file that the uder selects via a GUI/prompt """
        root = Tk()
        root.withdraw()
        path = askopenfilename(title='Please select a file')
        root.destroy()
        return path
    
    def get_oct_volume_dims(self, file_path: str) -> tuple :
        """ reads out and returns the dimensions of an OCT volume from the bin-files' name """
        file_name = os.path.split(file_path)[-1]
        dims_list = [s for s in file_name.split('_') if s.find('x') != -1]
        dims_block = ''.join(dims_list)
        dims = tuple(int(i) for i in dims_block.split('x'))
        return dims
    
    def load_bin_file(self, path_file) -> np.array :
        """ loads and returns data in a numpy.array """
        assert os.path.isfile(path_file), "[CAUTION] path/string doesn't contain a valid file"
        return np.asarray(np.fromfile(path_file, dtype=self.dtype))
    
    def save_as_bin_file(self, buffer: np.array, pre_string: str, dtype_save=np.uint16) -> None :
        """ Saves selected volume in main directory with the established dimensions """
        # TODO: Rethink how to handle loading/saving dimensions tuples
        filename_saving = pre_string + f'_{self.dims[0]}x{self.dims[1]}x{self.dims[2]}.bin'
        _path_saving = os.path.join(self.dir_main, filename_saving)
        print(f"Saving selected volume to file {filename_saving}... ")
        buffer.astype(dtype_save).tofile(_path_saving)
        print("[DONE]Saving selected volume!")
    
    def load_image_file(self, file_path, dtype_loading=np.uint8) -> np.array :
        if os.path.isfile(file_path) :  
            img = cv2.imread(file_path)
        if img :
            return np.asarray(img[:,:,0], dtype=dtype_loading) 
    
    def load_all_imgs_in_dir(self, img_list, dtype_loading=np.uint8) -> np.array :
        img_buffer = []
        for img in img_list :
            if os.path.isfile(img) :
                c_img = cv.imread(img)
                if c_img.ndim == 3 : # assuming RGB-img
                    img_buffer.append(c_img[:,:,0])
                else : # assuming grey-scale img 
                    img_buffer.append(c_img)
        return np.asarray(img_buffer, dtype=dtype_loading)
    
    def reshape_oct_volume(self, buffer: np.array) -> np.array :
        """ Returns reshaped volume buffer/np-array acc. to self.dims-shape """
        return np.asarray( np.reshape(buffer, (self.dims), dtype=self.dtype) )
    
    def preprocess_dimensionality(self, buffer, vector) -> np.array :
        """ evaluate and prepare buffer and vector for numpy matrix-vektor operations """
        if buffer.ndim == 1 :
            return np.asarray(buffer), np.asarray(vector)     
        elif buffer.ndim == 2 :
            return np.asarray(buffer), np.asarray(vector[:, np.newaxis])
        elif buffer.ndim == 3 :
            return np.asarray(buffer), np.asarray(vector[:, np.newaxis, np.newaxis])
        else : 
            raise ValueError("[DIMENSIONALITY ERROR] while preprocessing for numpy operation")
            return []

    def average_nDim_independent(self, buffer) -> np.array :
        """ """
        if buffer.ndim == 1 : 
            print("[CAUTION] paramater is returned as is (1D array)")
            return array
        elif buffer.ndim == 2 :
            return np.average(array, axis=1)
        elif buffer.ndim == 3 :
            return np.average(array, axis=(1,2))
        else : # TODO: check if necessary, since preprocessing should take care of that
            raise ValueError("[DIMENSION ERROR] of OCT array")
                    
                    
if __name__ == '__main__' :
        MAN = OctDataFileManager(is_user_file_selection=True, 
                                 file_path_main = r"D:\PhilippDataAndFiles\4D-OCT\Data\reconstructed_1536x640x645_vol.bin")
        
