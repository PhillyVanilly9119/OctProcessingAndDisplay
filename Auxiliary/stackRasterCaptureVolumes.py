"""

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering

"""

import os
import numpy as np
#import matplotlib.pyplot as plt
from tkinter.filedialog import Tk, askdirectory


def clean_path_selection(text: str) :
    root = Tk()
    root.withdraw()
    path = askdirectory(title=text, mustexist=True)
    root.destroy()
    return path


def find_indices_in_file_names(path: str=None):
    # Add logic to find max index for vols and B-scan/vol
    if path is None:
        path = clean_path_selection("")
    main_file_list = os.listdir(path)
    split_list = [file.split('.bin')[0] for file in main_file_list]
    split_list = [[file.split('_')[0].split('rasterVol')[1], 
                   file.split('_')[1].split('bufferNo.')[1]] for file in split_list]
    return dict(zip( main_file_list, split_list )), split_list
   
    
def load_raw_bScan(path: str, dims: tuple, is_dims_in_file_name: bool=False, dtype='uint16'):
    #TODO: Flag has to be implemented
    if is_dims_in_file_name:
        pass
    assert os.path.isfile(path)
    buffer = np.fromfile(path, dtype=dtype)
    return np.reshape(buffer, dims)


def stack_bScans(path: str):
    stack = []
    print("[INFO:] Loading and stacking B-scans tzo C-scan...")
    for root, _, files in os.walk(os.path.abspath(path)):
        for file in files:
            c_file_path = os.path.join(root, file)
            if os.path.isfile(c_file_path):
                # print(c_file_path)
                dims = (int(c_file_path.split('_')[-1].split('.bin')[0].split('x')[0]), 
                       int(c_file_path.split('_')[-1].split('.bin')[0].split('x')[1]))
                # c_vol_idx = int(c_file_path.split('_')[-2][-3:]) # debug
                stack.append(load_raw_bScan(c_file_path, dims))
    stack = np.array(stack, dtype='uint16')
    stack = np.swapaxes(stack, 0, 1)
    print("[INFO:] Done!")
    return stack


def save_stacked_vol(stack: np.ndarray, path_saving: str, file_name: str="StackedOctVolume") -> None :
    if not os.path.isdir(path_saving):
        os.mkdir(path_saving)
    print("[INFO:] Saving stacked OCT volume data to disk - this might take a while...")
    stack.astype(np.uint16).tofile(os.path.join(path_saving, f"{file_name}_{stack.shape[0]}x{stack.shape[1]}x{stack.shape[2]}_.bin"))
    print(f"[INFO:] Done saving OCT volume data to {os.path.join(path_saving, file_name)} !")
    
    
def main(): 
    save_stacked_vol(stack_bScans(clean_path_selection("Please select folder with all B-scans in it:")), 
                     r"C:\Users\phili\Desktop" , "testVol.bin")
    

if __name__ == '__main__':
    main()
