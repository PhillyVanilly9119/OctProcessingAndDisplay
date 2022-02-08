"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2022 
                                        ******
                                         
        >>> run file for simple GUI to help take care of the reconstruction of entire (folders) of buffers     
                                
"""

# global imports
from genericpath import isdir
import os
import cv2
import sys
import json
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt # debug
from tkinter import messagebox

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

# import backend module(s)
from octreconstructionmanager import OctReconstructionManager
    

def process_test_buffer(manual_json_selection: bool) -> tuple:
    Rec = OctReconstructionManager()
    path = Rec._tk_file_selection()#"Please select a file for testing the reconstruction parameters:")
    recon_data = load_and_recon_file_from_json_params(path, manual_json_selection)
    recon_data = cv2.resize(recon_data, (900, 1600))
    # show recon data to user
    fig = plt.figure(figsize=(5, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    plt.title("Reconstructed and reshaped b-Scan", fontsize=15)
    ax.imshow(recon_data, cmap='gray')
    plt.draw()
    plt.pause(0.001)
    # display information and ask user if they are satisfied with the reconstructed data
    response = messagebox.askyesno("Ask Question", "Reconstruction with current parameters has finished\nPlease select \'Yes\' if you want to continue the reconstruction for all files or \'No\' if you want to adjust the reconstruction parameters")
    if response == True:
        print("[INFO:] PROCESSING - Continuing with reconstruction of all buffers in folder...")
        plt.close()
        return True, path
    elif response == False:
        print("\'No\' was selected - please adjust parameters in *.JSON-file")
        plt.close()
        return False, path
    
def load_and_recon_file_from_json_params(path: str, manual_json_selection: bool) -> np.ndarray:
    Rec = OctReconstructionManager()
    raw_data = Rec.reshape_oct_volume(Rec.load_bin_file(path), Rec.get_oct_volume_dims(path)[0])
    # load recon params
    if manual_json_selection:
        with open(Rec._tk_file_selection()) as f:
            config = json.load(f)
    else:
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config', 'Config_Reconstruction_Params.json'))) as f:
            config = json.load(f)
    # reconstruct buffer
    recon_data = Rec._run_reconstruction(raw_data,
                                         tuple(config["dispersion_coefficients"]),
                                         config["windowing_key"],
                                         config["hf_crop_samples"],
                                         config["dc_crop_samples"],
                                         config["disp_scale_range"],
                                         config["black_lvl_for_dis"])
    return recon_data

def reconstruct_and_save_all_buffers_in_folder(path: str, manual_json_selection: bool) -> None:
    Rec = OctReconstructionManager()
    raw_buffer_file_list = os.listdir(os.path.dirname(path))
    # make new dir for saving
    save_dir = os.path.join(os.path.dirname(path), "Reconstructed")
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    for file in tqdm(raw_buffer_file_list):
        rec_data = load_and_recon_file_from_json_params(os.path.join(os.path.dirname(path), file), 
                                                        manual_json_selection)
        save_file_name = "reconstructed_" + file
        rec_data.astype('uint8').tofile(os.path.join(save_dir, save_file_name))
    print("[INFO:] Done processing folder!")
        
def run(manual_json_selection: bool) -> None:
    # process and display example buffer 
    res, path = process_test_buffer(manual_json_selection)
    if res == False:
        return
    # call processing function to recon entre folder 
    reconstruct_and_save_all_buffers_in_folder(path, manual_json_selection)
    

if __name__ == '__main__' :
    print("[INFO:] Running from <singlebscanreconstructioncanvas.py > ...")
    manual_json_selection = False
    run(manual_json_selection)

