"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                         
        >>> contains handling of reconstruction functions that are called by GUI events and actions     
                                
"""

#TODO: change to relative path import
sys.path.append("D:\PhilippDataAndFiles\Programming\Repositories\OctProcessingAndDisplay\Backend")
from recon_funcs import OctReconstructionManager as REC

class ReconFunctionImports() :
    def __init__(self) -> None:
        super().__init__()
        self.data = REC.return_oct_cube()   