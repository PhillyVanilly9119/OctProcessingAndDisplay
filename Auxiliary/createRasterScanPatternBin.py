# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:32:10 2020

@author:    Philipp
            philipp.matten@meduniwien.ac.at

@copyright: Medical University of Vienna,
            Center for Medical Physics and Biomedical Engineering
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import Tk, askdirectory, askopenfilename

def createScanPattern(bLen, cLen, flybackPnts) :
    pattern = np.zeros((cLen * (bLen + flybackPnts), 4))
    x_mapping_coord = np.zeros(bLen + flybackPnts)
    y_mapping_coord = np.zeros(bLen + flybackPnts)
    x_mapping_coord[:bLen] = range(1, bLen+1) # x-mapping-position, for each C-scan 1:len(bLen+1)
    for line in range(cLen) : # Loop though C-scans
        y_mapping_coord[:bLen] = line # only y-mapping-position of tuple if valid point, i.e. if currentSpot <= bLen 
        pattern[line * len(x_mapping_coord) : line*len(x_mapping_coord) + len(x_mapping_coord), 0] = x_mapping_coord # spots in optical Y-direction
        pattern[line * len(x_mapping_coord) : line*len(x_mapping_coord) + len(x_mapping_coord), 1] = y_mapping_coord # spots in optical X-direction
    return np.asarray(pattern, dtype=np.uint32)

def writeScanTable2BinFile(table, file_name, path='', is_manual_path_selection=False, dtype=np.uint32) :
    print(f'File you are about to save contains {int(sys.getsizeof(table)/8)} remapping positions') 
    if is_manual_path_selection :
        ###
        # TODO: Change once the Backend can be globally imported
        root = Tk()
        root.withdraw()
        path = askdirectory(title='Please select a directory were you want to save the pattern', mustexist=True)
        root.destroy()
        ###
    path_saving = os.path.join(path, file_name + '.bin')
    table.astype(dtype).tofile(path_saving)
    
if __name__ == '__main__' :
    rasterPattern = createScanPattern(1024, 512, 128)
    writeScanTable2BinFile(rasterPattern, 'test', is_manual_path_selection=True)