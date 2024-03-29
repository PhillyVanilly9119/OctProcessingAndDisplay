"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2021 Medical University of Vienna 
                                        ******
                                        
        >>> Contains methods and functionality for general OCT data input/output (I/O)     
                                        
"""

# global imports
import os
import re
import cv2
import numpy as np

from tkinter.filedialog import Tk, askopenfilename, askdirectory

from numpy.core.fromnumeric import reshape 

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
    
    def _tk_folder_selection(self) -> str:
        """ returns path to main folder of what the user selects via a GUI/prompt """
        root = Tk()
        root.withdraw()
        path = askdirectory(title='Please select a folder')
        root.destroy()
        return path
    
    def get_oct_volume_dims(self, file_path: str) -> tuple :
        """ reads out and returns the dimensions of an OCT volume from the bin-files' name 
        the dimensions block has to be of form '..._{aLen}x{bLen}x({cLen})...' """
        file_name = os.path.split(file_path)[-1] # get filename only
        dims_list = [s for s in file_name.split('_') if s.find('x') != -1]
        dims_block = ''.join(dims_list)
        dims_block = dims_block.split('x')
        numbers = re.compile(r'\d+(?:\.\d+)?')
        dims = []
        for dim in dims_block: # rewrite list comprehensions
            dims.append(numbers.findall(dim))
        dims = [item for sublist in dims for item in sublist]
        dims = tuple(int(i) for i in dims)
        return dims, len(dims)
    
    def load_oct_data(self, dtype=np.uint16) -> np.ndarray :
        """ returns properly reshaped OCT data (cube) """
        self._get_oct_meta_data() # creates <self.file_path_main>, which is needed in < self.load_selected_bin_file() >
        return np.asarray( self._reshape_oct_volume(self.load_selected_bin_file()), dtype=dtype )
            
    def load_selected_bin_file(self) :
        """ loads and returns bin file that was selected when class instance was created 
        NOTE: always loads data as uint"""
        return self.load_bin_file( self.file_path_main )
    
    def _reshape_oct_volume(self, buffer: np.array) -> np.array :
        """ Returns reshaped volume buffer/np-array acc. to self.dims-shape """
        if len(self.oct_dims) == 1 :
            dims = self.oct_dims
        elif len(self.oct_dims) == 2 :
            dims = (self.oct_dims[1], self.oct_dims[0])
        elif len(self.oct_dims) == 3 :
            dims = (self.oct_dims[2], self.oct_dims[1], self.oct_dims[0])
        return np.asarray( np.swapaxes(np.reshape(buffer, dims), 0, -1) )
    
    def load_bin_file(self, path_file) -> np.array :
        """ loads and returns data in a numpy.array """
        # # debug
        # print(f"Loading data as type: {self.dtype_loading}")
        assert os.path.isfile(path_file), "[CAUTION] path/string doesn't contain a valid file"
        return np.asarray(np.fromfile(path_file, dtype=self.dtype_loading))
    
    # TODO: test all methods from here on out
    def save_as_bin_file(self, buffer: np.array, pre_string: str, dtype_save=np.uint16) -> None :
        """ Saves selected volume in main directory with the established dimensions """
        # TODO: Rethink how to handle loading/saving dimensions tuples!!!
        vol_dims = self.create_vol_dims_suffix
        print(vol_dims)
        filename_saving = pre_string + f'_{self.oct_dims[0]}x{self.oct_dims[1]}_' + '.bin'
        _path_saving = os.path.join(self.dir_main, filename_saving)
        print(f"Saving selected volume to file {filename_saving}... ")
        buffer.astype(dtype_save).tofile(_path_saving)
        print("[DONE] Saving selected volume!")
    
    def create_vol_dims_suffix(self) -> str :
        """ Creates a string containing the OCT data dimensions for saving """
        if len(self.oct_dims) == 3 :
            str_dims = f"_{self.oct_dims[0]}x{self.oct_dims[1]}x{self.oct_dims[2]}_"
        elif len(self.oct_dims) == 2 :
            str_dims =  f"_{self.dims[0]}x{self.oct_dims[1]}_"
        elif len(self.dims) == 1 :
            str_dims = f"_{self.oct_dims[0]}_"
        else :
            ValueError("Dimensionality is not in range - please check <self.oct_dims>!")
        return str(str_dims)
    
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
                    
    
#---------------------------------------------------------
### General static methods related to volume reshaping ###
#---------------------------------------------------------
def __return_volume_dims_string(t: tuple) -> str:
    if not isinstance(t, tuple):
        raise ValueError("Input must be a tuple.")
    filename_unfiltered = "x".join(str(elem) for elem in t)
    return "_" + filename_unfiltered + "_"
              
# not tested
def reshape_oct_volume(buffer: np.array, dims: tuple) -> np.array :
    """ Returns reshaped volume buffer/np-array acc. to self.dims-shape """
    if len(dims) == 1 :
        dims = dims[0]
    elif len(dims) == 2 :
        dims = (dims[1], dims[0])
    elif len(dims) == 3 :
        dims = (dims[2], dims[1], dims[0])
    return np.asarray( np.swapaxes(np.reshape(buffer, dims), 0, -1) )
   
                    

if __name__ == '__main__' :
    print("[INFO:] Running from < data_io.py > ...")
    # IO = OctDataFileManager()  
