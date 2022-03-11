"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> Contains methods and functionality for OCT raw data file handling and conversion     
                                
"""

# global imports
import re
import os
from tqdm import tqdm
import numpy as np

# custom imports
import octdatafilemanager as IO


class OctRawDataManager(IO.OctDataFileManager) :
    def __init__(self, dtype_loading='>u2') -> None :
        super().__init__(dtype_loading=dtype_loading)
        self.dtype_raw = np.uint16
        self.main_folder = self._tk_folder_selection()
        self.full_file_list_full_path = self._get_list_of_files_full_path()
    
    def _get_list_of_files_full_path(self) -> None :
        """ returns a list of all complete paths from all files in the self.main_dir """
        return [os.path.join(self.main_folder, f) for f in os.listdir(self.main_folder) if os.path.isfile(os.path.join(self.main_folder, f))]
    
    def _get_list_of_files(self) -> None :
        """ returns a list of all files in the self.main_dir """
        return [f for f in os.listdir(self.main_folder) if os.path.isfile(os.path.join(self.main_folder, f))]
    
    def _get_sorted_scan_list(self) -> list :
        """ returns a list with all sorted """
        file_list_numbers = []
        for file in self._get_list_of_files() :
            file_list_numbers.append(file)
        return self.sort_scan_list_after_nums(file_list_numbers)  
    
    def _load_bins_in_dir(self) -> np.array :
        """ """
        data_stack = []
        for file in tqdm(self._get_sorted_scan_list()) :
            c_file = os.path.join(self.main_folder, file)
            c_buffer = np.reshape(np.fromfile(c_file, dtype='<u2'), (5120, 500))
            data_stack.append(c_buffer)
        return np.swapaxes(np.asarray(data_stack), 1, 0)
                                  
    def sort_scan_list_after_nums(self, file_list_numbers) -> list :
        """ returns sorted list numbers in file names """
        def natural_keys(text):
            def atoi(text):
                return int(text) if text.isdigit() else text
            return [ atoi(c) for c in re.split(r'(\d+)', text) ]
        
        file_list_numbers.sort(key=natural_keys)
        return file_list_numbers
    
    def check_if_files_complete(self) :
        """ TODO: implement """
        file_list_nums = self._get_sorted_scan_list()
        if len(file_list_nums)==int(file_list_nums[-1])+1 :
            return True
        else :
            return False


if __name__ == "__main__" :
    RDM = OctRawDataManager()