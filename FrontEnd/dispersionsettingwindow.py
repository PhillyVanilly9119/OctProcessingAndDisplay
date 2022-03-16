

import os
import sys
import cv2
import numpy as np
from sqlalchemy import JSON, false
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
        Dialog.resize(1200, 800)
        # ----------- class variables ------------
        # TODO: pass as params
        json_config_file_path = os.path.join(os.getcwd(), 'Config', 'DefaultReconParams')
        self.REC = OctReconstructionManager()
        self.JSON = ConfigDataManager(filename=json_config_file_path).load_json_file()
        self.disp_coeffs_tuple = self.JSON['dispersion_coefficients']
        self.bScanWidth = 511 # default param
        self.bScanHeight = 13312 # default param
        self.bScanIndex = 256 # default param
        self.flag_loaded_oct_data = False
        # ----------- Display Widgets --------------
        # display window
        self.BScanWidget = QtWidgets.QLabel(Dialog)
        self.BScanWidget.setEnabled(False)
        self.BScanWidget.setGeometry(QtCore.QRect(10, 10, 1180, 700))
        self.BScanWidget.setObjectName("BScanWidget")
        # -------------- Spin Boxes and Labels ------------------
        # disp coeffs
        # c3
        self.spinBox_C3 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C3.setGeometry(QtCore.QRect(20, 720, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_C3.setFont(font)
        self.spinBox_C3.setObjectName("spinBox_C3")
        self.spinBox_C3.setRange(-200,200)
        self.spinBox_C3.setValue(self.disp_coeffs_tuple[0])
        # c3 label
        self.label_C3 = QtWidgets.QLabel(Dialog)
        self.label_C3.setGeometry(QtCore.QRect(20, 760, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_C3.setFont(font)
        self.label_C3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C3.setWordWrap(False)
        self.label_C3.setObjectName("label_C3")
        self.label_C3.setAlignment(QtCore.Qt.AlignCenter)
        # c2 
        self.spinBox_C2 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C2.setGeometry(QtCore.QRect(90, 720, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_C2.setFont(font)
        self.spinBox_C2.setObjectName("spinBox_C2")
        self.spinBox_C2.setRange(-200,200)
        self.spinBox_C2.setValue(self.disp_coeffs_tuple[1])
        # c2 label
        self.label_C2 = QtWidgets.QLabel(Dialog)
        self.label_C2.setGeometry(QtCore.QRect(90, 760, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_C2.setFont(font)
        self.label_C2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C2.setWordWrap(False)
        self.label_C2.setObjectName("label_C2")
        self.label_C2.setAlignment(QtCore.Qt.AlignCenter)
        # c1
        self.spinBox_C1 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C1.setGeometry(QtCore.QRect(160, 720, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_C1.setFont(font)
        self.spinBox_C1.setObjectName("spinBox_C1")
        self.spinBox_C1.setRange(-200,200)
        self.spinBox_C1.setValue(self.disp_coeffs_tuple[2])
        # c1 label
        self.label_C1 = QtWidgets.QLabel(Dialog)
        self.label_C1.setGeometry(QtCore.QRect(160, 760, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_C1.setFont(font)
        self.label_C1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C1.setWordWrap(False)
        self.label_C1.setObjectName("label_C1")
        self.label_C1.setAlignment(QtCore.Qt.AlignCenter)
        # c0 
        self.spinBox_C0 = QtWidgets.QSpinBox(Dialog)
        self.spinBox_C0.setGeometry(QtCore.QRect(230, 720, 60, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_C0.setFont(font)
        self.spinBox_C0.setObjectName("spinBox_C0")
        self.spinBox_C0.setRange(-200,200)
        self.spinBox_C0.setValue(self.disp_coeffs_tuple[3])
        # c0 label
        self.label_C0 = QtWidgets.QLabel(Dialog)
        self.label_C0.setGeometry(QtCore.QRect(230, 760, 60, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_C0.setFont(font)
        self.label_C0.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_C0.setWordWrap(False)
        self.label_C0.setObjectName("label_C0")
        self.label_C0.setAlignment(QtCore.Qt.AlignCenter)
        # B-scan index
        self.spinBox_bScanIndex = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanIndex.setGeometry(QtCore.QRect(450, 720, 85, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_bScanIndex.setFont(font)
        self.spinBox_bScanIndex.setObjectName("spinBox_bScanIndex")
        self.spinBox_bScanIndex.setRange(0,4096)
        self.spinBox_bScanIndex.setValue(self.bScanIndex)
        # label B-scan index
        self.label_bScanIndex = QtWidgets.QLabel(Dialog)
        self.label_bScanIndex.setGeometry(QtCore.QRect(450, 750, 120, 25))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_bScanIndex.setFont(font)
        self.label_bScanIndex.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanIndex.setWordWrap(False)
        self.label_bScanIndex.setObjectName("label_bScanIndex")
        # B-scan width
        self.spinBox_bScanWidth = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanWidth.setGeometry(QtCore.QRect(580, 720, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_bScanWidth.setFont(font)
        self.spinBox_bScanWidth.setObjectName("spinBox_bScanWidth")
        self.spinBox_bScanWidth.setRange(0,2048)
        self.spinBox_bScanWidth.setValue(self.bScanWidth)
        # label for spinbox to set B-scan width
        self.label_bScanWidth = QtWidgets.QLabel(Dialog)
        self.label_bScanWidth.setGeometry(QtCore.QRect(670, 725, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_bScanWidth.setFont(font)
        self.label_bScanWidth.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanWidth.setWordWrap(False)
        self.label_bScanWidth.setObjectName("label_bScanWidth")
        # B-scan Heigth
        self.spinBox_bScanHeight = QtWidgets.QSpinBox(Dialog)
        self.spinBox_bScanHeight.setGeometry(QtCore.QRect(580, 755, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.spinBox_bScanHeight.setFont(font)
        self.spinBox_bScanHeight.setObjectName("spinBox_bScanHeight")
        self.spinBox_bScanHeight.setRange(0,13312)
        self.spinBox_bScanHeight.setValue(self.bScanHeight)
        # label of spinbox to set B-scan heigth
        self.label_bScanHeight = QtWidgets.QLabel(Dialog)
        self.label_bScanHeight.setGeometry(QtCore.QRect(670, 760, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.label_bScanHeight.setFont(font)
        self.label_bScanHeight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_bScanHeight.setWordWrap(False)
        self.label_bScanHeight.setObjectName("label_bScanHeight")
        # ------------- Push Buttons ---------------
        # button to load B-scan with selected params 
        self.pushButton_loadBScan = QtWidgets.QPushButton(Dialog)
        self.pushButton_loadBScan.setGeometry(QtCore.QRect(960, 715, 110, 75))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.pushButton_loadBScan.setFont(font)
        self.pushButton_loadBScan.setObjectName("pushButton_loadBScan")
        # putton to start recon of current frame
        self.pushButton_reconBscan = QtWidgets.QPushButton(Dialog)
        self.pushButton_reconBscan.setGeometry(QtCore.QRect(840, 715, 110, 75))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.pushButton_reconBscan.setFont(font)
        self.pushButton_reconBscan.setObjectName("pushButton_reconBscan")
        # button to end application
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setGeometry(QtCore.QRect(1080, 715, 110, 75))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setWeight(75)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.pushButton_close.setAutoFillBackground(True)
        self.pushButton_close.setObjectName("pushButton_close")
        # --------------- Check Boxes -----------------
        # check box to set +/- 5 increments for spinbox
        self.checkBox_increment5 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_increment5.setGeometry(QtCore.QRect(310, 730, 100, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        self.checkBox_increment5.setFont(font)
        self.checkBox_increment5.setObjectName("checkBox_increment5")
        # check box to set +/- 10 increments for spinbox
        self.checkBox_increment10 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_increment10.setGeometry(QtCore.QRect(310, 755, 100, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        self.checkBox_increment10.setFont(font)
        self.checkBox_increment10.setObjectName("checkBox_increment10")
        # self.checkBox_increment10.setChecked(True)
        
        # assign default-texts to all labels
        self.retranslateUi(Dialog)

        """ ****** SIGNALS ******   """
        self.spinBox_C3.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C2.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C1.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_C0.valueChanged.connect(self.update_disp_coeff_tuple)
        
        self.pushButton_reconBscan.clicked.connect(self.run_recon_for_current_settings)
        
        self.checkBox_increment5.stateChanged.connect(self.update_checkboxes)
        self.checkBox_increment10.stateChanged.connect(self.update_checkboxes)
        
        self.spinBox_bScanHeight.valueChanged.connect(self.update_bScan_height)
        self.spinBox_bScanWidth.valueChanged.connect(self.update_bScan_width)
        self.spinBox_bScanIndex.valueChanged.connect(self.update_bScan_index)        
        
        self.close_application_via_button() 

        self.pushButton_loadBScan.clicked.connect(self.load_bScan_from_binary_file)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BScanWidget.setText(_translate("Dialog", "TextLabel"))
        self.label_C3.setText(_translate("Dialog", "C3"))
        self.label_C2.setText(_translate("Dialog", "C2"))
        self.label_C1.setText(_translate("Dialog", "C1"))
        self.label_C0.setText(_translate("Dialog", "C0"))
        self.label_bScanWidth.setText(_translate("Dialog", "Width (B-scan)"))
        self.label_bScanHeight.setText(_translate("Dialog", "Height (B-scan)"))
        self.label_bScanIndex.setText(_translate("Dialog", "B-scan Index"))
        self.pushButton_close.setText(_translate("Dialog", "Close\nApplication"))
        self.pushButton_reconBscan.setText(_translate("Dialog", "Reconstruct\nB-scan"))
        self.pushButton_loadBScan.setText(_translate("Dialog", "Load B-scan\nfrom file"))
        self.checkBox_increment5.setText(_translate("Dialog", "+/- 5"))
        self.checkBox_increment10.setText(_translate("Dialog", "+/- 10"))

    def _is_no_oct_data_loaded(self) -> bool :
        """ evaluate if OCT data been loaded (call _load_oct_data() -method), 
        which sets self.flag_loaded_oct_data to true 
        >>> diplays error window if there is no previously loaded data """
        if self.flag_loaded_oct_data :
            return True
        else :
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Invalid request")
            msg_box.setText("[ERROR] No Data selected! Please select data file\n(by pressing the \"Load OCT Data\" button)")
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            x = msg_box.exec_()
            return False

    def update_checkboxes(self) -> None:
        if self.checkBox_increment5.isChecked() == False and self.checkBox_increment10.isChecked() == False:
            self.spinBox_C0.setSingleStep(1)
            self.spinBox_C1.setSingleStep(1)
            self.spinBox_C2.setSingleStep(1)
            self.spinBox_C3.setSingleStep(1)
            
        if self.checkBox_increment5.isChecked() == True:
            self.checkBox_increment10.setEnabled(False) 
            self.spinBox_C0.setSingleStep(5)
            self.spinBox_C1.setSingleStep(5)
            self.spinBox_C2.setSingleStep(5)
            self.spinBox_C3.setSingleStep(5)
            
        if self.checkBox_increment10.isChecked() == True:
            self.checkBox_increment5.setEnabled(False)
            self.spinBox_C0.setSingleStep(10)
            self.spinBox_C1.setSingleStep(10)
            self.spinBox_C2.setSingleStep(10)
            self.spinBox_C3.setSingleStep(10)    
            
        if self.checkBox_increment5.isChecked() == False:
            self.checkBox_increment10.setEnabled(True)
            
        if self.checkBox_increment10.isChecked() == False:
            self.checkBox_increment5.setEnabled(True)        

    def close_application_via_button(self) :
        """ closes GUI via the CLOSE button -> terminates application """
        self.pushButton_close.clicked.connect(QtCore.QCoreApplication.instance().quit)

    def update_disp_coeff_tuple(self) -> None :
        self.disp_coeffs_tuple = (self.spinBox_C3.value(), self.spinBox_C2.value(),
                                  self.spinBox_C1.value(), self.spinBox_C0.value()) 
        # self.spinBox_C0.setValue(self.disp_coeffs_tuple[3])
        # self.spinBox_C1.setValue(self.disp_coeffs_tuple[2])
        # self.spinBox_C2.setValue(self.disp_coeffs_tuple[1])
        # self.spinBox_C3.setValue(self.disp_coeffs_tuple[0])
        print(self.disp_coeffs_tuple)
            
    def update_bScan_height(self) -> None:
        self.bScanHeight = self.spinBox_bScanHeight.value()
        
    def update_bScan_width(self) -> None:
        self.bScanWidth = self.spinBox_bScanWidth.value()
        
    def update_bScan_index(self) -> None:
        self.bScanIndex = self.spinBox_bScanIndex.value()

    def load_bScan_from_binary_file(self):
        """  """
        bScan_size = self.bScanHeight*self.bScanWidth
        path = self.REC._tk_file_selection()
        if path is None:
            print("No file has been chosen - returning...")
            return
        data = np.fromfile(path, count=bScan_size, offset=bScan_size*self.bScanIndex, dtype='<u2')
        self.data = np.swapaxes(np.reshape(data, (self.bScanHeight, self.bScanWidth)), 0, 1)
        if self.data is not None:
            self.flag_loaded_oct_data = True
        self.spinBox_bScanWidth.setEnabled(False)
        self.spinBox_bScanHeight.setEnabled(False)
        self.spinBox_bScanIndex.setEnabled(False)
        # self.run_recon_for_current_settings()

    def run_recon_for_current_settings(self) :
        """ runs recosntruction og B-scan with the current recon-params """
        if not self._is_no_oct_data_loaded():
            return
        print("Reconstructing...")
        # create/update current b-Scan
        recon_buffer = self.REC._run_reconstruction(self.data, disp_coeffs=self.disp_coeffs_tuple,
                                                      wind_key=self.JSON['windowing_key'], 
                                                      samples_hf_crop=self.JSON['hf_crop_samples'], 
                                                      samples_dc_crop=self.JSON['dc_crop_samples'], 
                                                      scale_fac=self.JSON['disp_scale_factor'], 
                                                      blck_lvl=self.JSON['black_lvl_for_dis'],
                                                      is_bg_sub=self.JSON['is_substract_background'],
                                                      show_scaled_data=self.JSON['is_scale_data_for_display'])
        recon_buffer = cv2.cvtColor( recon_buffer, cv2.COLOR_BAYER_GR2GRAY )
        display_buffer = QtGui.QImage(recon_buffer.data.tobytes(), 
                                     recon_buffer.shape[1], recon_buffer.shape[0], 
                                     QtGui.QImage.Format_Grayscale8)
        self.BScanWidget.setPixmap( QtGui.QPixmap(display_buffer) )
        self.BScanWidget.setScaledContents(True) 
        
    
def run() :
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiWindowDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
