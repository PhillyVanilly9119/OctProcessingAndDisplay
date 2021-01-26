"""
@author:    philipp.matten@meduniwien.ac.at
            philipp.matten@gmx.de

                                        **** 
       Contains methods and functionality for general OCT data input/output (I/O)     
                                        ****
"""

# proprietary imports
import os 
import time
import numpy as np
from tkinter.filedialog import Tk, askopenfilename 

# costom imports


###############################
###     ABSTRACT METHODS    ###
###############################
def tk_file_selection(text) :
        root = Tk()
        root.withdraw()
        path = askopenfilename(title=text)
        root.destroy()
        return path

###########################
###     DATA I/O        ###
###########################
def load_data_from_bin_file(path, dtype=np.uint16, dims=None, is_select_path_manually=False, is_dims_in_file_name=True, is_reshaping_array=True) :
        """
        >>> Loads a binary file containing the raw OCT data and returns it as properly reshaped np-array
        -> flag 'is_dim_appendix' can be set to automatically read out dimensions of scan from file name 
        """
        t_start = time.time()
        print("Loading raw data...")  
        # path/file selection
        if is_select_path_manually :
                file_path = tk_file_selection('Please select file which contains [OCT RAW DATA]')
        else :
                file_path = path
        assert (os.path.isfile(file_path)), "Selected [FILE DOES NOT EXIST]!" 
        # process dimensionality of data
        if is_dims_in_file_name and dims == None :
                dims_string = path.split('\\')[-1].split('_')[-1].split('.bin')[0].split('x')
                dimensions = []
                for dims in dims_string :
                        dimensions.append(int(dims))
                dims = tuple(dimensions)        
        else :
                dims = dims     
        # load data
        oct_buffer = []
        with open(file_path) as _ :     
                try :
                        oct_buffer = np.fromfile(file_path, dtype=dtype)         
                except : 
                        ValueError("[COULDN'T LOAD DATA] - received erroneous array!")  
        if is_reshaping_array and oct_buffer is not None :
                oct_buffer = np.reshape(oct_buffer, (dims))
        # TODO: Figure out if transposing the array is neccessary
        #         oct_buffer = np.transpose(np.reshape(oct_buffer, (dims[1], dims[0])))
        print(f"Done loading OCT data buffer \nIt took {round(time.time() - t_start, 3)}s to load data \nDimensions of loaded data file are {dims}")
        return np.asarray(oct_buffer, dtype=dtype)

def load_data_from_image(path, dims, img_dtype, return_dtype) :
    pass

def load_data_from_images(path, dims, dtype, return_dtype) :
    pass

if __name__ == '__main__' :
        path = r'C:\Users\phili\Desktop\recon_100k_data_1536x100000.bin'
        load_data_from_bin_file(path)


# def save_data_as_images(path, data, dims, dtype) :
#     pass

# def save_data_as_bin_file(path, data, save_dtype=np.uint8) :
#     pass


# def preprocess_dimensionality(array, vector) :
#         """
#         Abstract method to evaluate and prepare (1-3)D / A-,B- or C-Scans 
#         for being performing vector-matrix-operations
#         """
#         n_dims = np.size(np.shape(array))
#         if n_dims == 1 :
#                 return np.asarray(array), np.asarray(vector)     
#         elif n_dims == 2 :
#                 return np.asarray(array), np.asarray(vector[:, np.newaxis])
#         elif n_dims == 3 :
#                 return np.asarray(array), np.asarray(vector[:, np.newaxis, np.newaxis])
#         else : 
#                 raise ValueError("[DIMENSIONALITY ERROR] while preprocessing for numpy operation")
        
# def average_nDim_independent(array) :
#         if np.size(np.shape(array)) == 1 : 
#                 print("[CAUTION] paramater is returned as is (1D array)")
#                 return array
#         elif np.size(np.shape(array)) == 2 :
#                 return np.average(array, axis=1)
#         elif np.size(np.shape(array)) == 3 :
#                 return np.average(array, axis=(1,2))
#         else : # TODO: check if necessary, since preprocessing should take care of that
#                 raise ValueError("[DIMENSION ERROR] of OCT array")


# def get_usr_selected_file() :
#         """
#         >>> Makro to load *.BIN-file selected by the user in the file explorer
#         """
#         file_path = tk_file_selection('Please select the OCT data file') 
#         path = os.path.join(f"{file_path.split('/')[0]}\\", *file_path.split('/')[1:-1])
#         folder = file_path.split('/')[-1]
#         return path, folder

# ### LOADING AND STORING ###

# def save_data_to_bin(data, path, file, dtype=np.uint16) :
#         """
#         >>> Creates appendix-string with data dimensions
#         -> Saves *.bin-file containing the data in specified path as dtype
#         NOTE that the default data type for raw oct data is uint16 -> change param if necessary
#         """
#         # make appendix
#         shape = np.shape(data)
#         appendix = ''
#         for count, value in enumerate(shape) :
#                 if count == 0 :
#                         appendix += f'_{value}'
#                 else :
#                         appendix += f'x{value}'
#         full_path = os.path.join(path, file + appendix + '.bin')
#         assert not os.path.isfile(full_path), "[FILE ERROR] file already exists"
#         with open(full_path, 'wb') as f :
#                 np.save(f, data.astype(dtype))
#                 print("Saved data successfully to {}", full_path)