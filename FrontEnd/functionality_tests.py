"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                         
        >>> main file file for OCT Recon GUI creation, methods and handling     
                                
"""

# global imports
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

# custom imports
#TODO: change to relative path import
sys.path.append("D:\PhilippDataAndFiles\Programming\Repositories\OctProcessingAndDisplay\Backend")
from recon_funcs import OctReconstructionManager as REC

#!/usr/bin/python3
# Threading example with QThread and moveToThread (PyQt5)
import sys
import time
from PyQt5 import QtWidgets, QtCore
 
class WorkerThread(QtCore.QObject):
    signalExample = QtCore.pyqtSignal(str, int)
 
    def __init__(self):
        super().__init__()
 
    @QtCore.pyqtSlot()
    def run(self):
        while True:
            # Long running task ...
            self.signalExample.emit("leet", 1337)
            time.sleep(5)
 
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)  # Init worker run() at startup (optional)
        self.worker.signalExample.connect(self.signalExample)  # Connect your signals/slots
        self.worker.moveToThread(self.workerThread)  # Move the Worker object to the Thread object
        self.workerThread.start()
 
    def signalExample(self, text, number):
        print(text)
        print(number)
 
if __name__== '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = Main()
    sys.exit(app.exec_())