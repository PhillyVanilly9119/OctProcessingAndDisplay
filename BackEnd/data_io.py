"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2021 Medical University of Vienna 
                                        ******
                                        
        >>> Contains methods and functionality for general OCT data input/output (I/O)     
                                        
"""

# global imports
import os
import cv2
import numpy as np

from tkinter.filedialog import Tk, askopenfilename 

# custom imports


class OctDataFileManager() :
    """
    >>> OCT-data I/O class for handling OCT data in binaries and images
    (so far, images have not been test and/or properly been implemented)
    """
    def __init__(self, dtype_loading='uint16') -> None:
        self.dtype_loading = dtype_loading
        self.is_user_selected_directory = False # label to see if directory was selected
                
    def _get_oct_meta_data(self) :
        """ makes user select file creates class variables of """   
        self.file_path_main = self._tk_file_selection()
        self.dir_main = self._get_main_dir()
        self.oct_dims, self.oct_ndims = self.get_oct_volume_dims(self.file_path_main)
        
    def _display_meta_data(self):
        self._get_oct_meta_data()
        print(f'OCT data (dimensions={self.oct_ndims}) shape = {self.oct_dims} ')
 
    def _get_main_dir(self) -> str :
        """ returns the directory in which the selected file self.file_path_main is located """ 
        return os.path.join( *(os.path.split(self.file_path_main)[:-1]) )
    
    def _tk_file_selection(self) -> str :
        """ returns full path of a file that the user selects via a GUI/prompt """
        self.is_user_selected_directory = True
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
        return dims, len(dims)
    
    def load_oct_data(self) :
        """ returns properly reshaped OCT data (cube) """
        self._get_oct_meta_data() # creates <self.file_path_main>, which is needed in < self.load_selected_bin_file()>
        return self.reshape_oct_volume( self.load_selected_bin_file() )
    
    def load_selected_bin_file(self) :
        """ loads and returns bin file that was selected when class instance was created """
        return self.load_bin_file( self.file_path_main )
    
    def reshape_oct_volume(self, buffer: np.array) -> np.array :
        """ Returns reshaped volume buffer/np-array acc. to self.dims-shape """
        return np.asarray( np.reshape(buffer, (self.oct_dims)) )
    
    def load_bin_file(self, path_file) -> np.array :
        """ loads and returns data in a numpy.array """
        assert os.path.isfile(path_file), "[CAUTION] path/string doesn't contain a valid file"
        return np.asarray(np.fromfile(path_file, dtype=self.dtype_loading))
    
    # TODO: test all methods from here on out
    def save_as_bin_file(self, buffer: np.array, pre_string: str, dtype_save=np.uint16) -> None :
        """ Saves selected volume in main directory with the established dimensions """
        # TODO: Rethink how to handle loading/saving dimensions tuples
        filename_saving = pre_string + self.create_vol_dims_suffix + '.bin'
        _path_saving = os.path.join(self.dir_main, filename_saving)
        print(f"Saving selected volume to file {filename_saving}... ")
        buffer.astype(dtype_save).tofile(_path_saving)
        print("[DONE] Saving selected volume!")
        
    def get_list_of_only_files(self) -> None :
        """ returns a list of all files in the self.main_dir """
        self.file_list_full = [f for f in os.listdir(self.dir_main) if os.path.isfile(os.path.join(self.dir_main, f))]
    
    def create_vol_dims_suffix(self) -> str :
        """ Creates a string containing the OCT data dimensions for saving """
        if len(self.oct_dims) == 3 :
            return f"{self.oct_dims[0]}x{self.oct_dims[1]}x{self.oct_dims[2]}"
        elif len(self.oct_dims) == 2 :
            return f"{self.dims[0]}x{self.oct_dims[1]}"
        elif len(self.dims) == 1 :
            return f"{self.oct_dims[0]}"
        else :
            ValueError("Dimensionality is not in range - please check <self.oct_dims>!")
    
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
                    
                    
# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from data_io...")
    IO = OctDataFileManager()
    IO._display_meta_data()    
