"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                        Copyright 2021 Medical University of Vienna 
                                        ******
                                         
        >>> main file for OCT Recon GUI creation, methods and handling     
                                
"""

# global imports
import os
import cv2
import sys
import time # debug
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt # debug
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend')))
# import backend module(s)
from recon_funcs import OctReconstructionManager


class UiWindowDialog(object) :
    def __init__(self, data_endianness = '>u2') -> None:
        super().__init__()
        self.data_endianness = data_endianness
         
    def setupUi(self, Dialog):
        # create dialog box / GUI-display-canvass
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
        # set validator to only allow interger inputs
        self.onlyInt = QtGui.QIntValidator()
        # check box endian-ness of loaded data
        self.checkBox_Endianness = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Endianness.setGeometry(QtCore.QRect(1790, 845, 100, 30))
        self.checkBox_Endianness.setText("")
        self.checkBox_Endianness.setObjectName("checkBox_Endianness")
        self.checkBox_Endianness.setChecked(True)
        self.checkBox_Endianness.stateChanged.connect(self.set_data_endianness)
        # left-hand-side/vertical B-scan display canvas/widget
        self.Left_BScanWindow = QtWidgets.QLabel(Dialog)
        self.Left_BScanWindow.setGeometry(QtCore.QRect(30, 30, 920, 540))
        self.Left_BScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Left_BScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Left_BScanWindow.setText("")
        self.Left_BScanWindow.setObjectName("Left_BScanWindow")
        # label for left-hand-side/vertical B-scan display canvas/widget
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_leftBscanDisplayCanvas_ = QtWidgets.QLabel(Dialog)
        self.label_leftBscanDisplayCanvas_.setGeometry(QtCore.QRect(300, 10, 350, 20))
        self.label_leftBscanDisplayCanvas_.setFont(font)
        self.label_leftBscanDisplayCanvas_.setObjectName("label_leftBscanDisplayCanvas_")
        # right-hand-side/horizontal B-scan display canvas/widget
        self.Right_BScanWindow = QtWidgets.QLabel(Dialog)
        self.Right_BScanWindow.setGeometry(QtCore.QRect(970, 30, 920, 540))
        self.Right_BScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Right_BScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Right_BScanWindow.setText("")
        self.Right_BScanWindow.setObjectName("Right_BScanWindow")
        # label for right-hand-side/horizontal B-scan display canvas/widget
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_rightBscanDisplayCanvas_= QtWidgets.QLabel(Dialog)
        self.label_rightBscanDisplayCanvas_.setGeometry(QtCore.QRect(1260, 10, 370, 20))
        self.label_rightBscanDisplayCanvas_.setFont(font)
        self.label_rightBscanDisplayCanvas_.setObjectName("label_rightBscanDisplayCanvas_")
        # display widget for click button options
        self.DisplayOptionsWindow = QtWidgets.QLabel(Dialog)
        self.DisplayOptionsWindow.setGeometry(QtCore.QRect(30, 600, 650, 450))
        self.DisplayOptionsWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DisplayOptionsWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DisplayOptionsWindow.setText("")
        self.DisplayOptionsWindow.setObjectName("DisplayOptionsWindow")
        # label for display options window 
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisplayOptionsWindow_ = QtWidgets.QLabel(Dialog)
        self.label_DisplayOptionsWindow_.setFont(font)
        self.label_DisplayOptionsWindow_.setGeometry(QtCore.QRect(250, 580, 300, 20))
        self.label_DisplayOptionsWindow_.setObjectName("label_DisplayOptionsWindow_")
        # display widget for square enface image of loaded OCT volume
        self.EnfaceDisplayWindow = QtWidgets.QLabel(Dialog)
        self.EnfaceDisplayWindow.setGeometry(QtCore.QRect(700, 650, 400, 400))
        self.EnfaceDisplayWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.EnfaceDisplayWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.EnfaceDisplayWindow.setText("")
        self.EnfaceDisplayWindow.setObjectName("EnfaceDisplayWindow")
        # LEFT = VERTICAL B-scan selection spin box
        self.spinBox_leftBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_leftBScanWindow.setGeometry(QtCore.QRect(890, 600, 60, 30))
        self.spinBox_leftBScanWindow.setObjectName("spinBox_leftBScanWindow")
        # RIGHT = HORIZONTAL B-scan selection spin box
        self.spinBox_rightBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_rightBScanWindow.setGeometry(QtCore.QRect(970, 600, 60, 30))
        self.spinBox_rightBScanWindow.setObjectName("spinBox_rightBScanWindow")
        
        # close/end application push button
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setGeometry(QtCore.QRect(1790, 1010, 100, 35))
        font = QtGui.QFont()
        font.setFamily("Neue Haas Grotesk Text Pro")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(50)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setDefault(True)
        self.pushButton_close.setObjectName("pushButton_close")
        # button for loading OCT data - with customized font
        self.pushButton_loadOctData = QtWidgets.QPushButton(Dialog)
        self.pushButton_loadOctData.setGeometry(QtCore.QRect(1790, 880, 100, 120))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_loadOctData.setFont(font)
        self.pushButton_loadOctData.setDefault(True)
        self.pushButton_loadOctData.setFlat(False)
        self.pushButton_loadOctData.setObjectName("pushButton_loadOctData")
        # button to run the reconstruction (partially obsolete)
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
        # enface display push button
        font = QtGui.QFont()
        font.setFamily("Neue Haas Grotesk Text Pro")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_showEnFace = QtWidgets.QPushButton(Dialog)
        self.pushButton_showEnFace.setGeometry(QtCore.QRect(1120, 830, 230, 40))
        self.pushButton_showEnFace.setFont(font)
        self.pushButton_showEnFace.setObjectName("pushButton_showEnFace")
        # A-scan display push button
        self.pushButton_displayAScanAtIntersection = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayAScanAtIntersection.setGeometry(QtCore.QRect(1120, 890, 230, 40))
        self.pushButton_displayAScanAtIntersection.setFont(font)
        self.pushButton_displayAScanAtIntersection.setObjectName("pushButton_displayAScanAtIntersection")
        # polynomial function for dispersion correction display  
        self.pushButton_displayDispersionCurves = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayDispersionCurves.setGeometry(QtCore.QRect(1120, 950, 230, 40))
        self.pushButton_displayDispersionCurves.setFont(font)
        self.pushButton_displayDispersionCurves.setObjectName("pushButton_displayDispersionCurves")
        # convolutional/windowing functions plot/display 
        self.pushButton_displayWindowingFunctions = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayWindowingFunctions.setGeometry(QtCore.QRect(1120, 1010, 230, 40))
        self.pushButton_displayWindowingFunctions.setFont(font)
        self.pushButton_displayWindowingFunctions.setObjectName("pushButton_displayWindowingFunctions")
       
        # left-hand-side widget/vertical B-scan display button  
        self.horizontalSlider_leftBScanWindow = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_leftBScanWindow.setGeometry(QtCore.QRect(700, 600, 160, 30))
        self.horizontalSlider_leftBScanWindow.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_leftBScanWindow.setObjectName("horizontalSlider_leftBScanWindow")
        # right-hand-side side widget/horizontal B-scan display button
        self.horizontalSlider_rightBScanWindow = QtWidgets.QSlider(Dialog)
        self.horizontalSlider_rightBScanWindow.setGeometry(QtCore.QRect(1050, 600, 160, 30))
        self.horizontalSlider_rightBScanWindow.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_rightBScanWindow.setObjectName("horizontalSlider_rightBScanWindow")
        
        # spin box to set n-samples from zero-delay (DC-removal) for cropping of DC
        self.spinBox_CropDcSamples = QtWidgets.QSpinBox(Dialog)
        self.spinBox_CropDcSamples.setGeometry(QtCore.QRect(1825, 755, 45, 25))
        self.samples_crop_dc = 25 
        self.samples_crop_hf = 0
        self.spinBox_CropDcSamples.setValue(self.samples_crop_dc)   
        # label to crop n-samples from zero-delay (DC-removal)
        self.label_CropDcSamples_ = QtWidgets.QLabel(Dialog)
        self.label_CropDcSamples_.setGeometry(QtCore.QRect(1630, 755, 170, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_CropDcSamples_.setFont(font)
        self.label_CropDcSamples_.setEnabled(True)
        self.label_CropDcSamples_.setObjectName("label_CropDcSamples")
        
        # spin box to set n-samples from bottom of A-scan
        self.spinBox_CropHfSamples = QtWidgets.QSpinBox(Dialog)
        self.spinBox_CropHfSamples.setGeometry(QtCore.QRect(1825, 785, 45, 25))
        self.samples_crop_hf = 20
        self.spinBox_CropHfSamples.setValue(self.samples_crop_hf)  
        # label to set n-samples from bottom of A-scan
        self.label_CropHfSamples_ = QtWidgets.QLabel(Dialog)
        self.label_CropHfSamples_.setGeometry(QtCore.QRect(1630, 785, 150, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_CropHfSamples_.setFont(font)
        self.label_CropHfSamples_.setEnabled(True)
        self.label_CropHfSamples_.setObjectName("label_CropHfSamples")
        
        # spin box to set value for scaling the intensity of reconstructed scans
        self.spinBox_DisplayScale = QtWidgets.QSpinBox(Dialog)
        self.spinBox_DisplayScale.setGeometry(QtCore.QRect(1555, 755, 45, 25))
        self.value_scaled_display = 64
        self.spinBox_DisplayScale.setValue(self.value_scaled_display)  
        # label of value for scaling reconstructed display level
        self.label_DisplayScale_ = QtWidgets.QLabel(Dialog)
        self.label_DisplayScale_.setGeometry(QtCore.QRect(1370, 755, 150, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisplayScale_.setFont(font)
        self.label_DisplayScale_.setEnabled(True)
        self.label_DisplayScale_.setObjectName("label_DisplayScale")
        
        # spin box to set value for black level in reconstruction
        self.spinBox_BlackLevel = QtWidgets.QSpinBox(Dialog)
        self.spinBox_BlackLevel.setGeometry(QtCore.QRect(1555, 785, 45, 25))
        self.value_black_level = 77
        self.spinBox_BlackLevel.setValue(self.value_black_level)  
        # label of value for black level in reconstruction
        self.label_BlackLevel_ = QtWidgets.QLabel(Dialog)
        self.label_BlackLevel_.setGeometry(QtCore.QRect(1370, 785, 150, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.label_BlackLevel_.setFont(font)
        self.label_BlackLevel_.setEnabled(True)
        self.label_BlackLevel_.setObjectName("label_BlackLevel")
        
        # label for the perform reconstruction for current pair of B-scans button
        self.label_DisperisonCoefficients_ = QtWidgets.QLabel(Dialog)
        self.label_DisperisonCoefficients_.setGeometry(QtCore.QRect(1630, 640, 245, 30))
        # label for current setting of dispersion coefficients
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisperisonCoefficients_.setFont(font)
        self.label_DisperisonCoefficients_.setObjectName("label_DisperisonCoefficients_")
        # grid layout of dispersion correction polynomial coefficients 
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1630, 670, 240, 60))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        ### spin boxes and labels for dispersion coefficients ###
        self.spinBox_DispCoeffC2 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC2.setObjectName("spinBox_DispCoeffC2")
        self.spinBox_DispCoeffC2.setRange(-150, 150)
        self.gridLayout.addWidget(self.spinBox_DispCoeffC2, 1, 1, 1, 1)
        self.label_DispCoeffC2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_DispCoeffC2.setFont(font)
        self.label_DispCoeffC2.setObjectName("label_DispCoeffC2")
        self.gridLayout.addWidget(self.label_DispCoeffC2, 0, 1, 1, 1)
        self.spinBox_DispCoeffC1 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC1.setObjectName("spinBox_DispCoeffC1")
        self.spinBox_DispCoeffC1.setRange(-150, 150)
        self.gridLayout.addWidget(self.spinBox_DispCoeffC1, 1, 2, 1, 1)
        self.spinBox_DispCoeffC3 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC3.setObjectName("spinBox_DispCoeffC3")
        self.spinBox_DispCoeffC3.setRange(-150, 150)
        self.gridLayout.addWidget(self.spinBox_DispCoeffC3, 1, 0, 1, 1)
        self.spinBox_DispCoeffC0 = QtWidgets.QSpinBox(self.gridLayoutWidget)
        self.spinBox_DispCoeffC0.setObjectName("spinBox_DispCoeffC0")
        self.spinBox_DispCoeffC0.setRange(-150, 150)
        self.gridLayout.addWidget(self.spinBox_DispCoeffC0, 1, 3, 1, 1)
        self.label_DispCoeffC3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_DispCoeffC3.setEnabled(True)
        self.label_DispCoeffC3.setFont(font)
        self.label_DispCoeffC3.setObjectName("label_DispCoeffC3")
        self.gridLayout.addWidget(self.label_DispCoeffC3, 0, 0, 1, 1)
        self.label_DispCoeffC1 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_DispCoeffC1.setFont(font)
        self.label_DispCoeffC1.setObjectName("label_DispCoeffC1")
        self.gridLayout.addWidget(self.label_DispCoeffC1, 0, 2, 1, 1)
        self.label_DispCoeffC0 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_DispCoeffC0.setFont(font)
        self.label_DispCoeffC0.setObjectName("label_DispCoeffC0")
        self.gridLayout.addWidget(self.label_DispCoeffC0, 0, 3, 1, 1)
        # display box for console print displays
        self.label_ConsoleLog = QtWidgets.QLabel(Dialog)
        self.label_ConsoleLog.setGeometry(QtCore.QRect(1370, 820, 400, 230))
        self.label_ConsoleLog.setFrameShape(QtWidgets.QFrame.Box)
        self.label_ConsoleLog.setMidLineWidth(1)
        self.label_ConsoleLog.setObjectName("label_ConsoleLog")
        # label for box with display options
        self.label_DisplayOptions_ = QtWidgets.QLabel(Dialog)
        self.label_DisplayOptions_.setGeometry(QtCore.QRect(1150, 780, 170, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DisplayOptions_.setFont(font)
        self.label_DisplayOptions_.setObjectName("label_DisplayOptions_")
        # drop-down menu for selection of different windowing-functions
        self.comboBox_windowingOptions = QtWidgets.QComboBox(Dialog)
        self.comboBox_windowingOptions.setGeometry(QtCore.QRect(1370, 680, 230, 30))
        self.comboBox_windowingOptions.setObjectName("comboBox_windowingOptions")
        # NOTE: all box items contain data in form a list of a string (wind-key) and a int (value filter-sigma)
        self.comboBox_windowingOptions.addItem("Von-Hann window (default)", ["Hann", 1])
        self.comboBox_windowingOptions.addItem("Hamming window", ["Hamm", 1])
        self.comboBox_windowingOptions.addItem("Kaiser-Bessel window", ["Kaiser", 0])
        self.comboBox_windowingOptions.addItem("Gaussian (narrow) window", ["Gauss", 111]) #TODO: check values for sigma
        self.comboBox_windowingOptions.addItem("Gaussian (medium) window", ["Gauss", 211])
        self.comboBox_windowingOptions.addItem("Gaussian (wide) window", ["Gauss", 311])
        # holds the string for the windowing function -> set default
        self.curr_wind_key = self.comboBox_windowingOptions.currentData()  
        # label/head line for windowing function selection field
        self.label_WindowingFunction_ = QtWidgets.QLabel(Dialog)
        self.label_WindowingFunction_.setGeometry(QtCore.QRect(1370, 640, 215, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_WindowingFunction_.setFont(font)
        self.label_WindowingFunction_.setObjectName("label_WindowingFunction_")
        self.flag_loaded_oct_data = False
        self.flag_calculate_enface = False
        self.disp_coeffs_tuple = (0,0,0,0)

        # set all style elements in UI
        self.retranslateUi(Dialog)
        
        ####################################################
        # ***** FROM BACKEND / SIGNALS AND CONNECTIONS *****
        ####################################################
        self.REC = OctReconstructionManager(self.data_endianness)
    
        # START PROCESING: load OCT data
        self.pushButton_loadOctData.clicked.connect(self._load_oct_data)
        
        # exit if close button is pressed
        self.close_application_via_button()      
   
        # run reconstruction for display of current pair of cross-sectional A-scans
        self.pushButton_runReconstruction.clicked.connect(self.run_recon_for_current_settings)
        
        # run calculation of enface image and display
        # self.pushButton_showEnFace.clicked.connect(self.display_enface_image) # implement efficient enface-calculation algo
        self.pushButton_showEnFace.clicked.connect(self.create_enface_display_widget) 
        
        # display current windowing function
        self.pushButton_displayWindowingFunctions.clicked.connect(self.display_current_windowing_function)
        self.pushButton_displayDispersionCurves.clicked.connect(self.display_current_disp_curves)
        
        # display inference signal and reconstructed A-scan in display widgets
        self.pushButton_displayAScanAtIntersection.clicked.connect(self.display_aScans_at_intersection)
        
        # change the id-string for windowing function if values in comboBox are changes
        self.comboBox_windowingOptions.activated.connect(self.display_current_windowing_function)
        
        # if values in disp coeff boxes are change -> plot if curves is displayed and tuple with coeffs is updated
        self.spinBox_DispCoeffC0.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC0.valueChanged.connect(self.update_disp_coeff_tuple)
        # self.spinBox_DispCoeffC0.valueChanged.connect(self.run_recon_for_current_settings)
        self.spinBox_DispCoeffC1.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC1.valueChanged.connect(self.update_disp_coeff_tuple)
        # self.spinBox_DispCoeffC1.valueChanged.connect(self.run_recon_for_current_settings)
        self.spinBox_DispCoeffC2.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC2.valueChanged.connect(self.update_disp_coeff_tuple)
        # self.spinBox_DispCoeffC2.valueChanged.connect(self.run_recon_for_current_settings)
        self.spinBox_DispCoeffC3.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC3.valueChanged.connect(self.update_disp_coeff_tuple)
        # self.spinBox_DispCoeffC3.valueChanged.connect(self.run_recon_for_current_settings)
        
        # change of values for cropping and adjusting black level and scale for display
        self.spinBox_CropDcSamples.valueChanged.connect(self.update_dc_crop_samples)
        self.spinBox_CropHfSamples.valueChanged.connect(self.update_hf_crop_samples)
        self.spinBox_DisplayScale.valueChanged.connect(self.update_display_scale_value)
        self.spinBox_BlackLevel.valueChanged.connect(self.update_black_level_value)
                        
        # couple B-scan display selection elements & set update dependecy of lines
        self.horizontalSlider_leftBScanWindow.valueChanged['int'].connect(self.spinBox_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.horizontalSlider_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.create_enface_display_widget)
        self.horizontalSlider_rightBScanWindow.valueChanged['int'].connect(self.spinBox_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.horizontalSlider_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.create_enface_display_widget)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        """ add texts and dialog descriptions """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ODD-UI (Oct Data Display - User Interface)"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.checkBox_Endianness.setText(_translate("Dialog", "Data is (IEEE)\nBig Endian"))
        self.pushButton_loadOctData.setText(_translate("Dialog", "Load\nOCT\nData"))
        self.pushButton_showEnFace.setText(_translate("Dialog", "Show en face OCT and update lines"))
        self.pushButton_displayAScanAtIntersection.setText(_translate("Dialog", "Display A-scan at Intersection"))
        self.pushButton_displayDispersionCurves.setText(_translate("Dialog", "Plot Dispersion Curves"))
        self.pushButton_displayWindowingFunctions.setText(_translate("Dialog", "Plot Windowing Function"))
        self.pushButton_runReconstruction.setText(_translate("Dialog", "Reconstruct"))
        self.label_BlackLevel_.setText(_translate("Dialog", "Black Level Value"))
        self.label_DisplayScale_.setText(_translate("Dialog", "Display Scale Factor"))
        self.label_CropDcSamples_.setText(_translate("Dialog", "Crop LF/DC [samples]"))
        self.label_CropHfSamples_.setText(_translate("Dialog", "Crop HF [samples]"))
        self.label_DisperisonCoefficients_.setText(_translate("Dialog", "Dispersion Coefficients (real + compl.)"))
        self.label_leftBscanDisplayCanvas_.setText(_translate("Dialog", "Vertical B-scan Display Canvas (red)"))
        self.label_rightBscanDisplayCanvas_.setText(_translate("Dialog", "Horizontal B-scan Display Canvas (green)"))
        self.label_DispCoeffC2.setText(_translate("Dialog", "C2"))
        self.label_DispCoeffC3.setText(_translate("Dialog", "C3"))
        self.label_DispCoeffC1.setText(_translate("Dialog", "C1"))
        self.label_DispCoeffC0.setText(_translate("Dialog", "C0"))
        self.label_ConsoleLog.setText(_translate("Dialog", "Console prints"))
        self.label_DisplayOptions_.setText(_translate("Dialog", "Display Options"))
        self.label_DisplayOptionsWindow_.setText(_translate("Dialog","Display Options Window"))
        self.label_WindowingFunction_.setText(_translate("Dialog", "Windowing Function"))

            
    """     ****** SIGNALS ******
        Backend-connected functions     """
    def _load_oct_data(self) -> None :
        """ loads user-selected file containing OCT data and created class-vars raw data buffer and dimensions """
        print("Loading OCT data... ")
        buffer_oct_raw_data = self.REC.load_plex_oct_data().astype(np.uint16)
        print(f"Loaded selected data (shape={buffer_oct_raw_data.shape} and dtype={buffer_oct_raw_data.dtype}) into memory")
        self.buffer_oct_raw_data = buffer_oct_raw_data
        self.dims_buffer_oct_raw_data = buffer_oct_raw_data.shape
        self.flag_loaded_oct_data = True
        self.set_spinbox_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
        self.set_bScan_slider_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 

    def create_enface_display_widget(self) -> None :
        """ creates an enface image with overlayed lines indicating the current B-scans and/or updates the display """
        if not self._is_no_oct_data_loaded():
            return
        enface = self.calculate_enface()
        enface_img = QtGui.QImage(enface.data.tobytes(), 
                                  enface.shape[1], enface.shape[0], 
                                  QtGui.QImage.Format_Indexed8)
        # convert image file into pixmap
        self.pixmap_image = QtGui.QPixmap( enface_img )
        # create painter instance with pixmap
        self.painterInstance = QtGui.QPainter(self.pixmap_image)
        self.update_pos_Bscan_indicating_lines(self.spinBox_leftBScanWindow.value(),
                                               self.spinBox_rightBScanWindow.value())
        self.painterInstance.end() # painter instance has to be deleted after every update
        self.EnfaceDisplayWindow.setPixmap(self.pixmap_image)
        self.EnfaceDisplayWindow.setScaledContents(True)
    
        
    def display_aScans_at_intersection(self) :
        """ displays the raw (left top side canvas) and recostructed (right top side canvas) A-scan 
        at the selected B-scan intersection """
        if not self._is_no_oct_data_loaded():
            return
        # display raw A-scan at intersection in left-hand-side top canvas
        fig = Figure(figsize=(6, 3.6), dpi=300) # dimensions roughly taken from widget/canvas
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.set_title(f"Raw (unprocessed) A-scan at intersection")
        a_scan = self.buffer_oct_raw_data[:, self.spinBox_rightBScanWindow.value()-1, self.spinBox_leftBScanWindow.value()-1]
        ax.plot(a_scan)
        ax.axis('off')
        canvas.draw()
        buffer = canvas.buffer_rgba()
        buffer = np.asarray(buffer)
        disp_img = QtGui.QImage(buffer.data.tobytes(), 
                                buffer.shape[1], buffer.shape[0], 
                                QtGui.QImage.Format_ARGB32)
        self.Left_BScanWindow.setPixmap( QtGui.QPixmap(disp_img) )
        self.Left_BScanWindow.setScaledContents(True)
        # display reconstructed A-scan at intersection in right-hand-side top canvas
        fig = Figure(figsize=(6, 3.6), dpi=300)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.set_title(f"Reconstructed A-scan at intersection")
        a_scan = self.buffer_oct_raw_data[:, self.spinBox_rightBScanWindow.value()-1, self.spinBox_leftBScanWindow.value()-1]
        ax.plot(self.REC._run_reconstruction(a_scan, 
                                            disp_coeffs=self.disp_coeffs_tuple, 
                                            wind_key=self.curr_wind_key[0]))
        ax.axis('off')
        canvas.draw()
        buffer = canvas.buffer_rgba() # already a RGBA buffer - no conversion nec.
        buffer = np.asarray(buffer)
        disp_img = QtGui.QImage(buffer.data.tobytes(), 
                                buffer.shape[1], buffer.shape[0], 
                                QtGui.QImage.Format_ARGB32)
        self.Right_BScanWindow.setPixmap( QtGui.QPixmap(disp_img) )
        self.Right_BScanWindow.setScaledContents(True)
        
    def display_current_disp_curves(self) :
        """ plots graphs of real + compl. parts of disp. comp. curves in DisplayOptionsWindow-Widget """
        if not self._is_no_oct_data_loaded():
            return
        fig = Figure(figsize=(6, 3.6), dpi=300)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        disp = self.REC.create_comp_disp_vec(self.dims_buffer_oct_raw_data[0], self.disp_coeffs_tuple, 
                                             self.curr_wind_key[0], self.curr_wind_key[1])
        ax.set_title(f"Disperison ({self.curr_wind_key[0]}-windowed)")
        ax.plot(disp.real)
        ax.plot(disp.imag)
        ax.legend(["Real Part", "Complex Part"])
        canvas.draw()
        buffer = canvas.buffer_rgba() # already a RGBA buffer - no conversion nec.
        buffer = np.asarray(buffer)
        disp_img = QtGui.QImage(buffer.data.tobytes(), 
                                buffer.shape[1], buffer.shape[0], 
                                QtGui.QImage.Format_ARGB32)
        self.DisplayOptionsWindow.setPixmap( QtGui.QPixmap(disp_img) )
        self.DisplayOptionsWindow.setScaledContents(True) 
        
    def display_current_windowing_function(self) :
        """ plots graph of windowing curve in DisplayOptionsWindow-Widget """
        if not self._is_no_oct_data_loaded():
            return
        self.update_wind_fct_key() # so it doesn't have to get called as a second event signal
        fig = Figure(figsize=(6, 3.6), dpi=300)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        wind = self.REC.create_windowing_function(self.dims_buffer_oct_raw_data[0], self.curr_wind_key[0], self.curr_wind_key[1])
        ax.set_title(f"Windowing Function: {self.curr_wind_key[0]}")
        ax.plot(wind)
        canvas.draw()
        buffer = canvas.buffer_rgba() # already a RGBA buffer - no conversion nec.
        buffer = np.asarray(buffer)
        disp_img = QtGui.QImage(buffer.data.tobytes(), 
                                buffer.shape[1], buffer.shape[0], 
                                QtGui.QImage.Format_ARGB32)
        self.DisplayOptionsWindow.setPixmap( QtGui.QPixmap(disp_img) )
        self.DisplayOptionsWindow.setScaledContents(True) 

    def calculate_enface(self) :
        # TODO: rethink what params are needed
        if not self.flag_calculate_enface:
            print("Calculating Enface")
            self.enface = self.REC.calculate_enface_for_display(self.buffer_oct_raw_data)
            self.flag_calculate_enface = True
            print("Done!")
        return self.enface

    def run_recon_for_current_settings(self) :
        """ runs recosntruction from backend on cirrently selected pair of B-scans in volume """
        if not self._is_no_oct_data_loaded():
            return
        print("Reconstructing...")
        # create/update vertical/left scan (dims_buffer_oct_raw_data[1])
        curr_vert_raw = self.buffer_oct_raw_data[:,:,self.spinBox_leftBScanWindow.value()-1]
        curr_vert_recon = self.REC._run_reconstruction(curr_vert_raw, 
                                                       disp_coeffs=self.disp_coeffs_tuple, 
                                                       wind_key=self.curr_wind_key, 
                                                       samples_hf_crop=self.samples_crop_hf, 
                                                       samples_dc_crop=self.samples_crop_dc, 
                                                       scale_fac=self.value_scaled_display, 
                                                       blck_lvl=self.value_black_level,
                                                       is_bg_sub=False,
                                                       show_scaled_data=True)
        curr_vert_recon = cv2.cvtColor( curr_vert_recon, cv2.COLOR_BAYER_GR2GRAY )
        img_left_vert = QtGui.QImage(curr_vert_recon.data.tobytes(), 
                                     curr_vert_recon.shape[1], curr_vert_recon.shape[0], 
                                     QtGui.QImage.Format_Grayscale8)
        self.Left_BScanWindow.setPixmap( QtGui.QPixmap(img_left_vert) )
        self.Left_BScanWindow.setScaledContents(True) 
        # create/update horizontal/right scan (dims_buffer_oct_raw_data[2])
        curr_hori_raw = self.buffer_oct_raw_data[:,self.spinBox_rightBScanWindow.value()-1]
        curr_hori_recon = self.REC._run_reconstruction(curr_hori_raw, 
                                                       disp_coeffs=self.disp_coeffs_tuple, 
                                                       wind_key=self.curr_wind_key, 
                                                       samples_hf_crop=self.samples_crop_hf, 
                                                       samples_dc_crop=self.samples_crop_dc, 
                                                       scale_fac=self.value_scaled_display, 
                                                       blck_lvl=self.value_black_level,
                                                       is_bg_sub=False,
                                                       show_scaled_data=True)
        curr_hori_recon = cv2.cvtColor( curr_hori_recon, cv2.COLOR_BAYER_GR2GRAY )
        img_right_hori = QtGui.QImage(curr_hori_recon.data.tobytes(), 
                                      curr_hori_recon.shape[1], curr_hori_recon.shape[0], 
                                      QtGui.QImage.Format_Grayscale8)
        self.Right_BScanWindow.setPixmap( QtGui.QPixmap(img_right_hori) )
        self.Right_BScanWindow.setScaledContents(True) # 2 display reconstructed B-scan pain
        # update lines indicating the B-scan positions in the enface image 
        self.create_enface_display_widget()
    
    def set_data_endianness(self) -> None :
        """ sets the endianness of the raw OCT data and reloads OCT data if it is changed"""
        # TODO: fix import and reloading of data!!!
        if self.checkBox_Endianness.isChecked():
            self.data_endianness = '>u2'
        else :
            self.data_endianness = '<u2'
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Please reload data")
        msg_box.setText("[WARNING:] You're changed the expected endianness!\nPlease reload data!")
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        x = msg_box.exec_()
        self.DEC = OctReconstructionManager() # create new instance of Backend / Reconstruction Class
     
    def update_pos_Bscan_indicating_lines(self, curr_left_idx: int, curr_right_idx: int, 
                                          line_width: int=1) -> None :
        """ draws/updates the lines, via getting spinbox/slider values """
        # set line color and thickness
        self.v_bScan_line = QtGui.QPen(QtCore.Qt.red)
        self.v_bScan_line.setWidth(line_width)
        self.h_bScan_line = QtGui.QPen(QtCore.Qt.green)
        self.h_bScan_line.setWidth(line_width)
        # draw lines on canvas
        self.painterInstance.setPen(self.v_bScan_line)
        self.painterInstance.drawLine(curr_left_idx, 0, curr_left_idx, 400) 
        self.painterInstance.setPen(self.h_bScan_line)
        self.painterInstance.drawLine(0, curr_right_idx, 400, curr_right_idx)
        
    def update_black_level_value(self) -> None:
        """ set the value for the black level acc. to spin box value """
        if not self._is_no_oct_data_loaded():
            return
        self.value_black_level = self.spinBox_BlackLevel.value()
        # print(f"New black level value = {self.value_black_level}") # debug
        
    def update_display_scale_value(self) -> None:
        """ set the value for the black level acc. to spin box value """
        self.value_scaled_display = self.spinBox_DisplayScale.value()
        # print(f"New display scale value = {self.value_scaled_display}") # debug
        
    def update_dc_crop_samples(self) -> None :
        """ Update the low-frequency samples that should be cropped in the reconstructed B-scan """
        if not self._is_no_oct_data_loaded():
            return
        self.samples_crop_dc = self.spinBox_CropDcSamples.value()
        # print(f"Cropping {self.samples_crop_dc} low-frequency (DC) samples") # debug
        
    def update_hf_crop_samples(self) -> None :
        """ Update the high-frequency samples that should be cropped in the reconstructed B-scan """
        if not self._is_no_oct_data_loaded():
            return
        self.samples_crop_hf = self.spinBox_CropHfSamples.value()
        # print(f"Cropping {self.samples_crop_hf} high-frequency samples") # debug
          
    def update_wind_fct_key(self) -> None :
        """ updates the key (class var) with the windowing function for reconstruction """
        if not self._is_no_oct_data_loaded():
            return
        self.curr_wind_key = self.comboBox_windowingOptions.currentData()
        
    def update_disp_coeff_tuple(self) -> None :
        """ updates tuple (clas var) containing the dispersion correction polynominal coefficients 
        according to the current spin box combinations/settings"""
        if not self._is_no_oct_data_loaded():
            return
        self.disp_coeffs_tuple = (self.spinBox_DispCoeffC3.value(), self.spinBox_DispCoeffC2.value(),
                                  self.spinBox_DispCoeffC1.value(), self.spinBox_DispCoeffC0.value()) 
    
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
        
    def close_application_via_button(self) :
        """ closes GUI via the CLOSE button -> terminates application """
        self.pushButton_close.clicked.connect(QtCore.QCoreApplication.instance().quit)


def run() :
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiWindowDialog()
    ui.setupUi(Dialog)
    # Dialog.showMaximized() # comment in if screen resolution >= Full HD
    Dialog.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    run()
