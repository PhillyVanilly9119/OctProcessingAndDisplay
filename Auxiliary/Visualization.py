"""
@author:    philipp.matten@meduniwien.ac.at
            philipp.matten@gmx.de

                                **** 
       Contains methods and functionality for OCT data visualization     
                                ****
"""
import matplotlib.pyplot as plt
from OctProcessingAndDisplay.BackEnd import data_io as IO

def plot_aScan(scan) :
        plt.figure()
        plt.plot(scan)
        plt.show()

def plot_avged_aScan(scan) :
        plt.figure()
        plt.plot(IO.average_nDim_independent(scan))
        plt.show()
        
def plot_bScan(scan, cmap='gray'):
        plt.figure()
        plt.imshow(scan, cmap=cmap)
        plt.show()

def plot_cScan_slice(scan, slice_id) :
        plt.figure()
        plt.imshow(scan[:,:,slice_id], cmap='gray')
        plt.show()