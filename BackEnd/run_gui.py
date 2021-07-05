"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                         
        >>> main run file containing all the functionality to run the GUi for OCT data reconstruction     
                                
"""

# global imports
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

# custom imports 
from data_io import OctDataFileManager
from recon_funcs import OctReconstructionManagager 

# Dummy application to test some GUI functions
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)
window.show()
app.exec()

# DEC = OctReconstructionManagager()