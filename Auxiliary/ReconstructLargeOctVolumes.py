"""
                                        ******
            @author: @Philipp Matten
            @contact: philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2022 
                                        ******
                                         
                >>> main file for OCT Recon GUI creation, methods and handling     
                                
"""

# global imports
import os
import sys
import matplotlib
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

from octreconstructionmanager import OctReconstructionManager

def process_and_save_bScan_wise(data: np.array, file_path: str, file_name: str) -> None:
    enface = []
    REC = OctReconstructionManager()
    print(data.shape)
    for c_len in tqdm(range(data.shape[-1])):
        frame = REC._run_reconstruction(buffer = data[:,:,c_len],
                                        disp_coeffs = (-8, 120, 0, 0),
                                        wind_key ="hann")
        enface.append(frame)
    enface = np.asarray(np.argmax(enface))
    plt.imshow(enface)
    plt.show()
    # matplotlib.image.imsave(r'C:\Users\PhilippsLabLaptop\Desktop\test.png', enface,  cmap="jet")    

def run() -> None:
    REC = OctReconstructionManager(dtype_loading='>u2')
    data = REC.load_oct_data()
    process_and_save_bScan_wise(data, r"C:\Users\PhilippsLabLaptop\Desktop", "test")

# for testing and debugging purposes
if __name__ == '__main__' :
    print("[INFO:] Running from     < reconstructlargeoctvolumes.py >     ...")
    run()