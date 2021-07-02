"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                        
        >>> Contains methods and functionality for general OCT data input/output (I/O)     
                                        
"""

# global imports
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from typing import List
from tkinter.filedialog import Tk, askopenfilename 

# custom imports


class OctDataFileManager() :
    """
    >>> Data managememt class for handling OCT-data I/O
    Constructor variables:
        > is_user_file_selection = flag to decide 
        > file_path_main = path to the (*.BIN)-file containing the OCT data
        > dtype = Data type of the expeted data - usually uint16 (OCT raw data) 
    """
    def __init__(self, is_user_file_selection: bool=False, file_path_main: str='', dtype='uint8') -> None:
        self.dtype = dtype
        if is_user_file_selection :
                self.file_path_main = self.tk_file_selection()
        else :
                self.file_path_main = file_path_main
        # get the path to the main dir in which the file is located 
        self.dir_main = self.get_main_dir()
        # get OCT volume dimensions from the file name
        self.dims = self.get_oct_volume_dims(self.file_path_main)
 
    # CONSTR: Gets called by contructor to create class variable with the main-dir
    def get_main_dir(self) -> str :
        """ returns the directory in which the selected file self.file_path_main is located """ 
        return os.path.join( *(os.path.split(self.file_path_main)[:-1]) )
    
    # CONSTR: Gets called by contructor to make user select a file containing OCT-data 
    def tk_file_selection(self) -> str :
        """ returns full path of a file that the user selects via a GUI/prompt """
        root = Tk()
        root.withdraw()
        path = askopenfilename(title='Please select a file')
        root.destroy()
        return path
    
    # CONSTR: Gets called by constructor to read-out OCT volume dimensions from *.BIN file name
    def get_oct_volume_dims(self, file_path: str) -> tuple :
        """ reads out and returns the dimensions of an OCT volume from the bin-files' name """
        file_name = os.path.split(file_path)[-1]
        dims_list = [s for s in file_name.split('_') if s.find('x') != -1]
        dims_block = ''.join(dims_list)
        dims = tuple(int(i) for i in dims_block.split('x'))
        return dims
    
    # A MAIN CLASS METHOD 
    def return_oct_cube(self) :
        """ returns properly reshaped OCT data (cube) """
        return self.reshape_oct_volume( self.load_selected_bin_file() )
    
    def load_selected_bin_file(self) :
        """ loads and returns bin file that was selected when class instance was created """
        return self.load_bin_file( self.file_path_main )
    
    def reshape_oct_volume(self, buffer: np.array) -> np.array :
        """ Returns reshaped volume buffer/np-array acc. to self.dims-shape """
        return np.asarray( np.reshape(buffer, (self.dims)) )
    
    def load_bin_file(self, path_file) -> np.array :
        """ loads and returns data in a numpy.array """
        assert os.path.isfile(path_file), "[CAUTION] path/string doesn't contain a valid file"
        return np.asarray(np.fromfile(path_file, dtype=self.dtype))
    
    # TODO: test all methods from here on out
    def save_as_bin_file(self, buffer: np.array, pre_string: str, dtype_save=np.uint16) -> None :
        """ Saves selected volume in main directory with the established dimensions """
        # TODO: Rethink how to handle loading/saving dimensions tuples
        filename_saving = pre_string + f'_{self.dims[0]}x{self.dims[1]}x{self.dims[2]}.bin'
        _path_saving = os.path.join(self.dir_main, filename_saving)
        print(f"Saving selected volume to file {filename_saving}... ")
        buffer.astype(dtype_save).tofile(_path_saving)
        print("[DONE] Saving selected volume!")
        
    def get_list_of_only_files(self) -> None :
        """ returns a list of all files in the self.main_dir """
        self.file_list_full = [f for f in os.listdir(self.dir_main) if os.path.isfile(os.path.join(self.dir_main, f))]
    
    def create_vol_dims_suffix(self) -> str :
        """ Creates a string containing the OCT data dimensions for saving """
        if len(self.dims) == 3 :
            return f"{self.dims[0]}x{self.dims[1]}x{self.dims[2]}"
        elif len(self.dims) == 2 :
            return f"{self.dims[0]}x{self.dims[1]}"
        elif len(self.dims) == 1 :
            return f"{self.dims[0]}"
        else :
            ValueError("Dimensionality is not in range - please check <self.dims>!")
    
    def load_image_file(self, file_path, dtype_loading=np.uint8) -> np.array :
        """ Check if it works... """
        assert os.path.isfile(file_path)  
        img = cv2.imread(file_path)
        if np.asarray(img).shape[-1] > 1 :
            return np.asarray(img[:,:,0], dtype=dtype_loading) 
        else :
            return np.asarray(img, dtype=dtype_loading)
        
    def load_all_imgs_in_dir(self, img_list, dtype_loading=np.uint8) -> np.array :
        img_buffer = []
        for img in img_list :
            if os.path.isfile(img) :
                c_img = cv2.imread(img)
                if c_img.ndim == 3 : # assuming RGB-img
                    img_buffer.append(c_img[:,:,0])
                else : # assuming grey-scale img 
                    img_buffer.append(c_img)
        return np.asarray(img_buffer, dtype=dtype_loading) 
                    
                    
if __name__ == '__main__' :
        MAN = OctDataFileManager(is_user_file_selection=False, 
                                 file_path_main = r"E:\WetLabsAndreas11062021\HDF5_ContinuousVolumeExport_decoded\20210611_133155_cubes\20210611_133155_949x583x583_0.bin")
        data = MAN.return_oct_cube()
        print(data.shape)
        print(data.ndim)
        print(data.dtype)
        print("Success!")
        plt.imshow(data[:,:,300])
        plt.show()
        
