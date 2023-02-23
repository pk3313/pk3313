from asyncio.windows_events import NULL
import sys
from tkinter import TOP
from typing import Counter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtTest, QtGui, QtCore, QtWidgets
import pyqtgraph as pg
import os
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, Qt, QThread, QTimer
from PyQt5.QtTest import *
from ClassVar import *
import numpy as np
import serial
import time
# .ui file load
dirName = os.path.dirname(os.path.realpath(__file__))
form_class = uic.loadUiType(os.path.join(dirName, "korearobotics DVL T-program_test.ui"))[0]

# korearobotics DVL T-program_Connect.ui GUI 클래스       
class COMconnect(QDialog):
    def __init__(self):
        super().__init__()
        # PyQt Designer 연결 
        self.ui = uic.loadUi(url.url_text+'korearobotics DVL T-program_Connect.ui')
        self.ui.comboBox_baud.setCurrentText("9600")
        #버튼클릭 함수 호출
        self.ui.pushButton.clicked.connect(self.WinClose)
        self.ui.show()  
    # 확인 버튼 클릭 함수     
    def WinClose(self):
        ui = self.ui
        port.port = ui.comboBox_com.currentText()
        baud.baud = ui.comboBox_baud.currentText()
        #선택한 comboBox의 COMPORT & Baudrate로 Serial 연결 
        self.ser= serial.Serial(port.port,baud.baud, timeout = 0.2)
        print(port.port,baud.baud)
        ui.close()
        Flag.flag = True
    print(port.port,baud.baud)    
            

# Qthread class 
class Thread_(QThread):
    #스레드 내부에서 함수 호출을 위한 signal 정의
    signal = pyqtSignal(list)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent = parent
        self.tmpList = [None]*12    
        self.working = True
        self.startFlag = False
    # 스레드 종료 함수 
    def stop(self):
        QthFlag.QthFlag = False
        self.Thread.terminate()
        self.Thread.wait(5000)
    #스레드 정지 함수       
    def threadstop(self):
        print('there')
        PD13DvlSampleList.PD13DvlSampleList.clear()
        print('clear!!!!!!!!!!!!!')
    #스레드 시작 함수                 
    def run(self):
        cnt=0
        # 메인HMI의 xomboBox가 PD13일때 --> 출력 데이터를 PD13형식으로 받을 때 
        if myWindow.text =="PD13":
            # DVL로 부터 데이터를 실시간으로 받아오는 반복문   
            for c in com.ser:
                if cnt ==11:
                    if self.startFlag == False:
                        myWindow.flag=False
                        # 출력 데이터 전처리 함수 호출 
                        self.signal.connect(myWindow.PD13ButtonFunction)
                        cnt=0
                    else:
                        print("Loop")
                    cnt=0
                else :
                    # DVL로부터 받아온 데이터를 HMI 화면에 출력
                    str_ser = c.decode('utf-8')
                    if len(PD13DvlSampleList.PD13DvlSampleList) >= 12:
                        PD13DvlSampleList.PD13DvlSampleList[cnt] = str_ser
                        self.signal.emit(PD13DvlSampleList.PD13DvlSampleList)
                    else:
                        PD13DvlSampleList.PD13DvlSampleList.append(str_ser)
                        self.signal.emit(PD13DvlSampleList.PD13DvlSampleList)
                    cnt+=1
                QTest.qWait(1000)
        # 메인HMI의 xomboBox가 PD11일때 --> 출력 데이터를 PD11형식으로 받을 때 
        elif myWindow.text =="PD11":
            for c in com.ser:
                if cnt ==3:
                    if self.startFlag == False:
                        myWindow.flag=False
                        # 출력 데이터 전처리 함수 호출 
                        self.signal.connect(myWindow.PD11ButtonFunction)
                        cnt=0
                    else:
                        print("Loop")
                    cnt=0  
                else :
                    # DVL로부터 받아온 데이터를 HMI 화면에 출력
                    str_ser = c.decode('utf-8')
                    if len(PD11DvlSampleList.PD11DvlSampleList) >= 4:
                        PD11DvlSampleList.PD11DvlSampleList[cnt] = str_ser
                        self.signal.emit(PD11DvlSampleList.PD11DvlSampleList)
                    else:
                        PD11DvlSampleList.PD11DvlSampleList.append(str_ser)
                        self.signal.emit(PD11DvlSampleList.PD11DvlSampleList)
                    cnt+=1
                QTest.qWait(1000)
                        
            
#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, QtWidgets.QWidget, form_class) :
    Thread = Thread_() 
    def __init__(self): 
        super().__init__()
        self.initUI()
        
        self.MessageID = 0
        self.add_dataX=[]
        self.add_dataY=[]

        # $PRDIG - [header]
        self.PRDIG_Heading = 2
        self.PRDIG_Pitch = 4
        self.PRDIG_Roll = 6
        self.PRDIG_Depth = 8

        # $PRDIH - [header]
        self.PRDIH_Range2Bottom = 2
        self.PRDIH_SpeedOverGround = 4
        self.PRDIH_CourseOverGround = 6

        # $PRDII - [header]
        self.PRDII_BeaconIndex = 2
        self.PRDII_StatusIndex = 3

        # :SA - [header] // System Attitude data
        self.SA_Pitch = 1
        self.SA_Roll = 2
        self.SA_Heading = 3
        
        # :TS - [header] // Timing and Scaling data
        self.TS_Time = 1
        self.TS_Salinity = 2
        self.TS_Temperature = 3
        self.TS_Depth = 4
        self.TS_SpeedOfSound = 5
        
        # :RA - [header] // Pressure and Range to bottom data
        self.RA_Pressure = 1
        self.RA_Beam1 = 2
        self.RA_Beam2 = 3
        self.RA_Beam3 = 4
        self.RA_Beam4 = 5
        
        # :WI - [header] // Water-mass, Instrument-referenced velocity data
        self.WI_VelX = 1
        self.WI_VelY = 2
        self.WI_VelZ = 3
        self.WI_Error = 4
        self.WI_Status = 5
        
        # :WS - [header] // Water-mass, Ship-referenced velocity data
        self.WS_VelTransverse = 1
        self.WS_VelLongitudinal = 2
        self.WS_VelNormal = 3
        self.WS_Status = 4
        
        # :WE - [header] // Water-mass, Earth-reference velocity data
        self.WE_VelX = 1
        self.WE_VelY = 2
        self.WE_VelZ = 3
        self.WE_Status = 4
        
        # :WD - [header] // Water-mass, Earth-referenced distance data
        self.WD_DistanceX = 1
        self.WD_DistanceY = 2
        self.WD_DistanceZ = 3
        self.WD_Range2WaterMassCenterInMeter = 4
        self.WD_TimeSinceLastGoodVelEstimateInSec = 5
        
        # :BI - [header] // Bottom-track, Instrument-referenced velocity data
        self.BI_VelX = 1
        self.BI_VelY = 2
        self.BI_VelZ = 3
        self.BI_Error = 4
        self.BI_Status = 5
                
        # :BS - [header] // Bottom-track, Ship-referenced velocity data
        self.BS_VelTransverse = 1
        self.BS_VelLongitudinal = 2
        self.BS_VelNormal = 3
        self.BS_Status = 4
        
        # :BE - [header] // Bottom-track, Earth-referenced velocity data
        self.BE_VelX = 1
        self.BE_VelY = 2
        self.BE_VelZ = 3
        self.BE_Status = 4
        
        # :BD - [header] // Bottom-track, Earth-referenced distance data
        self.BD_DistanceX = 1
        self.BD_DistanceY = 2
        self.BD_DistanceZ = 3
        self.BD_Range2WaterMassCenterInMeter = 4
        self.BD_TimeSinceLastGoodVelEstimateInSec = 5
        
        # Count DVL load data
        self.PD11ButtonCount = 0
        self.PD13ButtonCount = 0
        
        self.dvlHeading = None
        self.dvlRoll = None
        self.dvlPitch = None
        self.dvlDepth = None
        self.dvlAltimeter = None        
        
        self.testFlag = False
        self.MappingFlag = True
        
        # Velocity graph data
        self.add_x=[]
        self.add_y=[]
        self.num =0
        self.bi_velX_add_dataY=[]
        self.bi_vel_add_dataX=[]
        self.bi_velY_add_dataY=[]
        self.bi_velZ_add_dataY=[]
        self.pit=0
                         
        # exit Tread def
    def initUI(self):
        self.rollPitchPixmap = QtGui.QPixmap(os.path.join(dirName, 'icon/rollPitch_1.png'))
        self.pitchPixmap = QtGui.QPixmap(os.path.join(dirName, 'icon/pitch1.png'))
        self.headingPixmap = QtGui.QPixmap(os.path.join(dirName, 'icon/heading.png'))
        self.compassPixmap = QtGui.QPixmap(os.path.join(dirName, 'icon/compass.png'))

        # .ui load GUI objects
        self.setupUi(self)
        self.rollLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rollLabel.setPixmap(self.rollPitchPixmap)
        self.pitchLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.pitchLabel.setPixmap(self.pitchPixmap)
        self.headingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.headingLabel.setPixmap(self.headingPixmap)
        self.comboBox.addItem("PD11")
        self.comboBox.addItem("PD13")
        self.comboBox.setCurrentText("PD13")
        self.convert_Software_break.clicked.connect(self.Software_breakFunction)
        self.convert_StartPing.clicked.connect(self.Start_pingFunction)
        self.closeButton.clicked.connect(self.closeButtonFunction)
        self.pushButton.clicked.connect(self.OK_ButtonFunction)

        # Exit - [Menu]
        self.actionQuit.setShortcut("Ctrl+e")
        self.actionQuit.setStatusTip("Exit application")
        self.actionQuit.triggered.connect(QApplication.quit)
        # Device info - [Menu]
        self.actionDevice_Info.setStatusTip("Program Device Information")
        self.actionDevice_Info.triggered.connect(self.deviceInfoButtonFunction)
        # Program info - [Menu]
        self.actionDVL_T_Program_Info.setStatusTip("Program Information")
        self.actionDVL_T_Program_Info.triggered.connect(self.infoButtonFunction)
        self.actionSetting.setStatusTip("Program Setting")
        self.actionSetting.triggered.connect(self.settingButtonFunction)
        
        # Graph_Velocity 
        self.pw1 = pg.PlotWidget(title="Velocity X")
        self.pw2 = pg.PlotWidget(title="Velocity Y")
        self.pw3 = pg.PlotWidget(title="Velocity Z")
        self.vbox1.addWidget(self.pw1)
        self.vbox2.addWidget(self.pw2)
        self.vbox3.addWidget(self.pw3)
    
    #OK 버튼 클릭 함수    
    def OK_ButtonFunction(self):
        # comboBox로부터 선택된 text 값을 가져와 변수에 저장 
        self.text = str(myWindow.comboBox.currentText())
        print(self.text)
        # 출력 데이터 형식이 PD11일 때
        if self.text =="PD11":
            # PD11를 아스키 코드 값으로 변환하여 DVL에 전송
            # 이때 반드시 <CR>값(아스키값 = 13)을 함께 보내줘야 함  
            ascii_list_2=[80,68,49,49,13]
            res = bytes(ascii_list_2)
            com.ser.write(res)
        # 출력 데이터 형식이 PD13일 때    
        elif self.text =="PD13":
            # PD13을 아스키 코드 값으로 변환하여 DVL에 전송
            # 이때 반드시 <CR>값(아스키값 = 13)을 함께 보내줘야 함
            ascii_list=[80,68,49,51,13]
            res = bytes(ascii_list)
            com.ser.write(res)
              
    
    # software break function
    def Software_breakFunction(self) :
        # Software Break를 위한 명령어 (++++)를 Ascii 코드값으로 변환하여 전송 
        ascii_list=[43,43,43,13] # 43 = + , 13 = <CR> 반드시 CR을 붙여줘야 함 
        res = bytes(ascii_list)
        # Software Break 명령어를 전송할 때, 전송 길이가 300이어야 하기 때문에 반복문을 통해 명령어의 길이를 늘림 
        for i in range(300):
            com.ser.write(res)
        
        # 명령어가 잘 인식되었는지 확인하는 코드     
        # for c in com.ser:
        #     str_ser = c.decode('utf-8')
        #     print(str_ser)
        #     i+=1
        #     print(i)
           
                
     
   
        
        # ascii = (stringToascii.ascii(ascii_list))
        # ascii.append(13)
        # res = bytes(ascii)
        # print(ascii)
        # com.ser.write(res)
    # 출력 데이터가 PD11일 때 출력데이터 처리를 위한 함수     
    def PD11ButtonFunction(self) :
        self.PD11ButtonCount = 0    
        self.flag = False
        th = Thread_()
        th.startFlag = True
        if self.flag == False:
            for i in range(3):
                # Original Data에서 가시성을 높이는 전처리 작업 
                PD11DvlSampleList.PD11DvlSampleList[self.PD11ButtonCount] = PD11DvlSampleList.PD11DvlSampleList[self.PD11ButtonCount].replace(" ","").replace("'", "").replace("\n", "")
                self.textBrowser_DVL.append(PD11DvlSampleList.PD11DvlSampleList[self.PD11ButtonCount])
                dvlSampleTmp = PD11DvlSampleList.PD11DvlSampleList[self.PD11ButtonCount].split("*")
                dvlSampleTmp = dvlSampleTmp[0].split(",")
                # PD11 data format에 따른 전처리 작업 (개발보고서 2.2 참고)
                if dvlSampleTmp[self.MessageID] == "$PRDIG":
                    prdig_Heading = dvlSampleTmp[self.PRDIG_Heading]
                    prdig_Pitch = dvlSampleTmp[self.PRDIG_Pitch]
                    prdig_Roll = dvlSampleTmp[self.PRDIG_Roll]
                    prdig_Depth = dvlSampleTmp[self.PRDIG_Depth]
                    self.dvlHeading, self.dvlRoll, self.dvlPitch, self.dvlDepth = prdig_Heading, prdig_Pitch, prdig_Roll, prdig_Depth
                    h = float(prdig_Pitch)
                    data = int(h)
                    self.pitch(data)
                    # 메인 HMI에 전처리된 데이터를 출력
                    self.textBrowser_R_P_H.append("PRDIG Heading : " + str(prdig_Heading))
                    self.textBrowser_R_P_H.append("PRDIG Pitch : " + str(prdig_Pitch))
                    self.textBrowser_R_P_H.append("PRDIG Roll : " + str(prdig_Roll))
                    self.textBrowser_R_P_H.append("PRDIG Depth : " + str(prdig_Depth))
                    self.Rrotate_pixmap(self.headingLabel, self.headingPixmap, self.compassPixmap, self.dvlHeading, "H", os.path.dirname(os.path.realpath(__file__))) # Heading
                    self.rotate_pixmap(self.rollLabel, self.rollPitchPixmap, self.dvlRoll, "R") # Roll
                    # self.DepthAltimeter_Progress(self.depthProgressBar, self.dvlDepth, "D") # Depth
                # PD11 data format에 따른 전처리 작업 (개발보고서 2.2 참고)
                elif dvlSampleTmp[self.MessageID] == "$PRDIH":
                    prdih_Heading = dvlSampleTmp[self.PRDIG_Heading]
                    prdih_Pitch = dvlSampleTmp[self.PRDIG_Pitch]
                    prdih_Roll = dvlSampleTmp[self.PRDIG_Roll]
                # PD11 data format에 따른 전처리 작업 (개발보고서 2.2 참고)    
                elif dvlSampleTmp[self.MessageID] == "$PRDII":
                    prdii_Heading = dvlSampleTmp[self.PRDIG_Heading]
                self.PD11ButtonCount += 1
    
            
    # 출력데이터가 PD13일 때 출력데이터 처리를 위한 함수 
    def PD13ButtonFunction(self) :
        self.flag = False
        th = Thread_()
        th.startFlag = True
        self.PD13ButtonCount = 0
        if self.flag == False:
            for i in range(12):
                #Original Data에서 가시성을 높이는 전처리 작업 
                PD13DvlSampleList.PD13DvlSampleList[self.PD13ButtonCount] = PD13DvlSampleList.PD13DvlSampleList[self.PD13ButtonCount].replace(" ","").replace("'","").replace("\n","")
                self.textBrowser_DVL.append(PD13DvlSampleList.PD13DvlSampleList[self.PD13ButtonCount])
                dvlSampleTmp = PD13DvlSampleList.PD13DvlSampleList[self.PD13ButtonCount].split("*")
                dvlSampleTmp = PD13DvlSampleList.PD13DvlSampleList[self.PD13ButtonCount].split(",")
                # PD13 Data Format에 따른 전처리 작업 (개발보고서 2.2 참고)
                if dvlSampleTmp[self.MessageID] == ":SA":
                    sa_heading, sa_roll, sa_pitch = self.SAParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                    self.dvlHeading, self.dvlRoll, self.dvlPitch = sa_heading, sa_roll, sa_pitch # Heading. Roll, Pitch
                    h = float(self.dvlPitch)
                    data = int(h)
                    self.pitch(data)
                    self.textBrowser_R_P_H.append(f'Heading : {self.dvlHeading}')
                    self.textBrowser_R_P_H.append(f'Roll : {self.dvlRoll}')
                    self.textBrowser_R_P_H.append(f'Pitch : {self.dvlPitch}')
                    self.textBrowser_R_P_H.append(f'==========================')
                    self.Rrotate_pixmap(self.headingLabel, self.headingPixmap, self.compassPixmap, self.dvlHeading, "H", os.path.dirname(os.path.realpath(__file__))) # Heading
                    self.rotate_pixmap(self.rollLabel, self.rollPitchPixmap, self.dvlRoll, "R") # Roll

                elif dvlSampleTmp[self.MessageID] == ":TS":
                    ts_time, ts_salinity, ts_temperature, ts_depth, ts_speedOfSound = self.TSParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                    self.dvlDepth = ts_depth
                    self.textBrowser_Depth.append(f'Depth : {self.dvlDepth}')
                    # self.DepthAltimeter_Progress(self.depthProgressBar, self.dvlDepth, "D") # Depth

                elif dvlSampleTmp[self.MessageID] == ":RA":
                    ra_pressure, ra_beam1, ra_beam2, ra_beam3, ra_beam4, ra_altimeter = self.RAParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                    self.dvlAltimeter = ra_altimeter
                    self.textBrowser_Altimeter.append(f' Altimeter : {self.dvlAltimeter}')
                    # self.DepthAltimeter_Progress(self.altimeterProgressBar, self.dvlAltimeter, "A") # Altimeter
                    
                elif dvlSampleTmp[self.MessageID] == ":WI":
                    wi_velX, wi_velY, wi_velZ, wi_error, wi_status = self.WIParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":WS":
                    ws_velTransverse, ws_velLongitudinal, ws_velNormal, ws_status = self.WSParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":WE":
                    we_velX, we_velY, we_velZ, we_status = self.WEParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":WD":
                    wd_distanceX, wd_distanceY, wd_distanceZ, wd_range2WaterMassCenterInMeter, wd_timeSinceLastGoodVelEstimateInSec = self.WDParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":BI":
                    bi_velX, bi_velY, bi_velZ, bi_error, bi_status = self.BIParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13) 
                    # 메인 HMI에 전처리된 데이터를 출력
                    self.vel_data(bi_velX,bi_velY,bi_velZ)
                    self.textBrowser_VelX.append(f'Velocity_X : {bi_velX}')
                    self.textEdit_velX.append(f'Velocity_X : {bi_velX}')
                    self.textBrowser_VelY.append(f'Velocity_Y : {bi_velY}')
                    self.textEdit_velY.append(f'Velocity_Y : {bi_velY}')
                    self.textBrowser_VelZ.append(f'Velocity_Z : {bi_velZ}')
                    self.textEdit_velZ.append(f'Velocity_Z : {bi_velZ}')
                    
                elif dvlSampleTmp[self.MessageID] == ":BS":
                    bs_velTransverse, bs_velLongitudinal, bs_velNormal, bs_status = self.BSParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":BE":
                    be_velX, be_velY, be_velZ, be_status = self.BEParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                elif dvlSampleTmp[self.MessageID] == ":BD":
                    bd_distanceX, bd_distanceY, bd_distanceZ, bd_range2WaterMassCenterInMeter, bd_timeSinceLastGoodVelEstimateInSec = self.BDParse(dvlSampleTmp[self.MessageID], dvlSampleTmp, self.textBrowser_PD13)
                print('i',i)
                if i ==11:
                    print('in')
                    
                    self.flag = True
                    th.startFlag = False
                    # Thread_.threadstop
                    # th.signal.connect(th.threadstop)      

                self.PD13ButtonCount += 1
        self.textBrowser_DVL.append("========================PD13============================\n")
        self.textBrowser_PD13.append("============================================================")
    # 전처리된 VelocityX,Y,Z값을 메인HMI에 출력 
    def vel_data(self,bi_velX,bi_velY,bi_velZ):
        self.bi_velX_add_dataY.append(float(bi_velX))
        self.bi_velY_add_dataY.append(float(bi_velY))
        self.bi_velZ_add_dataY.append(float(bi_velZ))
        self.bi_vel_add_dataX.append(self.num)
        self.x = self.bi_vel_add_dataX
        self.X_y = self.bi_velX_add_dataY
        self.Y_y = self.bi_velY_add_dataY
        self.Z_y = self.bi_velZ_add_dataY
        if self.num == 50:
            self.num =0
        else :    
            self.num+=1
        # VelocityX,Y,Z Graph 그리는 코드     
        self.pw1.setYRange(-2, 2)
        self.pw2.setYRange(-2, 2)
        self.pw3.setYRange(-2, 2)
        self.plX = self.pw1.plot(pen='r')
        self.plY = self.pw2.plot(pen='g')
        self.plZ = self.pw3.plot(pen='b')
        self.plX.setData(x=self.x,y=self.X_y)
        self.plY.setData(x=self.x,y=self.Y_y)
        self.plZ.setData(x=self.x,y=self.Z_y)
    # Heading 값에 따라 Heading 이미지가 반시계 방향으로 움직이는 코드 
    def pitch(self,pt):
            pitch = int(pt)
            pitch_data=0
            if pitch >0 :
                pitch+=205
            elif pitch <0:
                pitch_data =abs(pitch)
                pitch_data+=205   # base value = 205
            self.pit = pitch_data
    # Pitch 값에 따라 Pitch 이미지 위에 빨간선으로 현재 Pitch 값을 표시하는 코드         
    def paintEvent(self,e):
        qp = QPainter()
        qp.begin(self)
        self.image(qp)
        qp.end()

    def image(self,qp):
        qp.setPen(QPen(Qt.red, 6))
        qp.drawLine(1010, self.pit, 1075, self.pit)
        self.update() 
    
    def draw_chart(self, x,y):
        self.pl.setData(x=x,y=y)
        self.show()
    @pyqtSlot()
    def get_data(self):
        self.x = self.add_dataX
        self.y = [1]
        self.draw_chart(self.x, self.y)  

    # Start ping
    def Start_pingFunction(self) :
        ascii_list=[99,115,13] # CS ascii
        # res = bytes(ascii_list)
        com.ser.write(ascii_list)
        self.threadAction()
    
    # def TestButtonFunction(self):
    #     self.ThreadReset
    
    def closeButtonFunction(self):
        # self.Thread.quit()
        # self.Thread.wait(5000)
        Thread_.stop
        QApplication.quit()

    # def TestThreadFunction(self):
    #     self.testFlag = True
    #     while self.testFlag:
    #         self.dvlHeading=float(self.dvlHeading)
    #         self.dvlRoll=float(self.dvlRoll)
    #         self.dvlPitch=float(self.dvlPitch)
    #         self.dvlDepth=float(self.dvlDepth)
    #         self.dvlAltimeter=float(self.dvlAltimeter)
    #         if self.dvlHeading >= 360:
    #             self.dvlHeading = 0
    #         else:
    #             self.dvlHeading += 5
                
    #         if self.dvlRoll >= 90:
    #             self.dvlRoll = 0
    #         else:
    #             self.dvlRoll += 5
                
    #         if self.dvlPitch >= 90:
    #             self.dvlPitch = 0
    #         else:
    #             self.dvlPitch += 3
                
    #         if self.dvlDepth >= 6000:
    #             self.dvlDepth = 0
    #         else:
    #             self.dvlDepth += 50
                
    #         if self.dvlAltimeter >= 100:
    #             self.dvlAltimeter = 0
    #         else:
    #             self.dvlAltimeter += 4
    #         QtTest.QTest.qWait(1000)
            
    ##========================================================##
    ##                     ToolBar Button                     ##
    ##========================================================##
    # Program info button function - [menu]
    def infoButtonFunction(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.about(self, "Information", 
                  "    DVL T-Program v0.0.1    \r\n\r\n    레드원테크놀러지(주) KPK/BSH    \r\n\r\n    Last Updated [2022.04.07.]    ")

    # Device info button function - [menu]
    def deviceInfoButtonFunction(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.about(self, "Device Information",
                  "    DVL T-Program Device Information    \r\n\r\n    DVL Device     -    ????????  /  ????????    \r\n\r\n    Where to use    -    Pilot  / Navigator  /  Mission\r\n\r\n                              Main Display  /  Mother Vessel")

    def settingButtonFunction(self):
        SettingWindowClass(self)

    ##========================================================##
    ##                      Event Button                      ##
    ##========================================================##
    # Warning message function
    def About_event(self) :
        QMessageBox.about(self,'Message','DVL버튼을 눌러 정보를 불러오세요.')

    ##========================================================##
    ##                   Calculate altimeter                  ##
    ##========================================================##
    # Calculate altimeter using 4 beam (beam1 ... beam4)
    def CalcAltimeter(self, beam1, beam2, beam3, beam4):
        beamNum = 4
        deciMeter2Meter = 10
        altimeter = ((float(beam1)+float(beam2)+float(beam3)+float(beam4))/beamNum)/deciMeter2Meter
        return altimeter

    ##========================================================##
    ##                      Parsing Func                      ##
    ##========================================================##
    # Parsing :SA Data
    def SAParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":SA":
            # Init variable
            heading, roll, pitch = 0, 0, 0
            heading = dvlSampleTmp[self.SA_Heading]
            roll = dvlSampleTmp[self.SA_Roll]
            pitch = dvlSampleTmp[self.SA_Pitch]
            textBrowser.append("SA heading : {}".format(str(heading)))
            textBrowser.append("SA roll : {}".format(str(roll)))
            textBrowser.append("SA pitch : {}".format(str(pitch)))
        return heading, roll, pitch
    
    # Parsing :TS Data
    def TSParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":TS":
            # Init variable
            Time, Salinity, Temperature, Depth, SpeedOfSound = 0, 0, 0, 0, 0
            Time = dvlSampleTmp[self.TS_Time]
            Salinity = dvlSampleTmp[self.TS_Salinity]
            Temperature = dvlSampleTmp[self.TS_Temperature]
            Depth = dvlSampleTmp[self.TS_Depth]
            SpeedOfSound = dvlSampleTmp[self.TS_SpeedOfSound]
            textBrowser.append("TS Time : {}".format(str(Time)))
            textBrowser.append("TS Salinity : {}".format(str(Salinity)))
            textBrowser.append("TS Temperature : {}".format(str(Temperature)))
            textBrowser.append("TS Depth : {}".format(str(Depth)))
            textBrowser.append("TS SpeedOfSound : {}".format(str(SpeedOfSound)))
        return Time, Salinity, Temperature, Depth, SpeedOfSound

    # Parsing :RA Data
    def RAParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":RA":
            # Init variable
            pressure, beam1, beam2, beam3, beam4, altimeter = 0, 0, 0, 0, 0, 0
            pressure = dvlSampleTmp[self.RA_Pressure]
            beam1 = dvlSampleTmp[self.RA_Beam1]
            beam2 = dvlSampleTmp[self.RA_Beam2]
            beam3 = dvlSampleTmp[self.RA_Beam3]
            beam4 = dvlSampleTmp[self.RA_Beam4]
            altimeter = self.CalcAltimeter(beam1, beam2, beam3, beam4)
            textBrowser.append("RA Pressure : {}".format(str(pressure)))
            textBrowser.append("RA Beam1 : {}".format(str(beam1)))
            textBrowser.append("RA Beam2 : {}".format(str(beam2)))
            textBrowser.append("RA Beam3 : {}".format(str(beam3)))
            textBrowser.append("RA Beam4 : {}".format(str(beam4)))
            textBrowser.append("RA Altimeter : {}".format(str(altimeter)))
        return pressure, beam1, beam2, beam3, beam4, altimeter
    
    # Parsing :WI Data
    def WIParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":WI":
            # Init variable
            velX, velY, velZ, error, status = 0, 0, 0, 0, 0
            velX = dvlSampleTmp[self.WI_VelX]
            velY = dvlSampleTmp[self.WI_VelY]
            velZ = dvlSampleTmp[self.WI_VelZ]
            error = dvlSampleTmp[self.WI_Error]
            status = dvlSampleTmp[self.WI_Status]
            textBrowser.append("WI velX : {}".format(str(velX)))
            textBrowser.append("WI velY : {}".format(str(velY)))
            textBrowser.append("WI velZ : {}".format(str(velZ)))
            textBrowser.append("WI error : {}".format(str(error)))
            textBrowser.append("WI status : {}".format(str(status)))
        return velX, velY, velZ, error, status
    
    # Parsing :WS Data
    def WSParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":WS":
            # Init variable
            velTransverse, velLongitudinal, velNormal, status = 0, 0, 0, 0
            velTransverse = dvlSampleTmp[self.WS_VelTransverse]
            velLongitudinal = dvlSampleTmp[self.WS_VelLongitudinal]
            velNormal = dvlSampleTmp[self.WS_VelNormal]
            status = dvlSampleTmp[self.WS_Status]
            textBrowser.append("WS velTransverse : {}".format(str(velTransverse)))
            textBrowser.append("WS velLongitudinal : {}".format(str(velLongitudinal)))
            textBrowser.append("WS velNormal : {}".format(str(velNormal)))
            textBrowser.append("WS status : {}".format(str(status)))
        return velTransverse, velLongitudinal, velNormal, status

    # Parsing :WE Data
    def WEParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":WE":
            # Init variable
            velX, velY, velZ, status = 0, 0, 0, 0
            velX = dvlSampleTmp[self.WE_VelX]
            velY = dvlSampleTmp[self.WE_VelY]
            velZ = dvlSampleTmp[self.WE_VelZ]
            status = dvlSampleTmp[self.WE_Status]
            textBrowser.append("WE velX : {}".format(str(velX)))
            textBrowser.append("WE velY : {}".format(str(velY)))
            textBrowser.append("WE velZ : {}".format(str(velZ)))
            textBrowser.append("WE status : {}".format(str(status)))
        return velX, velY, velZ, status
    
    # Parsing :WD Data
    def WDParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":WD":
            # Init variable
            distanceX, distanceY, distanceZ, range2WaterMassCenterInMeter, timeSinceLastGoodVelEstimateInSec = 0, 0, 0, 0, 0
            distanceX = dvlSampleTmp[self.WD_DistanceX]
            distanceY = dvlSampleTmp[self.WD_DistanceY]
            distanceZ = dvlSampleTmp[self.WD_DistanceZ]
            range2WaterMassCenterInMeter = dvlSampleTmp[self.WD_Range2WaterMassCenterInMeter]
            timeSinceLastGoodVelEstimateInSec = dvlSampleTmp[self.WD_TimeSinceLastGoodVelEstimateInSec]
            textBrowser.append("WD distanceX : {}".format(str(distanceX)))
            textBrowser.append("WD distanceY : {}".format(str(distanceY)))
            textBrowser.append("WD distanceZ : {}".format(str(distanceZ)))
            textBrowser.append("WD range2WaterMassCenterInMeter : {}".format(str(range2WaterMassCenterInMeter)))
            textBrowser.append("WD timeSinceLastGoodVelEstimateInSec : {}".format(str(timeSinceLastGoodVelEstimateInSec)))
        return distanceX, distanceY, distanceZ, range2WaterMassCenterInMeter, timeSinceLastGoodVelEstimateInSec

    # Parsing :BI Data
    def BIParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":BI":
            # Init variable
            velX, velY, velZ, error, status = 0, 0, 0, 0, 0
            velX = dvlSampleTmp[self.BI_VelX]
            velY = dvlSampleTmp[self.BI_VelY]
            velZ = dvlSampleTmp[self.BI_VelZ]
            error = dvlSampleTmp[self.BI_Error]
            status = dvlSampleTmp[self.BI_Status]
            textBrowser.append("BI velX : {}".format(str(velX)))
            textBrowser.append("BI velY : {}".format(str(velY)))
            textBrowser.append("BI velZ : {}".format(str(velZ)))
            textBrowser.append("BI error : {}".format(str(error)))
            textBrowser.append("BI status : {}".format(str(status)))
        return velX, velY, velZ, error, status
    
    # Parsing :BS Data
    def BSParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":BS":
            # Init variable
            velTransverse, velLongitudinal, velNormal, status = 0, 0, 0, 0
            velTransverse = dvlSampleTmp[self.BS_VelTransverse]
            velLongitudinal = dvlSampleTmp[self.BS_VelLongitudinal]
            velNormal = dvlSampleTmp[self.BS_VelNormal]
            status = dvlSampleTmp[self.BS_Status]
            textBrowser.append("BS velTransverse : {}".format(str(velTransverse)))
            textBrowser.append("BS velLongitudinal : {}".format(str(velLongitudinal)))
            textBrowser.append("BS velNormal : {}".format(str(velNormal)))
            textBrowser.append("BS status : {}".format(str(status)))
        return velTransverse, velLongitudinal, velNormal, status
    
    # Parsing :BE Data
    def BEParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":BE":
            # Init variable
            velX, velY, velZ, status = 0, 0, 0, 0
            velX = dvlSampleTmp[self.BE_VelX]
            velY = dvlSampleTmp[self.BE_VelY]
            velZ = dvlSampleTmp[self.BE_VelZ]
            status = dvlSampleTmp[self.BE_Status]
            textBrowser.append("BE velX : {}".format(str(velX)))
            textBrowser.append("BE velY : {}".format(str(velY)))
            textBrowser.append("BE velZ : {}".format(str(velZ)))
            textBrowser.append("BE status : {}".format(str(status)))
        return velX, velY, velZ, status

    # Parsing :BD Data
    def BDParse(self, header, dvlSampleTmp, textBrowser):
        if header == ":BD":
            # Init variable
            distanceX, distanceY, distanceZ, range2WaterMassCenterInMeter, timeSinceLastGoodVelEstimateInSec = 0, 0, 0, 0, 0
            distanceX = dvlSampleTmp[self.BD_DistanceX]
            distanceY = dvlSampleTmp[self.BD_DistanceY]
            distanceZ = dvlSampleTmp[self.BD_DistanceZ]
            range2WaterMassCenterInMeter = dvlSampleTmp[self.BD_Range2WaterMassCenterInMeter]
            timeSinceLastGoodVelEstimateInSec = dvlSampleTmp[self.BD_TimeSinceLastGoodVelEstimateInSec]
            textBrowser.append("BD distanceX : {}".format(str(distanceX)))
            textBrowser.append("BD distanceY : {}".format(str(distanceY)))
            textBrowser.append("BD distanceZ : {}".format(str(distanceZ)))
            textBrowser.append("BD range2WaterMassCenterInMeter : {}".format(str(range2WaterMassCenterInMeter)))
            textBrowser.append("BD timeSinceLastGoodVelEstimateInSec : {}".format(str(timeSinceLastGoodVelEstimateInSec)))
        return distanceX, distanceY, distanceZ, range2WaterMassCenterInMeter, timeSinceLastGoodVelEstimateInSec

    ##========================================================##
    ##                   Drawing Roll/Pitch                   ##
    ##========================================================##
    def rotate_pixmap(self, label, pixmaptmp, rotation, mode):
        pixmap = pixmaptmp.copy()
        transform = QtGui.QTransform().rotate(float(rotation))
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        self.headingPixmap
        self.compassPixmap
            
    def Rrotate_pixmap(self, label, rawPix, pixmaptmp, rotation, mode, mydir):
        pixmap = rawPix
        rot = float(rotation)
        rot*=-1
        transform = QtGui.QTransform().rotate(float(rot))
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        
    def RRrotate_pixmap(self, label, rawPix, pixmaptmp, rotation, mode, mydir):
        pixmap = pixmaptmp.copy()
        transform = QtGui.QTransform().rotate(float(rotation))
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        
        radius = 1000
        r = QtCore.QRectF()
        r.setSize(radius * QtCore.QSizeF(1, 1))
        r.moveCenter(rawPix.rect().center())
        path = QtGui.QPainterPath()
        path.addEllipse(r)
        painter = QtGui.QPainter(rawPix)
        painter.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform
        )
        painter.setClipPath(path, QtCore.Qt.IntersectClip)
        painter.drawPixmap(r.center()/2, pixmap)
        painter.end()
        label.setPixmap(rawPix)
    
    ##========================================================##
    ##                Set Progress Depth/Alti                 ##
    ##========================================================##
    def DepthAltimeter_Progress(self, progressBar, value, mode):
        progressBar.setValue(float(value))
        # print("{} : {}".format(mode, value))

      # serial communication 
        
    def threadAction(self):
        # self.x = Thread_(self)
        QthFlag.QthFlag = True
        self.Thread.start()
        
    # Setting UI Class 선언
class SettingWindowClass(QDialog):
    def __init__(self,parent) :
        super().__init__(parent)
        # PyQt Designer 연결
        self.ui = uic.loadUi(url.url_text_2+"korearobotics DVL T-program_setting.ui")
        # 버튼 클릭 이벤트 
        self.ui.pushButton_ok.clicked.connect(self.pushButtonClick)
        self.ui.pushButton_reset.clicked.connect(self.pushButtonReset)
        self.ui.show() 
        # 도움말 출력 
        self.f = open(url.url_text_2+"data\\how_to_use.txt",encoding='utf-8')
        self.note = self.f.readlines()
        for i in self.note:
            self.ui.textBrowser_showhelp.append(i)
    # 명령어 전송을 위한 버튼 클릭 이벤트 함수     
    def pushButtonClick(self):
        ui = self.ui
        self.text = ui.textEdit_inputcommand.toPlainText()
        if self.text == 'c?'or self.text == 'C?':
            self.ui.textBrowser_showhelp.clear()
            self.f = open(url.url_text_2+"data\\READ_ME.txt",encoding='utf-8')
            note = self.f.readlines() 
            for i in note:
                self.ui.textBrowser_showhelp.append(i)
        # 입력받은 명령어를 Ascii 코드 값으로 변환하여 DVL에 전송         
        for i in self.text:                     
            ascii_text.ascii_text.append(ord(i))
            # print(ascii_text.ascii_text)
        ascii_text.ascii_text.append(13)    
        com.ser.write(ascii_text.ascii_text)
        # DVL에 전송한 출력값(명령어)에 대한 결과값을 HMI에 출력
        for c in com.ser:
            str_ser = c.decode('utf-8')
            ui.textBrowser_show.append(str_ser)
    # Reset 버튼 클릭 이벤트 함수                   
    def pushButtonReset(self):
        ui = self.ui
        # 메인 HMI 화면 클리어 
        ui.textBrowser_show.clear()
        ui.textBrowser_showhelp.clear()
        ui.textEdit_inputcommand.clear()
        for i in self.note:
            self.ui.textBrowser_showhelp.append(i)
            

# Running the main window class / show main window GUI
if __name__ == "__main__" :
    app = 0
    app = QApplication(sys.argv)
    com = COMconnect()
    app.exec_()
    if Flag.flag == True:
        myWindow = WindowClass()
        myWindow.show()
        # sys.exit(app.exec_())
        app.exec_()
    # sys.exit(app.exec_())
    
    
    
###### to do list 
# 5월  9일 -> port 설정 GUI 생성 , setting GUI 생성 
# 5월 10일 -> GUI와 메인 코드 통합 & 오류 수정 ( 내장 라이브러리(serial.write함수)에서 에러 발생 -> serial 연결 코드 추가로 해결)
# 5월 11일 -> 1. VSCode를 종료해도 QThread가 종료되지 않아 액세스 거부 에러 발생 -> 원인: 쓰레드가 종료 되지 않음 , 종료 함수 작성하여 문제 해결
#             2.  