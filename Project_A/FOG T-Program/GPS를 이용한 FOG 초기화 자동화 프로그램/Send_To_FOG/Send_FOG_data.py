import datetime
from sqlite3 import Time
import sys
import math
import os
import time
import socket
from PySide2.QtWidgets import QMessageBox
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from spatial_device import Spatial
from anpp_packets.packets.an_packet_protocol import AN_Packet, an_packet_decode
from anpp_packets.packets import anpp_packets 
from vars import *

TRUE = 1
FALSE = 0
# load Pyqt design file
dirName = os.path.dirname(os.path.realpath(__file__))
form_class = uic.loadUiType(os.path.join(dirName,"Main.ui"))[0]
comport = 'COM3'
baudrate = 115200
spatial = Spatial(comport, baudrate, log = True)

# setting comport & baudrate. Base = 'COM2, 115200'

class WindowClass(QMainWindow, QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Manual_transmit_button.clicked.connect(self.def_bool)
        self.Clear_button.clicked.connect(self.FOGOutputClearButton)
        self.GPSRecvbutton.clicked.connect(self.recv_data)
        self.Automatic_transmit_button.clicked.connect(self.sendToFOG)
    
    # 입력값 체크 함수 
    def is_digit(self,str1,str2,str3):
        try:
            # 입력값이 float 일 경우 True 반환
            tmp,tmp2,tmp3 = float(str1),float(str2),float(str3)
            return True
        except ValueError:
            return False
    
    # FOGOutput Clear 함수 
    def FOGOutputClearButton(self):
        self.FOGOutput.setPlainText('')
    
    # 입력값 초기화 함수 
    def textreset(self):
        # 입력값 초기화 setPlainText = 입력값 set 함수
        self.Lat_text.setPlainText('')
        self.Long_text.setPlainText('')
        self.Heading_text.setPlainText('')
        
    # lat, long, heading 값 입력 체크 함수
    def def_bool(self):
        
        #toPlainText = 입력값 가져오는 함수
        lat = self.Lat_text.toPlainText()
        lon = self.Long_text.toPlainText()
        hed = self.Heading_text.toPlainText()
        
        # 입력값이 비어있는지 확인하는 조건문
        if lat == '' or lon == '' or hed == '' :
            print("hrrr")
            # 위도, 경도, 헤딩값을 입력하지 않았을 경우 경고 메시지창을 띄우기 위함.
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Warning")
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setInformativeText("위도, 경도, 헤딩 값을 입력해주세요.")  
            self.textreset()
            return msgBox.exec_()
        
        elif self.is_digit(lat,lon,hed):
            print("running!!!")
            print(f"lat : {lat} \n "
                  f"lon : {lon} \n "
                  f"hed : {hed} \n ")
            
            # FOGOutput에 띄우기 위한 append 
            data.data.append(float(lat)) # latitude
            data.data.append(float(lon)) # longitude
            data.data.append(170.01234)     # Height
            data.heading = float(hed)    # Heading
            repeatControl.repeatControl = True
            self.textreset()
            spatial_run = spatialRun()
            spatial_run.running()
            self.textreset()
        else:
            print("숫자만 입력하셈요")
            self.textreset()


    # GPS 데이터 recv 함수 (소켓통신)
    def recv_data(self):
        ip = '192.168.127.250'
        port = 9999
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('',port))
        
        # GPS 데이터를 계속해서 화면에 출력해줌 
        while data.rotate:
            self.orig_data, addr = sock.recvfrom(1024)
            print(self.orig_data)
            self.str_data = (self.orig_data.decode('utf-8'))
            self.gpsData = self.str_data.split(',')
            
            # gpsData == 'H' == Heading Data
            if self.gpsData[0] == 'H':
                data.HeadingData = self.gpsData[1]
                self.GPS_orig_Output.append(f"Heading : {data.HeadingData}")
                self.GPS_HeadingText.append(data.HeadingData)
            
            # gpsData == 'L' == Lat, Lon Data
            elif self.gpsData[0] =='L':
                data.LatitudeData = self.gpsData[1]
                data.LongitudeData = self.gpsData[2]
                self.GPS_orig_Output.append(f"Latitude : {data.LatitudeData}")
                self.GPS_orig_Output.append(f"Longitude : {data.LongitudeData}")
                self.GPS_LatText.append(data.LatitudeData)
                self.GPS_LongText.append(data.LongitudeData)
            
            # 화면 출력 함수 
            QApplication.processEvents()
            time.sleep(0.5)
    

    def sendToFOG(self):
        # FOG로 데이터를 전송하는 코드
        spa = spatialRun() 
        data.latitude =(float(data.LatitudeData))
        data.longitude =(float(data.LongitudeData))
        data.heading = data.HeadingData

        self.GPS_LatText.append(data.LatitudeData)
        self.GPS_LongText.append(data.LongitudeData)
        self.GPS_HeadingText.append(data.HeadingData)
        if  data.LatitudeData != None and data.LongitudeData != None:
            spa.running()
            

class spatialRun():
    def __init__(self):
        pass
   
    # 데이터 run 함수 
    def running(self):   
        spatial.start_serial()
        
        # Checks serial port connection is open
        if spatial.is_open:
            print(f"Connected to port:{spatial.port} with baud:{spatial.baud}")
            spatial.flush()
            an_packet = AN_Packet()
            
            #FOG로 데이터를 전송하는 함수들
            spatial.set_lat_lon_data(data.latitude,data.longitude) # ==> Latitude, longitude 
            spatial.external_time_packet()
            spatial.request_packet(45)
            print('heading =',data.heading)
            spatial.set_heading_data(float(data.heading))     
            spatial.request_packet(48)
            print("sended data")
            time.sleep(1)
            repeatControl.repeatControl = True
            

            # FOG로 부터 데이터를 받아오는 코드 
            while(repeatControl.repeatControl):
                if (spatial.in_waiting() > 0):

                    # Get bytes in serial buffer
                    bytes_in_buffer = spatial.in_waiting()
                    data_bytes = spatial.read(bytes_in_buffer)

                    # Adds bytes to array for decoding
                    spatial.bytes_waiting.add_data(packet_bytes = data_bytes)

                if (len(spatial.bytes_waiting.buffer) > 0):
                    an_packet, spatial.bytes_waiting = an_packet_decode(spatial.bytes_waiting)

                    if (an_packet is not None):
                        if (an_packet.id == spatial.PacketID.acknowledge.value):
                            acknowledge = spatial.AcknowledgePacket()
                            if (acknowledge.decode(an_packet) ==0):
                                print(f"acknowledge.acknowledge_result: {acknowledge.acknowledge_result.value}")
                                print(f"acknowledge.acknowledge_PacketID: {acknowledge.packet_id}")
                        elif(an_packet.id == spatial.PacketID.system_state.value):
                            system_state_packet = spatial.SystemStatePacket()
                            FilterStatus = spatial.FilterStatus()
                            if (system_state_packet.decode(an_packet) == 0):
                                myWindow.FOGOutput.append(f"Latitude:{math.degrees(system_state_packet.latitude)}")
                                myWindow.FOGOutput.append(f"Longitude:{math.degrees(system_state_packet.longitude)}")
                                myWindow.FOGOutput.append(f"Heading:{math.degrees(system_state_packet.orientation[2])}")
                                print(f"System State Packet:\n"
                                    f"\tLatitude:{math.degrees(system_state_packet.latitude)}, "
                                    f"Longitude:{math.degrees(system_state_packet.longitude)}, "
                                    f"Heading:{math.degrees(system_state_packet.orientation[2])},")
                                print(f"external_position_active:{FilterStatus.external_position_active}")
                                QApplication.processEvents()
                                
                                repeatControl.repeatControl = False
                        
                        else:
                            pass
                    
        else:
            print(f"No connection.")

        spatial.close()
    
if __name__ == '__main__':
    app = 0
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
        