

import os
import sys
import numpy as np
from sqlalchemy import JSON
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'BackEnd')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

# import backend module(s)
from octreconstructionmanager import OctReconstructionManager
from configdatamanager import ConfigDataManager


class UiWindowDialog(object):
    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(1000, 650)
        # TODO: pass as param 
        json_config_file_path = r"C:\Users\phili\Documents\Coding\Repositories\OctProcessingAndDisplay\Config\DefaultReconParams" 
        self.REC = OctReconstructionManager()
        self.JSON = ConfigDataManager(filename=json_config_file_path).load_json_file()
        self.disp_coeffs_tuple = self.JSON['dispersion_coefficients']
        self.bScanWidth = 1920
        self.bScanHeight = 1024
        self.bScanIndex = 0
        
        # disp coeffs
        # c3
        self.spinBox_C3 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C3.setGeometry(QtCore.QRect(20, 570, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_C3.setFont(font)
        self.spinBox_C3.setObjectName("spinBox_C3")
        # c3 label
        self.label_C3 = QtWidgets.QLabel(Dialog)
        self.label_C3.setGeometry(QtCore.QRect(20, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_C3.setFont(font)
        self.label_C3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C3.setWordWrap(False)
        self.label_C3.setObjectName("label_C3")
        # c2 
        self.spinBox_C2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C2.setGeometry(QtCore.QRect(90, 570, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_C2.setFont(font)
        self.spinBox_C2.setObjectName("spinBox_C2")
        # c2 label
        self.label_C2 = QtWidgets.QLabel(Dialog)
        self.label_C2.setGeometry(QtCore.QRect(90, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_C2.setFont(font)
        self.label_C2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C2.setWordWrap(False)
        self.label_C2.setObjectName("label_C2")

        # c1
        self.spinBox_C1 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C1.setGeometry(QtCore.QRect(160, 570, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_C1.setFont(font)
        self.spinBox_C1.setObjectName("spinBox_C1")
        # c1 label
        self.label_C1 = QtWidgets.QLabel(Dialog)
        self.label_C1.setGeometry(QtCore.QRect(160, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_C1.setFont(font)
        self.label_C1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C1.setWordWrap(False)
        self.label_C1.setObjectName("label_C1")
        
        # c0 
        self.spinBox_C0 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C0.setGeometry(QtCore.QRect(230, 570, 50, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_C0.setFont(font)
        self.spinBox_C0.setObjectName("spinBox_C0")
        # c0 label
        self.label_C0 = QtWidgets.QLabel(Dialog)
        self.label_C0.setGeometry(QtCore.QRect(230, 610, 50, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_C0.setFont(font)
        self.label_C0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C0.setWordWrap(False)
        self.label_C0.setObjectName("label_C0")
        
        # display window
        self.BScanWidget = QtWidgets.QLabel(Dialog)
        self.BScanWidget.setEnabled(False)
        self.BScanWidget.setGeometry(QtCore.QRect(10, 10, 980, 540))
        self.BScanWidget.setObjectName("BScanWidget")

        # B-scan index
        self.label_bScanIndex = QtWidgets.QLabel(Dialog)
        self.label_bScanIndex.setGeometry(QtCore.QRect(380, 600, 85, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_bScanIndex.setFont(font)
        self.label_bScanIndex.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanIndex.setWordWrap(False)
        self.label_bScanIndex.setObjectName("label_bScanIndex")
        # label B-scan index
        self.spinBox_bScanIndex = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanIndex.setGeometry(QtCore.QRect(380, 570, 85, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_bScanIndex.setFont(font)
        self.spinBox_bScanIndex.setObjectName("spinBox_bScanIndex")

        self.pushButton_loadBScan = QtWidgets.QPushButton(Dialog)
        self.pushButton_loadBScan.setGeometry(QtCore.QRect(690, 570, 100, 60))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_loadBScan.setFont(font)
        self.pushButton_loadBScan.setObjectName("pushButton_loadBScan")
        self.spinBox_bScanWidth = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanWidth.setGeometry(QtCore.QRect(480, 570, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_bScanWidth.setFont(font)
        self.spinBox_bScanWidth.setObjectName("spinBox_bScanWidth")
        self.spinBox_bScanHeight = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanHeight.setGeometry(QtCore.QRect(480, 605, 80, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_bScanHeight.setFont(font)
        self.spinBox_bScanHeight.setObjectName("spinBox_bScanHeight")
        self.label_bScanWidth = QtWidgets.QLabel(Dialog)
        self.label_bScanWidth.setGeometry(QtCore.QRect(570, 570, 101, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_bScanWidth.setFont(font)
        self.label_bScanWidth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanWidth.setWordWrap(False)
        self.label_bScanWidth.setObjectName("label_bScanWidth")
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setGeometry(QtCore.QRect(870, 580, 110, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_close.setAutoFillBackground(True)
        self.pushButton_close.setObjectName("pushButton_close")
        self.checkBox_increment5 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_increment5.setGeometry(QtCore.QRect(290, 570, 60, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_increment5.setFont(font)
        self.checkBox_increment5.setObjectName("checkBox_increment5")
        self.checkBox_increment100 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_increment100.setGeometry(QtCore.QRect(290, 590, 60, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_increment100.setFont(font)
        self.checkBox_increment100.setObjectName("checkBox_increment100")
        self.label_bScanWidth_2 = QtWidgets.QLabel(Dialog)
        self.label_bScanWidth_2.setGeometry(QtCore.QRect(570, 600, 100, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_bScanWidth_2.setFont(font)
        self.label_bScanWidth_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanWidth_2.setWordWrap(False)
        self.label_bScanWidth_2.setObjectName("label_bScanWidth_2")

        self.retranslateUi(Dialog)

        self.spinBox_C3.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C2.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C1.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C0.valueChanged.connect(self.update_disp_coeff_tuple)

        self.close_application_via_button() 

        self.pushButton_loadBScan.clicked.connect(self.load_bScan_from_binary_file)

        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BScanWidget.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_loadBScan.setText(_translate("Dialog", "Load B-scan\nfrom file"))
        self.label_C3.setText(_translate("Dialog", "C3"))
        self.label_C2.setText(_translate("Dialog", "C2"))
        self.label_C1.setText(_translate("Dialog", "C1"))
        self.label_C0.setText(_translate("Dialog", "C0"))
        self.label_bScanWidth.setText(_translate("Dialog", "Width (B-scan)"))
        self.label_bScanIndex.setText(_translate("Dialog", "B-scan Index"))
        self.pushButton_close.setText(_translate("Dialog", "Close\nApplication"))
        self.checkBox_increment5.setText(_translate("Dialog", "+/- 5"))
        self.checkBox_increment100.setText(_translate("Dialog", "+/- 10"))
        self.label_bScanWidth_2.setText(_translate("Dialog", "Width (B-scan)"))


    def close_application_via_button(self) :
        """ closes GUI via the CLOSE button -> terminates application """
        self.pushButton_close.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def update_disp_coeff_tuple(self) -> None :
        """ updates tuple (clas var) containing the dispersion correction polynominal coefficients 
        according to the current spin box combinations/settings"""
        self.disp_coeffs_tuple = (self.spinBox_DispCoeffC3.value(), self.spinBox_DispCoeffC2.value(),
                                  self.spinBox_DispCoeffC1.value(), self.spinBox_DispCoeffC0.value()) 
        print(self.disp_coeffs_tuple)

    def load_bScan_from_binary_file(self):
        """  """
        bScan_size = self.bScanHeight*self.bScanWidth
        path = self.REC._tk_file_selection()
        data = np.fromfile(path, count=bScan_size, offset=bScan_size*self.bScanIndex, dtype='<u2')
        self.data = np.swapaxes(np.reshape(data, (1920, 1024)), 0, 1)

        
    """     ****** SIGNALS ******
    Backend-connected functions     """
    def _load_oct_data(self) -> None :
        """ loads user-selected file containing OCT data and created class-vars raw data buffer and dimensions """
        print("Loading OCT data... ")
        # LOAD DATA FROM FILE: generates meta data of raw data from file name (<data_io> module)
        buffer_oct_raw_data = self.REC.load_oct_data(dtype=self.data_endianness) 
        # print(f"Loaded selected data ( shape={buffer_oct_raw_data.shape} and dtype={buffer_oct_raw_data.dtype} ) into memory")
        # self.buffer_oct_raw_data = buffer_oct_raw_data
        # self.dims_buffer_oct_raw_data = self.REC.oct_dims
        # self._update_oct_volume_dimension_display()
        # # self._check_oct_data_dims() # check if established OCT volume dimensions are what was expected 
        # self.flag_loaded_oct_data = True
        # self.set_spinbox_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
        # self.set_bScan_slider_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
    
def run() :
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiWindowDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
