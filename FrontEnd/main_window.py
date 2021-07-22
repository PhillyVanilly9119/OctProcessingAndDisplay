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
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

# custom imports
sys.path.append(r"D:\PhilippDataAndFiles\Programming\Repositories\OctProcessingAndDisplay\Backend") # TODO: make relative import 
from data_io import OctDataFileManager
from recon_funcs import OctReconstructionManager


class UiWindowDialog(object) :
    def __init__(self) -> None:
        super().__init__()
        self.IO = OctDataFileManager()
        self.REC = OctReconstructionManager()
         
    def setupUi(self, Dialog):
        # create dialog box / GUI-display-canvass
        Dialog.setObjectName("Dialog")
        Dialog.resize(1920, 1080)
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
        # close/end application push button
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
        # push button for loading OCT data - with customized font
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
        # LEFT = VERTICAL B-scan selection spin box
        self.spinBox_leftBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_leftBScanWindow.setGeometry(QtCore.QRect(890, 600, 60, 30))
        self.spinBox_leftBScanWindow.setObjectName("spinBox_leftBScanWindow")
        # RIGHT = HORIZONTAL B-scan selection spin box
        self.spinBox_rightBScanWindow = QtWidgets.QSpinBox(Dialog)
        self.spinBox_rightBScanWindow.setGeometry(QtCore.QRect(970, 600, 60, 30))
        self.spinBox_rightBScanWindow.setObjectName("spinBox_rightBScanWindow")
        # enface display push button
        self.pushButton_showEnFace = QtWidgets.QPushButton(Dialog)
        self.pushButton_showEnFace.setGeometry(QtCore.QRect(1120, 830, 230, 40))
        self.pushButton_showEnFace.setObjectName("pushButton_showEnFace")
        # A-scan display push button
        self.pushButton_displayAScanAtIntersection = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayAScanAtIntersection.setGeometry(QtCore.QRect(1120, 890, 230, 40))
        self.pushButton_displayAScanAtIntersection.setObjectName("pushButton_displayAScanAtIntersection")
        # polynomial function for dispersion correction display  
        self.pushButton_displayDispersionCurves = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayDispersionCurves.setGeometry(QtCore.QRect(1120, 950, 230, 40))
        self.pushButton_displayDispersionCurves.setObjectName("pushButton_displayDispersionCurves")
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
        # convolutional/windowing functions plot/display 
        self.pushButton_displayWindowingFunctions = QtWidgets.QPushButton(Dialog)
        self.pushButton_displayWindowingFunctions.setGeometry(QtCore.QRect(1120, 1010, 230, 40))
        self.pushButton_displayWindowingFunctions.setObjectName("pushButton_displayWindowingFunctions")
        self.pushButton_runReconstruction = QtWidgets.QPushButton(Dialog)
        self.pushButton_runReconstruction.setGeometry(QtCore.QRect(1120, 650, 230, 80))
        # perform reconstruction for current pair of B-scans
        font = QtGui.QFont()
        font.setFamily("Verdana Pro Semibold")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_runReconstruction.setFont(font)
        self.pushButton_runReconstruction.setDefault(True)
        self.pushButton_runReconstruction.setFlat(False)
        self.pushButton_runReconstruction.setObjectName("pushButton_runReconstruction")
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
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1630, 680, 240, 60))
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
        font.setPointSize(10)
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
        # display box for console print displays
        self.label_ConsoleLog = QtWidgets.QLabel(Dialog)
        self.label_ConsoleLog.setGeometry(QtCore.QRect(1380, 820, 380, 230))
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
        
        #######################################
        #   ***** SIGNALS AND CONNECTIONS *****
        #######################################
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
        self.spinBox_DispCoeffC1.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC1.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_DispCoeffC2.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC2.valueChanged.connect(self.update_disp_coeff_tuple)
        self.spinBox_DispCoeffC3.valueChanged.connect(self.display_current_disp_curves)
        self.spinBox_DispCoeffC3.valueChanged.connect(self.update_disp_coeff_tuple)
        
        # couple B-scan display selection elements
        self.horizontalSlider_leftBScanWindow.valueChanged['int'].connect(self.spinBox_leftBScanWindow.setValue)
        self.spinBox_leftBScanWindow.valueChanged['int'].connect(self.horizontalSlider_leftBScanWindow.setValue)
        self.horizontalSlider_rightBScanWindow.valueChanged['int'].connect(self.spinBox_rightBScanWindow.setValue)
        self.spinBox_rightBScanWindow.valueChanged['int'].connect(self.horizontalSlider_rightBScanWindow.setValue)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        """ add texts and dialog descriptions """
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "ODD-UI (Oct Data Display - User Interface)"))
        self.pushButton_close.setText(_translate("Dialog", "Close"))
        self.pushButton_loadOctData.setText(_translate("Dialog", "Load\nOCT\nData"))
        self.pushButton_showEnFace.setText(_translate("Dialog", "Show en face OCT and update lines"))
        self.pushButton_displayAScanAtIntersection.setText(_translate("Dialog", "Display A-scan at Intersection"))
        self.pushButton_displayDispersionCurves.setText(_translate("Dialog", "Plot Dispersion Curves"))
        self.pushButton_displayWindowingFunctions.setText(_translate("Dialog", "Plot Windowing Function"))
        self.pushButton_runReconstruction.setText(_translate("Dialog", "Reconstruct"))
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
        buffer_oct_raw_data = self.IO.load_oct_data() 
        print(f"Loaded selected data (shape={buffer_oct_raw_data.shape}) into memory")
        self.buffer_oct_raw_data = buffer_oct_raw_data
        self.dims_buffer_oct_raw_data = buffer_oct_raw_data.shape
        self.flag_loaded_oct_data = True
        self.set_spinbox_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 
        self.set_bScan_slider_max_values(self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]) 

    def create_enface_display_widget(self) -> None :
        # NOTE: Enface image is a numpy array with ones for now
        if not self._is_no_oct_data_loaded():
            return
        # TODO: update only the overlay line and avoid recalculating the enface image
        # TODO: uncomment, once it is implemented
        # self.display_enface_image()
        
        dummy_enface = np.full((self.dims_buffer_oct_raw_data[1], self.dims_buffer_oct_raw_data[2]), 1)
        # dummy_enface = cv2.cvtColor(dummy_enface, cv2.COLOR_GRAY2BGR)
        q_curr_hori_scan = QtGui.QImage(dummy_enface.data.tobytes(), 
                                        dummy_enface.shape[1], dummy_enface.shape[0], 
                                        QtGui.QImage.Format_Indexed8)
        # convert image file into pixmap
        self.pixmap_image = QtGui.QPixmap(q_curr_hori_scan)
        # create painter instance with pixmap
        self.painterInstance = QtGui.QPainter(self.pixmap_image)
        self.update_pos_Bscan_indicating_lines(self.spinBox_leftBScanWindow.value(),
                                               self.spinBox_rightBScanWindow.value())
        self.painterInstance.end() # instance has to be deleted after every update
        # set pixmap as displayed output on label widget
        self.EnfaceDisplayWindow.setPixmap(self.pixmap_image)
        self.EnfaceDisplayWindow.setScaledContents(True)
    
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
        
    def display_aScans_at_intersection(self) :
        """ displays the raw (left top side canvas) and recostructed (right top side canvas) A-scan 
        at the selected B-scan intersection """
        if not self._is_no_oct_data_loaded():
            return
        # display raw A-scan at intersection in left-hand-side top canvas
        fig = Figure(figsize=(5, 4), dpi=300)
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
        fig = Figure(figsize=(5, 4), dpi=300)
        canvas = FigureCanvasAgg(fig)
        ax = fig.add_subplot(111)
        ax.set_title(f"Reconstructed A-scan at intersection")
        a_scan = self.buffer_oct_raw_data[:, self.spinBox_rightBScanWindow.value()-1, self.spinBox_leftBScanWindow.value()-1]
        ax.plot(self.REC.reconstruct_buffer(a_scan))
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
        fig = Figure(figsize=(5, 4), dpi=300)
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
        fig = Figure(figsize=(5, 4), dpi=300)
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

    def display_enface_image(self) :
        # TODO: implement computationally inexpensive version of enface
        if not self.flag_calculate_enface:
            print("Calculating Enface")
            
            # self.overlay_BScans_with_lines()
            
            # enface = self.REC.reconstruct_buffer(self.buffer_oct_raw_data) # add disp coeffs and windowing key 
            # q_enface = cv2.cvtColor(enface , cv2.COLOR_GRAY2BGR)
            # q_enface = QtGui.QImage(q_enface.data.tobytes(), q_enface.shape[1], q_enface.shape[0], QtGui.QImage.Format_Indexed8)
            # self.EnfaceDisplayWindow.setPixmap( QtGui.QPixmap(q_enface) )
            # self.EnfaceDisplayWindow.setScaledContents(True) 
            # self.flag_calculate_enface = True
        else :
            print("Enface has already been calculated")

    def run_recon_for_current_settings(self) :
        """ runs recosntruction from backend on cirrently selected pair of B-scans in volume """
        # TODO: implement enface calculation (in backend and then call here)
        if not self._is_no_oct_data_loaded():
            return
        print("Reconstructing...")
        # create/update vertical/left scan (dims_buffer_oct_raw_data[1])
        curr_vert_raw = self.buffer_oct_raw_data[:,:,self.spinBox_leftBScanWindow.value()-1]
        curr_vert_recon = self.REC.reconstruct_buffer(curr_vert_raw, self.disp_coeffs_tuple, self.curr_wind_key[0])
        curr_vert_recon = cv2.cvtColor(curr_vert_recon, cv2.COLOR_BAYER_GR2GRAY)
        img_left_vert = QtGui.QImage(curr_vert_recon.data.tobytes(), self.dims_buffer_oct_raw_data[1], 
                                        self.dims_buffer_oct_raw_data[0], QtGui.QImage.Format_Grayscale8)
        self.Left_BScanWindow.setPixmap( QtGui.QPixmap(img_left_vert) )
        self.Left_BScanWindow.setScaledContents(True) 
        # create/update horizontal/right scan (dims_buffer_oct_raw_data[2])
        curr_hori_raw = self.buffer_oct_raw_data[:,self.spinBox_rightBScanWindow.value()-1]
        curr_hori_recon = self.REC.reconstruct_buffer(curr_hori_raw, self.disp_coeffs_tuple, self.curr_wind_key[0])
        curr_hori_recon = cv2.cvtColor(curr_hori_recon, cv2.COLOR_BAYER_GR2GRAY)
        img_right_hori = QtGui.QImage(curr_hori_recon.data.tobytes(), self.dims_buffer_oct_raw_data[2], 
                                        self.dims_buffer_oct_raw_data[0], QtGui.QImage.Format_Grayscale8)
        self.Right_BScanWindow.setPixmap( QtGui.QPixmap(img_right_hori) )
        self.Right_BScanWindow.setScaledContents(True) # 2 display reconstructed B-scan pain
        # update lines indicating the B-scan positions in the enface image 
        self.create_enface_display_widget()
        # TODO: call "real" enface function here - right now just the dummy function is called 
          
    def update_wind_fct_key(self) -> None :
        """ updates the key (class var) with the windowing function for reconstruction """
        self.curr_wind_key = self.comboBox_windowingOptions.currentData()
        
    def update_disp_coeff_tuple(self) -> None :
        """ updates tuple (clas var) containing the dispersion correction polynominal coefficients 
        according to the current spin box combinations/settings"""
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
    Dialog.show()
    sys.exit(app.exec_())
        
if __name__ == "__main__":
    run()
