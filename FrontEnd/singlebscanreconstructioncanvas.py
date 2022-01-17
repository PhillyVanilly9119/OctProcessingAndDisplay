"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2022 
                                        ******
                                         
        >>> run file for simple GUI to help take care of the reconstruction of entire (folders) of buffers     
                                
"""

# global imports
import os
import cv2
import sys
import json
import matplotlib.pyplot as plt # debug
from tkinter import messagebox

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

# import backend module(s)
from octreconstructionmanager import OctReconstructionManager
    

def process_test_buffer(manual_json_selection: bool) -> bool:
    Rec = OctReconstructionManager()
    path = Rec._tk_file_selection()#"Please select a file for testing the reconstruction parameters:")
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
        return True, path
    elif response == False:
        print("\'No\' was selected - please adjust parameters in *.JSON-file")
        return False, path

def run(manual_json_selection: bool):
    # process and display 
    res, path = process_test_buffer(manual_json_selection)
    if res == False:
        return
    # call processing function to recon entre folder 
    

# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from <singlebscanreconstructioncanvas.py > ...")
    manual_json_selection = False
    run(manual_json_selection)

