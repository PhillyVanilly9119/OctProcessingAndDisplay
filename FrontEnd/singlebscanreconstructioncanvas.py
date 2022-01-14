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
import PIL
# import numpy as np
import json
import matplotlib.pyplot as plt # debug
from tkinter.filedialog import Tk, askopenfilename

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

# import backend module(s)
from octreconstructionmanager import OctReconstructionManager
    
def process_test_buffer(manual_json_selection: bool=False) :
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
    # recon_data = recon_data.resize(recon_data, (1600, 900))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(recon_data, cmap='gray')
    plt.show()
    # display information and ask user if they are satisfied with the reconstructed data
    
    ## TODO: think how the functions can be used ideally to reach goal of
    ## reconstructing entire folder with raw b-Scans
    # ask user to open folder with all raw b-Scans 
    
    # Loop through and process all b-scans

def run():
    process_test_buffer()
    

# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from < singlebscanreconstructioncanvas.py > ...")
    run()

