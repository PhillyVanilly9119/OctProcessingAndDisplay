"""
@author:    philipp.matten@meduniwien.ac.at
            philipp.matten@gmx.de

                                        **** 
       Contains methods and functionality for general OCT data input/output (I/O)     
                                        ****
"""

import os 
import numpy as np
from tkinter.filedialog import Tk, askopenfilename 

### ABSTRACT METHODS ###
def preprocess_dimensionality(array, vector) :
        """
        Abstract method to evaluate and prepare (1-3)D / A-,B- or C-Scans 
        for being performing vector-matrix-operations
        """
        n_dims = np.size(np.shape(array))
        if n_dims == 1 :
                return np.asarray(array), np.asarray(vector)     
        elif n_dims == 2 :
                return np.asarray(array), np.asarray(vector[:, np.newaxis])
        elif n_dims == 3 :
                return np.asarray(array), np.asarray(vector[:, np.newaxis, np.newaxis])
        else : 
                raise ValueError("[DIMENSIONALITY ERROR] while preprocessing for numpy operation")
        
def average_nDim_independent(array) :
        if np.size(np.shape(array)) == 1 : 
                print("[CAUTION] paramater is returned as is (1D array)")
                return array
        elif np.size(np.shape(array)) == 2 :
                return np.average(array, axis=1)
        elif np.size(np.shape(array)) == 3 :
                return np.average(array, axis=(1,2))
        else : # TODO: check if necessary, since preprocessing should take care of that
                raise ValueError("[DIMENSION ERROR] of OCT array")

def tk_file_selection(text) :
        root = Tk()
        root.withdraw()
        path = askopenfilename(title=text)
        root.destroy()
        return path

def get_usr_selected_file() :
        """
        >>> Makro to load *.BIN-file selected by the user in the file explorer
        """
        file_path = tk_file_selection('Please select the OCT data file') 
        path = os.path.join(f"{file_path.split('/')[0]}\\", *file_path.split('/')[1:-1])
        folder = file_path.split('/')[-1]
        return path, folder

### LOADING AND STORING ###
def load_data_from_bin(glob_path, file, dims=None, dtype=np.uint16, is_dim_appendix=False, is_reshaping_array=False) :
        """
        >>> Loads a binary file containing the raw OCT data and returns it as properly reshaped np-array
        -> flag 'is_dim_appendix' can be set to automatically read out dimensions of scan from file name 
        """
        print("Loading raw data...") 
        print("[CAUTION] Asserting that raw data is *.BIN-file...") 
        oct_buffer = []
        file_path = os.path.join(glob_path, file)
        # try to load data
        if os.path.isfile(file_path) :
                try :
                        with open(file_path) as _ :     
                                oct_buffer  = np.fromfile(file_path, dtype=dtype)
                                assert oct_buffer, ValueError("Couldn't load data - received empty array!")         
                except : FileExistsError
        else:
                print("The selected file: \"{}\" does not exist or is not a file".format(file_path))    
        # flag to extract  dimensions from suffix** (i.e. '... X x Y x Z ... .bin')
        # ** file name like they're created when file was saved with <<save_data_to_bin()>>
        if is_dim_appendix :
                dims_string = file.split('_')[-1].split('.')[0].split('x')
                dimensions = []
                for dims in dims_string :
                        dimensions.append(int(dims))
                dims = tuple(dimensions)        
        else :
                dims = dims      
        # reshape and return buffer    
        oct_buffer = np.reshape(oct_buffer, (dims))      
        # Only works for B-Scans in this implementation -> TODO: Rethink more abstract way of doing this
        if is_reshaping_array :
                oct_buffer = np.transpose(np.reshape(oct_buffer, (dims[1], dims[0])))
        print(f"Done loading OCT data buffer! \nDimensions of loaded data file are {dims}")
        return np.asarray(oct_buffer, dtype=np.uint16)

def save_data_to_bin(data, path, file, dtype=np.uint16) :
        """
        >>> Creates appendix-string with data dimensions
        -> Saves *.bin-file containing the data in specified path as dtype
        NOTE that the default data type for raw oct data is uint16 -> change param if necessary
        """
        # make appendix
        shape = np.shape(data)
        appendix = ''
        for count, value in enumerate(shape) :
                if count == 0 :
                        appendix += f'_{value}'
                else :
                        appendix += f'x{value}'
        full_path = os.path.join(path, file + appendix + '.bin')
        assert not os.path.isfile(full_path), "[FILE ERROR] file already exists"
        with open(full_path, 'wb') as f :
                np.save(f, data.astype(dtype))
                print("Saved data successfully to {}", full_path)