"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2020 Medical University of Vienna 
                                        ******
                                         
        >>> main file for OCT Recon GUI creation, methods and handling     
                                
"""
# global imports
import sys

# custom imports
sys.path.append(r"D:\PhilippDataAndFiles\Programming\Repositories\OctProcessingAndDisplay\Backend")
from data_io import OctDataFileManager
from recon_funcs import OctReconstructionManager

from PyQt5 import QtCore, QtGui, QtWidgets

class UiWindowDialog(object):
    
    # Is this contructor pointless? 
    # Can I call setupUi somehow from this constructor?   
    def __init__(self) -> None:
        super().__init__()
        self.IO = OctDataFileManager()
        self.REC = OctReconstructionManager()
        # print(self.IO)
        # print(self.REC)
         
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        self.LeftBScanWindow = QtWidgets.QLabel(Dialog)
        self.LeftBScanWindow.setGeometry(QtCore.QRect(30, 20, 920, 560))
        self.LeftBScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LeftBScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.LeftBScanWindow.setText("")
        self.LeftBScanWindow.setObjectName("LeftBScanWindow")
        self.Right_BScanWindow = QtWidgets.QLabel(Dialog)
        self.Right_BScanWindow.setGeometry(QtCore.QRect(970, 20, 920, 560))
        self.Right_BScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Right_BScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Right_BScanWindow.setText("")
        self.Right_BScanWindow.setObjectName("Right_BScanWindow")
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setGeometry(QtCore.QRect(1790, 1010, 100, 35))
        font = QtGui.QFont()
        font.setFamily("Neue Haas Grotesk Text Pro")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setDefault(True)
        self.pushButton_close.setObjectName("pushButton_close")
        self.DisplayOptionsWindow = QtWidgets.QLabel(Dialog)
        self.DisplayOptionsWindow.setGeometry(QtCore.QRect(30, 600, 650, 450))
        self.DisplayOptionsWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DisplayOptionsWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DisplayOptionsWindow.setText("")
        self.DisplayOptionsWindow.setObjectName("DisplayOptionsWindow")
        self.EnfaceDisplayWindow = QtWidgets.QLabel(Dialog)
        self.EnfaceDisplayWindow.setGeometry(QtCore.QRect(700, 650, 400, 400))
        self.EnfaceDisplayWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.EnfaceDisplayWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.EnfaceDisplayWindow.setText("")
        self.EnfaceDisplayWindow.setObjectName("EnfaceDisplayWindow")
        self.pushButton_loadOctData = QtWidgets.QPushButton(Dialog)
        self.pushButton_loadOctData.setGeometry(QtCore.QRect(1789, 880, 100, 120))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_loadOctData.setFont(font)
        self.pushButton_loadOctData.setDefault(True)
        self.pushButton_loadOctData.setFlat(False)
        self.pushButton_loadOctData.setObjectName("pushButton_loadOctData")
        # LEFT = HORIZONTAL B-scan selection spin box
        self.spinBox_leftBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_leftBScanWindow.setGeometry(QtCore.QRect(890, 600, 60, 30))
        self.spinBox_leftBScanWindow.setObjectName("spinBox_leftBScanWindow")
        # RIGHT = VERTICAL B-scan selection spin box
        self.spinBox_rightBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_rightBScanWindow.setGeometry(QtCore.QRect(970, 600, 60, 30))
        self.spinBox_rightBScanWindow.setObjectName("spinBox_rightBScanWindow")
        self.pushButton_shwEnFace = QtWidgets.QPushButton(Dialog)
        self.pushButton_shwEnFace.setGeometry(QtCore.QRect(1120, 830, 230, 40))
        self.pushButton_shwEnFace.setObjectName("pushButton_shwEnFace")
        self.pushButton_displayAScanAtIntersection = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayAScanAtIntersection.setGeometry(QtCore.QRect(1120, 890, 230, 40))
        self.pushButton_displayAScanAtIntersection.setObjectName("pushButton_displayAScanAtIntersection")
        self.pushButton_displayDispersionCurves = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayDispersionCurves.setGeometry(QtCore.QRect(1120, 950, 230, 40))
        self.pushButton_displayDispersionCurves.setObjectName("pushButton_displayDispersionCurves")
        self.horizontalSlider_leftBScanWindow = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_leftBScanWindow.setGeometry(QtCore.QRect(700, 600, 160, 30))
        self.horizontalSlider_leftBScanWindow.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_leftBScanWindow.setObjectName("horizontalSlider_leftBScanWindow")
        self.horizontalSlider_rightBScanWindow = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_rightBScanWindow.setGeometry(QtCore.QRect(1050, 600, 160, 30))
        self.horizontalSlider_rightBScanWindow.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_rightBScanWindow.setObjectName("horizontalSlider_rightBScanWindow")
        self.pushButton_displayWindowingFunctions = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayWindowingFunctions.setGeometry(QtCore.QRect(1120, 1010, 230, 40))
        self.pushButton_displayWindowingFunctions.setObjectName("pushButton_displayWindowingFunctions")
        self.pushButton_runReconstruction = QtWidgets.QPushButton(Dialog)
        self.pushButton_runReconstruction.setGeometry(QtCore.QRect(1120, 650, 230, 80))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_runReconstruction.setFont(font)
        self.pushButton_runReconstruction.setDefault(True)
        self.pushButton_runReconstruction.setFlat(False)
        self.pushButton_runReconstruction.setObjectName("pushButton_runReconstruction")
        self.label_DisperisonCoefficients_ = QtWidgets.QLabel(Dialog)
        self.label_DisperisonCoefficients_.setGeometry(QtCore.QRect(1630, 640, 245, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisperisonCoefficients_.setFont(font)
        self.label_DisperisonCoefficients_.setObjectName("label_DisperisonCoefficients_")
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1630, 680, 240, 60))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.spinBox_DispCoeffC2 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC2.setObjectName("spinBox_DispCoeffC2")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC2, 1, 1, 1, 1)
        self.label_DispCoeffC2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DispCoeffC2.setFont(font)
        self.label_DispCoeffC2.setObjectName("label_DispCoeffC2")
        self.gridLayout.addWidget(self.label_DispCoeffC2, 0, 1, 1, 1)
        self.spinBox_DispCoeffC1 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC1.setObjectName("spinBox_DispCoeffC1")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC1, 1, 2, 1, 1)
        self.spinBox_DispCoeffC3 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC3.setObjectName("spinBox_DispCoeffC3")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC3, 1, 0, 1, 1)
        self.spinBox_DispCoeffC0 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC0.setObjectName("spinBox_DispCoeffC0")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC0, 1, 3, 1, 1)
        self.label_DispCoeffC3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_DispCoeffC3.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DispCoeffC3.setFont(font)
        self.label_DispCoeffC3.setObjectName("label_DispCoeffC3")
        self.gridLayout.addWidget(self.label_DispCoeffC3, 0, 0, 1, 1)
        self.label_DispCoeffC1 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DispCoeffC1.setFont(font)
        self.label_DispCoeffC1.setObjectName("label_DispCoeffC1")
        self.gridLayout.addWidget(self.label_DispCoeffC1, 0, 2, 1, 1)
        self.label_DispCoeffC0 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DispCoeffC0.setFont(font)
        self.label_DispCoeffC0.setObjectName("label_DispCoeffC0")
        self.gridLayout.addWidget(self.label_DispCoeffC0, 0, 3, 1, 1)
        self.label_ConsoleLog = QtWidgets.QLabel(Dialog)
        self.label_ConsoleLog.setGeometry(QtCore.QRect(1380, 820, 380, 230))
        self.label_ConsoleLog.setFrameShape(QtWidgets.QFrame.Box)
        self.label_ConsoleLog.setMidLineWidth(1)
        self.label_ConsoleLog.setObjectName("label_ConsoleLog")
        self.label_DisplayOptions_ = QtWidgets.QLabel(Dialog)
        self.label_DisplayOptions_.setGeometry(QtCore.QRect(1150, 780, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisplayOptions_.setFont(font)
        self.label_DisplayOptions_.setObjectName("label_DisplayOptions_")
        self.comboBox_windowingOptions = QtWidgets.QComboBox(Dialog)
        self.comboBox_windowingOptions.setGeometry(QtCore.QRect(1370, 680, 230, 30))
        self.comboBox_windowingOptions.setObjectName("comboBox_windowingOptions")
        self.comboBox_windowingOptions.addItem("Von-Hann window (default)") # check if 1st item really is default
        self.comboBox_windowingOptions.addItem("Hamming window")
        self.comboBox_windowingOptions.addItem("Kaiser-Bessel window")
        self.comboBox_windowingOptions.addItem("Gaussian (narrow) window") # pass different sigmas as params for different Gaussian-filters
        self.comboBox_windowingOptions.addItem("Gaussian (medium) window")
        self.comboBox_windowingOptions.addItem("Gaussian (wide) window ")
        self.label_WindowingFunction_ = QtWidgets.QLabel(Dialog)
        self.label_WindowingFunction_.setGeometry(QtCore.QRect(1370, 640, 215, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_WindowingFunction_.setFont(font)
        self.label_WindowingFunction_.setObjectName("label_WindowingFunction_")

        # set Labels and
        self.retranslateUi(Dialog)
        
        # load OCT data
        self.pushButton_loadOctData.clicked.connect(self._load_oct_data)
        # exit if close button is pressed
        self.close_application_via_button()            
        """
        1. if and only if OCT data cube has been loaded 
            Options:
                i) display reconstructed selected A-scans
        """
        
        self.horizontalSlider_leftBScanWindow.valueChanged['int'].connect(self.spinBox_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.horizontalSlider_leftBScanWindow.setValue)
        self.horizontalSlider_rightBScanWindow.valueChanged['int'].connect(self.spinBox_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.horizontalSlider_rightBScanWindow.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.pushButton_loadOctData.setText(_translate("Dialog", "Load\nOCT\nData"))
        self.pushButton_shwEnFace.setText(_translate("Dialog", "Show en face OCT"))
        self.pushButton_displayAScanAtIntersection.setText(_translate("Dialog", "Display A-scan at Intersection"))
        self.pushButton_displayDispersionCurves.setText(_translate("Dialog", "Plot Dispersion Curves"))
        self.pushButton_displayWindowingFunctions.setText(_translate("Dialog", "Plot Windowing Function"))
        self.pushButton_runReconstruction.setText(_translate("Dialog", "Reconstruct"))
        self.label_DisperisonCoefficients_.setText(_translate("Dialog", "Dispersion Coefficients"))
        self.label_DispCoeffC2.setText(_translate("Dialog", "C2"))
        self.label_DispCoeffC3.setText(_translate("Dialog", "C3"))
        self.label_DispCoeffC1.setText(_translate("Dialog", "C1"))
        self.label_DispCoeffC0.setText(_translate("Dialog", "C0"))
        self.label_ConsoleLog.setText(_translate("Dialog", "Console prints"))
        self.label_DisplayOptions_.setText(_translate("Dialog", "Display Options"))
        self.label_WindowingFunction_.setText(_translate("Dialog", "Windowing Function"))
  
    #### Backend-connected functions ####

    def run_recon_for_current_settings(self) :
        pass
        
    def _load_oct_data(self) -> None :
        """ loads user-selected file containing OCT data and created class-vars raw data buffer and dimensions """
        print("Loading OCT data... ")
        buffer_oct_raw_data = self.IO.load_oct_data() 
        print(f"Loaded selected buffer (shape={buffer_oct_raw_data.shape}) into memory")
        self.buffer_oct_raw_data = buffer_oct_raw_data
        self.dims_buffer_oct_raw_data = buffer_oct_raw_data.shape
        self.set_spinbox_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
        self.set_bScan_slider_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
        
    def set_bScan_slider_max_values(self, x_max, y_max) :
        """ Sets the values of the horizontal sliders to OCT (x,y) volume dims
        left = horizontal/y_max, right = vertical/x_max, assuming only pos. int-indexing """
        self.horizontalSlider_leftBScanWindow.setMaximum(int(y_max))
        self.horizontalSlider_rightBScanWindow.setMaximum(int(x_max))
    
    def set_spinbox_max_values(self, x_max, y_max) :
        """ Sets the values of the select-boxes to OCT (x,y) volume dims
        left = horizontal/y_max, right = vertical/x_max, assuming only pos. int-indexing """
        self.spinBox_leftBScanWindow.setRange(1, int(y_max))
        self.spinBox_rightBScanWindow.setRange(1, int(x_max))
        
    def show_reconstructed_bScans(self) :
        pass

    def close_application_via_button(self) :
        self.pushButton_close.clicked.connect(QtCore.QCoreApplication.instance().quit)


def run() :
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiWindowDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    run()
