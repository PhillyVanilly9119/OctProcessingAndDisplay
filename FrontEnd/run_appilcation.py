"""
                                        ******
        Author: @Philipp Matten - philipp.matten@meduniwien.ac.at / philipp.matten@gmx.de
                
                                    Copyright 2021 
                                        ******
                                         
        >>> main file for OCT Recon GUI creation, methods and handling     
                                
"""

# global imports
import os
import cv2
import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt # debug
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# custom imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Backend')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Config')))

# import backend module(s)
from octreconstructionmanager import OctReconstructionManager
# from guidesignparamatermanager import GuiConfigDataManager


class UiWindowDialog(object) :
    def __init__(self, data_endianness = '>u2') -> None:
        super().__init__()
        self.data_endianness = data_endianness
        # WORKS! TODO: rethink the place where the config parameters are supposed to be parsed
        # self.gui_layout_config = GuiConfigDataManager('config_gui_layout').load_json_file() # create a new config file
         
    def setupUi(self, Dialog):
        
        # create dialog box / GUI-display-canvass
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1030)
        Dialog.setStyleSheet("background: rgb(17, 29, 78);")
        # set validator to only allow interger inputs
        self.onlyInt = QtGui.QIntValidator()
        
        ######################################################################################
        # Check Boxes #
        ###############
        # check box endian-ness of loaded data
        self.checkBox_Endianness = QtWidgets.QCheckBox(Dialog)
        self.checkBox_Endianness.setGeometry(QtCore.QRect(1780, 760, 110, 50))
        font = QtGui.QFont()
        font.setFamily("Neue Haas Grotesk Text Pro")
        font.setPointSize(5)
        font.setWeight(75)
        self.checkBox_Endianness.setFont(font)
        self.checkBox_Endianness.setText("")
        self.checkBox_Endianness.setObjectName("checkBox_Endianness")
        self.checkBox_Endianness.setChecked(True)
        self.checkBox_Endianness.setStyleSheet("color: rgb(231, 243, 251)")
        self.checkBox_Endianness.stateChanged.connect(self.set_data_endianness)
        
        ######################################################################################
        # Push Buttons #
        ################
        # close/end application push button
        self.pushButton_close = QtWidgets.QPushButton(Dialog)
        self.pushButton_close.setGeometry(QtCore.QRect(1780, 980, 110, 35))
        font = QtGui.QFont()
        font.setFamily("Neue Haas Grotesk Text Pro")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(50)
        self.pushButton_close.setFont(font)
        self.pushButton_close.setDefault(True)
        self.pushButton_close.setObjectName("pushButton_close")
        self.pushButton_close.setStyleSheet("background: rgb(240, 167, 148);" 
                                            "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-radius: 5px;"
                                            "border-color: grey;"
                                            "padding: 2px;")
                                            
        # button for loading OCT data - with customized font
        self.pushButton_loadOctData = QtWidgets.QPushButton(Dialog)
        self.pushButton_loadOctData.setGeometry(QtCore.QRect(1780, 860, 110, 110))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_loadOctData.setFont(font)
        self.pushButton_loadOctData.setDefault(True)
        self.pushButton_loadOctData.setFlat(False)
        self.pushButton_loadOctData.setStyleSheet("background: rgb(95, 180, 229);"
                                                  "border-style: outset;"
                                                  "border-width: 2px;"
                                                  "border-radius: 5px;"
                                                  "border-color: grey;"
                                                  "padding: 2px;")
        self.pushButton_loadOctData.setObjectName("pushButton_loadOctData")
        # button to run the reconstruction (partially obsolete)
        self.pushButton_runReconstruction = QtWidgets.QPushButton(Dialog)
        self.pushButton_runReconstruction.setGeometry(QtCore.QRect(1350, 600, 180, 70))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_runReconstruction.setFont(font)
        self.pushButton_runReconstruction.setDefault(True)
        self.pushButton_runReconstruction.setFlat(False)
        self.pushButton_runReconstruction.setStyleSheet("background: rgb(132, 201, 188);"
                                                        "border-style: outset;"
                                                        "border-width: 2px;"
                                                        "border-radius: 5px;"
                                                        "border-color: rgb(47, 142, 145);"
                                                        "padding: 2px;")
        self.pushButton_runReconstruction.setObjectName("pushButton_runReconstruction")

        ## Push Buttons for Display Options
        # label for box with display options
        self._label_DisplayOptions = QtWidgets.QLabel(Dialog)
        self._label_DisplayOptions.setGeometry(QtCore.QRect(1350, 690, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self._label_DisplayOptions.setFont(font)
        self._label_DisplayOptions.setAlignment(QtCore.Qt.AlignCenter)
        self._label_DisplayOptions.setStyleSheet("color: rgb(17, 29, 78);"
                                                 "background: rgb(181, 220, 241);"
                                                 "border-style: outset;"
                                                 "border-width: 2px;"
                                                 "border-radius: 3px;"
                                                 "border-color: grey;"
                                                 "padding: 2px;")
        self._label_DisplayOptions.setObjectName("_label_DisplayOptions")
        # enface display push button
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_showEnFace = QtWidgets.QPushButton(Dialog)
        self.pushButton_showEnFace.setGeometry(QtCore.QRect(1350, 722, 180, 40))
        self.pushButton_showEnFace.setFont(font)
        self.pushButton_showEnFace.setFlat(False)
        self.pushButton_showEnFace.setStyleSheet("background : rgb(95, 180, 229);"
                                                "border-style: outset;"
                                                "border-width: 2px;"
                                                "border-radius: 7px;"
                                                "border-color: grey;"
                                                "padding: 2px;")
        self.pushButton_showEnFace.setObjectName("pushButton_showEnFace")
        # A-scan display push button
        self.pushButton_displayAScanAtIntersection = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayAScanAtIntersection.setGeometry(QtCore.QRect(1350, 772, 180, 40))
        self.pushButton_displayAScanAtIntersection.setFont(font)
        self.pushButton_displayAScanAtIntersection.setFlat(False)
        self.pushButton_displayAScanAtIntersection.setStyleSheet("background : rgb(151, 207, 236);"
                                                                 "border-style: outset;"
                                                                 "border-width: 2px;"
                                                                 "border-radius: 7px;"
                                                                 "border-color: grey;"
                                                                 "padding: 2px;")
        self.pushButton_displayAScanAtIntersection.setObjectName("pushButton_displayAScanAtIntersection")
        # polynomial function for dispersion correction display  
        self.pushButton_displayDispersionCurves = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayDispersionCurves.setGeometry(QtCore.QRect(1350, 822, 180, 40))
        self.pushButton_displayDispersionCurves.setFont(font)
        self.pushButton_displayDispersionCurves.setFlat(False)
        self.pushButton_displayDispersionCurves.setStyleSheet("background : rgb(181, 220, 241);"
                                                                 "border-style: outset;"
                                                                 "border-width: 2px;"
                                                                 "border-radius: 7px;"
                                                                 "border-color: grey;"
                                                                 "padding: 2px;")
        self.pushButton_displayDispersionCurves.setObjectName("pushButton_displayDispersionCurves")
        # convolutional/windowing functions plot/display 
        self.pushButton_displayWindowingFunctions = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayWindowingFunctions.setGeometry(QtCore.QRect(1350, 872, 180, 40))
        self.pushButton_displayWindowingFunctions.setFont(font)
        self.pushButton_displayWindowingFunctions.setFlat(False)
        self.pushButton_displayWindowingFunctions.setStyleSheet("background : rgb(207, 232, 246);"
                                                                 "border-style: outset;"
                                                                 "border-width: 2px;"
                                                                 "border-radius: 7px;"
                                                                 "border-color: grey;"
                                                                 "padding: 2px;")
        self.pushButton_displayWindowingFunctions.setObjectName("pushButton_displayWindowingFunctions")
        
        ######################################################################################
        # Display Widgets #
        ###################
        
        # LEFT-HAND-SIDE / VERTICAL B-scan Display
        # display canvas/widget
        self.Left_BScanWindow = QtWidgets.QLabel(Dialog)
        self.Left_BScanWindow.setGeometry(QtCore.QRect(20, 30, 925, 550))
        self.Left_BScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Left_BScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Left_BScanWindow.setText("")
        self.Left_BScanWindow.setStyleSheet("background: rgb(181, 220, 241)")
        self.Left_BScanWindow.setObjectName("Left_BScanWindow")
        # label left B-scan display canvas/widget
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self._label_leftBscanDisplayCanvas = QtWidgets.QLabel(Dialog)
        self._label_leftBscanDisplayCanvas.setGeometry(QtCore.QRect(10, 10, 920, 20))
        self._label_leftBscanDisplayCanvas.setAlignment(QtCore.Qt.AlignCenter)
        self._label_leftBscanDisplayCanvas.setFont(font)
        self._label_leftBscanDisplayCanvas.setStyleSheet("color: rgb(231, 243, 251)")
        self._label_leftBscanDisplayCanvas.setObjectName("_label_leftBscanDisplayCanvas")
        # LEFT = VERTICAL B-scan selection spin box
        self.spinBox_leftBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_leftBScanWindow.setGeometry(QtCore.QRect(930, 960, 60, 30))
        self.spinBox_leftBScanWindow.setStyleSheet("color: rgb(231, 243, 251);"
                                                   "border-style: outset;"
                                                   "border-width: 2px;"
                                                    "border-radius: 3px;"
                                                    "border-color: grey;"
                                                    "padding: 2px;")
        self.spinBox_leftBScanWindow.setObjectName("spinBox_leftBScanWindow")
        # left-hand-side widget/vertical B-scan display button  
        self.slideBar_leftBScanWindow = QtWidgets.QSlider(Dialog)
        self.slideBar_leftBScanWindow.setGeometry(QtCore.QRect(640, 960, 270, 30))
        self.slideBar_leftBScanWindow.setOrientation(QtCore.Qt.Horizontal)
        self.slideBar_leftBScanWindow.setObjectName("slideBar_leftBScanWindow")
        
        # RIGHT-HAND-SIDE / HORIZONTAL B-scan display
        # display canvas/widget
        self.Right_BScanWindow = QtWidgets.QLabel(Dialog)
        self.Right_BScanWindow.setGeometry(QtCore.QRect(965, 30, 925, 550))
        self.Right_BScanWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Right_BScanWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Right_BScanWindow.setText("")
        self.Right_BScanWindow.setStyleSheet("background: rgb(181, 220, 241)")
        self.Right_BScanWindow.setObjectName("Right_BScanWindow")
        # label B-scan right display canvas/widget
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self._label_rightBscanDisplayCanvas= QtWidgets.QLabel(Dialog)
        self._label_rightBscanDisplayCanvas.setGeometry(QtCore.QRect(1260, 10, 370, 20))
        self._label_rightBscanDisplayCanvas.setFont(font)
        self._label_rightBscanDisplayCanvas.setStyleSheet("color: rgb(231, 243, 251)")
        self._label_rightBscanDisplayCanvas.setObjectName("_label_rightBscanDisplayCanvas")
        # RIGHT = HORIZONTAL B-scan selection spin box
        self.spinBox_rightBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_rightBScanWindow.setGeometry(QtCore.QRect(1000, 920, 60, 30))
        self.spinBox_rightBScanWindow.setStyleSheet("color: rgb(231, 243, 251);"
                                                    "border-style: outset;"
                                                    "border-width: 2px;"
                                                    "border-radius: 3px;"
                                                    "border-color: grey;"
                                                    "padding: 2px;")
        self.spinBox_rightBScanWindow.setObjectName("spinBox_rightBScanWindow")
        # right-hand-side side widget/horizontal B-scan display button
        self.slideBar_rightBScanWindow = QtWidgets.QSlider(Dialog)
        self.slideBar_rightBScanWindow.setGeometry(QtCore.QRect(1015, 600, 30, 300))
        self.slideBar_rightBScanWindow.setOrientation(QtCore.Qt.Vertical)
        self.slideBar_rightBScanWindow.setObjectName("slideBar_rightBScanWindow")
        
        # Widget for BUTTON OPTIONS display
        self.DisplayOptionsWindow = QtWidgets.QLabel(Dialog)
        self.DisplayOptionsWindow.setGeometry(QtCore.QRect(20, 600, 600, 400))
        self.DisplayOptionsWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DisplayOptionsWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DisplayOptionsWindow.setStyleSheet("background: rgb(181, 220, 241)")
        self.DisplayOptionsWindow.setText("")
        self.DisplayOptionsWindow.setObjectName("DisplayOptionsWindow")
        
        # Square Enface Display Options
        # display widget for square enface image of loaded OCT volume
        self.EnfaceDisplayWindow = QtWidgets.QLabel(Dialog)
        self.EnfaceDisplayWindow.setGeometry(QtCore.QRect(640, 600, 350, 350))
        self.EnfaceDisplayWindow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.EnfaceDisplayWindow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.EnfaceDisplayWindow.setStyleSheet("background: rgb(181, 220, 241);")
        self.EnfaceDisplayWindow.setText("")
        self.EnfaceDisplayWindow.setObjectName("EnfaceDisplayWindow")
        
        ######################################################################################
        # OCT volume dimension display grid layout #
        ############################################        
        # define grid
        self.gridLayoutWidget_OctVolumeDims = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_OctVolumeDims.setEnabled(True)
        self.gridLayoutWidget_OctVolumeDims.setGeometry(QtCore.QRect(1550, 690, 340, 60))
        self.gridLayoutWidget_OctVolumeDims.setStyleSheet("background: rgb(207, 232, 246);"
                                                          "color: rgb(17, 29, 78)")
        self.gridLayoutWidget_OctVolumeDims.setObjectName("gridLayoutWidget_OctVolumeDims")
        self.gridLayout_OctVolumeDims = QtWidgets.QGridLayout(self.gridLayoutWidget_OctVolumeDims)
        self.gridLayout_OctVolumeDims.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_OctVolumeDims.setHorizontalSpacing(3)
        self.gridLayout_OctVolumeDims.setVerticalSpacing(2)
        self.gridLayout_OctVolumeDims.setObjectName("gridLayout_OctVolumeDims")
        
        # spinbox for A-scan length display
        self.spinBox_aScanLength = QtWidgets.QSpinBox(self.gridLayoutWidget_OctVolumeDims)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.spinBox_aScanLength.setEnabled(False)
        self.spinBox_aScanLength.setRange(0, 4096)
        self.spinBox_aScanLength.setObjectName("_spinBox_aScanLength")
        self.spinBox_aScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                               "background: rgb(181, 220, 241 )")
        self.gridLayout_OctVolumeDims.addWidget(self.spinBox_aScanLength, 2, 1, 1, 1)
        # label A-scan length display
        self._label_aScanLength = QtWidgets.QLabel(self.gridLayoutWidget_OctVolumeDims)
        self._label_aScanLength.setFont(font)
        self._label_aScanLength.setAlignment(QtCore.Qt.AlignCenter)
        self._label_aScanLength.setObjectName("_label_aScanLength")
        self._label_aScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self.gridLayout_OctVolumeDims.addWidget(self._label_aScanLength, 1, 1, 1, 1)
        
        # spinbox for b-scan length display
        self.spinBox_bScanLength = QtWidgets.QSpinBox(self.gridLayoutWidget_OctVolumeDims)
        self.spinBox_bScanLength.setEnabled(False)
        self.spinBox_bScanLength.setRange(0, 4096)
        self.spinBox_bScanLength.setObjectName("_spinBox_bScanLength")
        self.spinBox_bScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                               "background: rgb(181, 220, 241 )")
        self.gridLayout_OctVolumeDims.addWidget(self.spinBox_bScanLength, 2, 2, 1, 1)
        # label B-scan length display
        self._label_bScanLength = QtWidgets.QLabel(self.gridLayoutWidget_OctVolumeDims)
        self._label_bScanLength.setFont(font)
        self._label_bScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self._label_bScanLength.setAlignment(QtCore.Qt.AlignCenter)
        self._label_bScanLength.setObjectName("_label_bScanLength")
        self.gridLayout_OctVolumeDims.addWidget(self._label_bScanLength, 1, 2, 1, 1)
        
        # spinbox for c-scan length display
        self.spinBox_cScanLength = QtWidgets.QSpinBox(self.gridLayoutWidget_OctVolumeDims)
        self.spinBox_cScanLength.setEnabled(False)
        self.spinBox_cScanLength.setRange(0, 4096)
        self.spinBox_bScanLength.setObjectName("_spinBox_cScanLength")
        self.spinBox_cScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                               "background: rgb(181, 220, 241);")
        self.gridLayout_OctVolumeDims.addWidget(self.spinBox_cScanLength, 2, 3, 1, 1)
        # label C-scan length display
        self._label_cScanLength = QtWidgets.QLabel(self.gridLayoutWidget_OctVolumeDims)
        self._label_cScanLength.setFont(font)
        self._label_cScanLength.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self._label_cScanLength.setAlignment(QtCore.Qt.AlignCenter)
        self._label_cScanLength.setObjectName("_label_cScanLength")
        self.gridLayout_OctVolumeDims.addWidget(self._label_cScanLength, 1, 3, 1, 1) 
        
        ######################################################################################
        # Dispersion coefficient grid layout #
        ######################################
        # grid layout
        self.gridLayoutWidget_dispCoeffs = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget_dispCoeffs.setEnabled(True)
        self.gridLayoutWidget_dispCoeffs.setGeometry(QtCore.QRect(1550, 620, 340, 60))
        self.gridLayoutWidget_dispCoeffs.setObjectName("gridLayoutWidget_dispCoeffs")
        self.gridLayoutWidget_dispCoeffs.setStyleSheet("background: rgb(207, 232, 246);"
                                                       "color: rgb(17, 29, 78)")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_dispCoeffs)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setObjectName("gridLayout_dispCoeffs")
        # label disp coeffs grid layout
        self._label_DisperisonCoefficients = QtWidgets.QLabel(Dialog)
        self._label_DisperisonCoefficients.setAlignment(QtCore.Qt.AlignCenter)
        self._label_DisperisonCoefficients.setGeometry(QtCore.QRect(1550, 600, 340, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self._label_DisperisonCoefficients.setFont(font)
        self._label_DisperisonCoefficients.setStyleSheet("color: rgb(17, 29, 78);"
                                                         "background: rgb(95, 180, 229);"
                                                         "border-style: outset;"
                                                         "border-width: 2px;"
                                                         "border-radius: 3px;"
                                                         "border-color: grey;"
                                                         "padding: 2px;")
        self._label_DisperisonCoefficients.setObjectName("_label_DisperisonCoefficients")
        
        ## c_0
        # spinbox c0 coeff
        self.spinBox_DispCoeffC0 = QtWidgets.QSpinBox(self.gridLayoutWidget_dispCoeffs)
        self.spinBox_DispCoeffC0.setEnabled(True)
        self.spinBox_DispCoeffC0.setRange(-256, 256)
        self.spinBox_DispCoeffC0.setObjectName("spinBox_DispCoeffC0")
        self.spinBox_DispCoeffC0.setStyleSheet("background: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC0, 2, 3, 1, 1)
        # label c0 coeff
        self._label_DispCoeffC0 = QtWidgets.QLabel(self.gridLayoutWidget_dispCoeffs)
        self._label_DispCoeffC0.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self._label_DispCoeffC0.setFont(font)
        self._label_DispCoeffC0.setToolTipDuration(4)
        self._label_DispCoeffC0.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self._label_DispCoeffC0.setAutoFillBackground(False)
        self._label_DispCoeffC0.setObjectName("_label_DispCoeffC0")
        self.gridLayout.addWidget(self._label_DispCoeffC0, 1, 3, 1, 1, QtCore.Qt.AlignHCenter)
        
        ## c_1
        # spinbox c1 coeff
        self.spinBox_DispCoeffC1 = QtWidgets.QSpinBox(self.gridLayoutWidget_dispCoeffs)
        self.spinBox_DispCoeffC1.setStyleSheet("color: rgb(231, 243, 251)")
        self.spinBox_DispCoeffC1.setEnabled(True)
        self.spinBox_DispCoeffC1.setRange(-256, 256)
        self.spinBox_DispCoeffC1.setStyleSheet("background: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self.spinBox_DispCoeffC1.setObjectName("spinBox_DispCoeffC1")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC1, 2, 2, 1, 1)
        # label c1 coeff
        self._label_DispCoeffC1 = QtWidgets.QLabel(self.gridLayoutWidget_dispCoeffs)
        self._label_DispCoeffC1.setEnabled(True)
        self._label_DispCoeffC1.setFont(font)
        self._label_DispCoeffC1.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self._label_DispCoeffC1.setObjectName("_label_DispCoeffC1")
        self.gridLayout.addWidget(self._label_DispCoeffC1, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        
        ## c_2
        # spinbox c2 coeff
        self.spinBox_DispCoeffC2 = QtWidgets.QSpinBox(self.gridLayoutWidget_dispCoeffs)
        self.spinBox_DispCoeffC2.setObjectName("spinBox_DispCoeffC2")
        self.spinBox_DispCoeffC2.setRange(-256, 256)
        self.spinBox_DispCoeffC2.setStyleSheet("background: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC2, 2, 1, 1, 1)
        # label c2 coeff
        self._label_DispCoeffC2 = QtWidgets.QLabel(self.gridLayoutWidget_dispCoeffs)
        self._label_DispCoeffC2.setFont(font)
        self._label_DispCoeffC2.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                              "border-width: 2px;"
                                              "border-radius: 3px;"
                                              "border-color: grey;"
                                              "padding: 2px;")
        self._label_DispCoeffC2.setObjectName("_label_DispCoeffC2")
        self.gridLayout.addWidget(self._label_DispCoeffC2, 1, 1, 1, 1, QtCore.Qt.AlignHCenter)
        
        ## c_3
        # spinbox c2 coeff
        self.spinBox_DispCoeffC3 = QtWidgets.QSpinBox(self.gridLayoutWidget_dispCoeffs)
        self.spinBox_DispCoeffC3.setObjectName("spinBox_DispCoeffC3")
        self.spinBox_DispCoeffC3.setRange(-256, 256)
        self.spinBox_DispCoeffC3.setStyleSheet("background: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self.gridLayout.addWidget(self.spinBox_DispCoeffC3, 2, 0, 1, 1)
        # label c3 coeff
        self._label_DispCoeffC3 = QtWidgets.QLabel(self.gridLayoutWidget_dispCoeffs)
        self._label_DispCoeffC3.setEnabled(True)
        self._label_DispCoeffC3.setFont(font)
        self._label_DispCoeffC3.setStyleSheet("color: rgb(17, 29, 78);"
                                              "border-style: outset;"
                                            "border-width: 2px;"
                                            "border-radius: 3px;"
                                            "border-color: grey;"
                                            "padding: 2px;")
        self._label_DispCoeffC3.setObjectName("_label_DispCoeffC3")
        self.gridLayout.addWidget(self._label_DispCoeffC3, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        
        #######################################################################################
        # Reconstruction Option Spin Boxes #
        ####################################  
        ## Scaling - intensity of reconstructed scans
        # spin box disp scale
        self.spinBox_DisplayScale = QtWidgets.QSpinBox(Dialog)
        self.spinBox_DisplayScale.setGeometry(QtCore.QRect(1500, 935, 50, 30))
        self.value_scaled_display = 64
        self.spinBox_DisplayScale.setValue(self.value_scaled_display)  
        self.spinBox_DisplayScale.setStyleSheet("color: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        # label of value for scaling reconstructed display level
        self._label_DisplayScale = QtWidgets.QLabel(Dialog)
        self._label_DisplayScale.setGeometry(QtCore.QRect(1350, 935, 148, 25))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self._label_DisplayScale.setFont(font)
        self._label_DisplayScale.setEnabled(True)
        self._label_DisplayScale.setStyleSheet("color: rgb(17, 29, 78);"
                                               "background: rgb(181, 220, 241);"
                                               "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self._label_DisplayScale.setObjectName("_label_DisplayScale")
        
        ## Black Level Value
        # spinbox black level
        self.spinBox_BlackLevel = QtWidgets.QSpinBox(Dialog)
        self.spinBox_BlackLevel.setGeometry(QtCore.QRect(1500, 975, 50, 30))
        self.value_black_level = 77
        self.spinBox_BlackLevel.setValue(self.value_black_level) 
        self.spinBox_BlackLevel.setStyleSheet("color: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;") 
        # label of value for black level in reconstruction
        self._label_BlackLevel = QtWidgets.QLabel(Dialog)
        self._label_BlackLevel.setGeometry(QtCore.QRect(1350, 975, 148, 25))
        self._label_BlackLevel.setFont(font)
        self._label_BlackLevel.setStyleSheet("color: rgb(17, 29, 78);"
                                             "background: rgb(181, 220, 241);"
                                             "border-style: outset;"
                                             "border-width: 2px;"
                                             "border-radius: 3px;"
                                             "border-color: grey;"
                                             "padding: 2px;")
        self._label_BlackLevel.setEnabled(True)
        self._label_BlackLevel.setObjectName("_label_BlackLevel")
        
        ## Crop DC Samples
        # spin box to set n-samples from zero-delay (DC-removal) for cropping of DC
        self.spinBox_CropDcSamples = QtWidgets.QSpinBox(Dialog)
        self.spinBox_CropDcSamples.setGeometry(QtCore.QRect(1710, 935, 50, 30))
        self.spinBox_CropDcSamples.setStyleSheet("color: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;")
        self.samples_crop_dc = 25 
        self.samples_crop_hf = 0
        self.spinBox_CropDcSamples.setValue(self.samples_crop_dc)   
        # label to crop n-samples from zero-delay (DC-removal)
        self._label_CropDcSamples = QtWidgets.QLabel(Dialog)
        self._label_CropDcSamples.setGeometry(QtCore.QRect(1560, 935, 148, 25))
        self._label_CropDcSamples.setFont(font)
        self._label_CropDcSamples.setStyleSheet("color: rgb(17, 29, 78);"
                                                "background: rgb(181, 220, 241);"
                                                "border-style: outset;"
                                                "border-width: 2px;"
                                                "border-radius: 3px;"
                                                "border-color: grey;"
                                                "padding: 2px;")
        self._label_CropDcSamples.setEnabled(True)
        self._label_CropDcSamples.setObjectName("label_CropDcSamples")
        
        ## Crop HF Samples
        # spin box to set n-samples from bottom of A-scan
        self.spinBox_CropHfSamples = QtWidgets.QSpinBox(Dialog)
        self.spinBox_CropHfSamples.setGeometry(QtCore.QRect(1710, 975, 50, 30))
        self.spinBox_CropHfSamples.setStyleSheet("color: rgb(231, 243, 251);"
                                              "border-style: outset;"
                                               "border-width: 2px;"
                                               "border-radius: 3px;"
                                               "border-color: grey;"
                                               "padding: 2px;") 
        self.samples_crop_hf = 20
        self.spinBox_CropHfSamples.setValue(self.samples_crop_hf) 
        # label to set n-samples from bottom of A-scan
        self._label_CropHfSamples = QtWidgets.QLabel(Dialog)
        self._label_CropHfSamples.setGeometry(QtCore.QRect(1560, 975, 148, 25))
        self._label_CropHfSamples.setFont(font)
        self._label_CropHfSamples.setStyleSheet("color: rgb(17, 29, 78);"
                                                "background: rgb(181, 220, 241);"
                                                "border-style: outset;"
                                                "border-width: 2px;"
                                                "border-radius: 3px;"
                                                "border-color: grey;"
                                                "padding: 2px;")
        self._label_CropHfSamples.setEnabled(True)
        self._label_CropHfSamples.setObjectName("label_CropHfSamples")        

        #################################################################################
        # Console prints #
        ####################
        # display box for console print displays
        self.label_ConsoleLog = QtWidgets.QLabel(Dialog)
        self.label_ConsoleLog.setGeometry(QtCore.QRect(1070, 600, 260, 400))
        self.label_ConsoleLog.setFrameShape(QtWidgets.QFrame.Box)
        self.label_ConsoleLog.setStyleSheet("background: rgb(231, 243, 251);"
                                            "color: rgb(17, 29, 89)")
        self.label_ConsoleLog.setMidLineWidth(1)
        self.label_ConsoleLog.setObjectName("label_ConsoleLog")
        
        #################################################################################
        # Drop Down Boxes #
        ####################
        # label/head line for windowing function selection field
        self._label_WindowingFunction = QtWidgets.QLabel(Dialog)
        self._label_WindowingFunction.setGeometry(QtCore.QRect(1550, 770, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self._label_WindowingFunction.setFont(font)
        self._label_WindowingFunction.setStyleSheet("color: rgb(231, 243, 251)")
        self._label_WindowingFunction.setObjectName("_label_WindowingFunction")
        self._label_WindowingFunction.setLayoutDirection(QtCore.Qt.LeftToRight) 
        self._label_WindowingFunction.setAlignment(QtCore.Qt.AlignCenter)
        # Windowing options drop down menu
        self.comboBox_windowingOptions = QtWidgets.QComboBox(Dialog)
        self.comboBox_windowingOptions.setGeometry(QtCore.QRect(1550, 800, 220, 30))
        self.comboBox_windowingOptions.setStyleSheet("color: rgb(17, 29, 78);"
                                                     "background: rgb(181, 220, 241)")
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
        self.slideBar_leftBScanWindow.valueChanged['int'].connect(self.spinBox_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.slideBar_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.create_enface_display_widget)
        self.slideBar_rightBScanWindow.valueChanged['int'].connect(self.spinBox_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.slideBar_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.create_enface_display_widget)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        """ add texts and dialog descriptions """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ODD-UI (Oct Data Display - User Interface)"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.checkBox_Endianness.setText(_translate("Dialog", "Data is (IEEE)\nBig Endian"))
        self.pushButton_loadOctData.setText(_translate("Dialog", "Load\nOCT\nData"))
        self.pushButton_runReconstruction.setText(_translate("Dialog", "Reconstruct"))
        self.pushButton_showEnFace.setText(_translate("Dialog", "Show Enface"))
        self.pushButton_displayDispersionCurves.setText(_translate("Dialog", "Show Dispersion"))
        self.pushButton_displayWindowingFunctions.setText(_translate("Dialog", "Show Windowing"))
        self.pushButton_displayAScanAtIntersection.setText(_translate("Dialog", "Show A-scans"))
        self._label_DispCoeffC2.setText(_translate("Dialog", "C2"))
        self._label_DispCoeffC3.setText(_translate("Dialog", "C3"))
        self._label_DispCoeffC1.setText(_translate("Dialog", "C1"))
        self._label_DispCoeffC0.setText(_translate("Dialog", "C0"))
        self._label_aScanLength.setText(_translate("Dialog", "A-Length"))
        self._label_bScanLength.setText(_translate("Dialog", "B-Length"))
        self._label_cScanLength.setText(_translate("Dialog", "C-Length"))
        self.label_ConsoleLog.setText(_translate("Dialog", "Console prints"))
        self._label_BlackLevel.setText(_translate("Dialog", "Black Level Value"))
        self._label_DisplayOptions.setText(_translate("Dialog", "Display Options"))
        self._label_CropHfSamples.setText(_translate("Dialog", "Crop HF [smpls]"))
        self._label_DisplayScale.setText(_translate("Dialog", "Display Scale Factor"))
        self._label_CropDcSamples.setText(_translate("Dialog", "Crop LF/DC [smpls]"))
        self._label_WindowingFunction.setText(_translate("Dialog", "Windowing Function"))
        self._label_DisperisonCoefficients.setText(_translate("Dialog", "Dispersion Coefficients"))
        self._label_leftBscanDisplayCanvas.setText(_translate("Dialog", "Vertical B-scan Display Canvas (red)"))
        self._label_rightBscanDisplayCanvas.setText(_translate("Dialog", "Horizontal B-scan Display Canvas (green)"))

            
    """     ****** SIGNALS ******
        Backend-connected functions     """
    def _load_oct_data(self) -> None :
        """ loads user-selected file containing OCT data and created class-vars raw data buffer and dimensions """
        print("Loading OCT data... ")
        # LOAD DATA FROM FILE: generates meta data of raw data from file name (<data_io> module)
        buffer_oct_raw_data = self.REC.load_oct_data(dtype=self.data_endianness) 
        print(f"Loaded selected data ( shape={buffer_oct_raw_data.shape} and dtype={buffer_oct_raw_data.dtype} ) into memory")
        self.buffer_oct_raw_data = buffer_oct_raw_data
        self.dims_buffer_oct_raw_data = self.REC.oct_dims
        self._update_oct_volume_dimension_display()
        # self._check_oct_data_dims() # check if established OCT volume dimensions are what was expected 
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
     
    ###############################################################################################
    # Update Functions for GUI elements #
    #####################################  
    def _update_oct_volume_dimension_display(self) -> None :
        """ updates the displayed tuple containing the volume dimensions in < OctVolumeDimensionWindow > """
        self.spinBox_aScanLength.setValue( self.dims_buffer_oct_raw_data[0] )
        self.spinBox_bScanLength.setValue( self.dims_buffer_oct_raw_data[1] )
        self.spinBox_cScanLength.setValue( self.dims_buffer_oct_raw_data[2] )
        
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
        self.painterInstance.drawLine(curr_left_idx, 0, curr_left_idx, self.dims_buffer_oct_raw_data[1]) 
        self.painterInstance.setPen(self.h_bScan_line)
        self.painterInstance.drawLine(0, curr_right_idx, self.dims_buffer_oct_raw_data[2], curr_right_idx)
        
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
        self.slideBar_leftBScanWindow.setMaximum(int(y_max))
        self.slideBar_rightBScanWindow.setMaximum(int(x_max))
    
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
        
    def _check_oct_data_dims(self) -> None :
        """ TODO: implement/debug"""
        qst_box = QtWidgets.QMessageBox()
        ret = QtWidgets.QMessageBox.question(self, 
                                             'Correct Dimensions?', 
                                             f"Are the detected dimensions {self.REC.oct_dims} of the volume correct?",
                                             QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                             QtWidgets.QMessageBox.Yes)
        print("Ran through...")
        
    def close_application_via_button(self) :
        """ closes GUI via the CLOSE button -> terminates application """
        self.pushButton_close.clicked.connect(QtCore.QCoreApplication.instance().quit)


def run() :
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UiWindowDialog()
    ui.setupUi(Dialog)
    Dialog.setWindowIcon( QtGui.QIcon(os.path.join(os.path.dirname( __file__ ), 'ZeissLabLogo.jpg')) )
    # Dialog.showMaximized() # comment in if screen resolution == Full HD
    Dialog.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    run()
