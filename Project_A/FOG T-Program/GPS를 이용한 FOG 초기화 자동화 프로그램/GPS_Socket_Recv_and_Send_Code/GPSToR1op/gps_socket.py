import serial
import socket

com = 'COM6'
baudrate = 9600
ser = serial.Serial(com, baudrate, timeout=1)
MessageID = 0
GPGLatDeg = 2
GPGLonDeg = 4
GPGHeighMSL = 9
GPGGPSSatNo = 7
GPHHeadDeg = 1
gpsButtonCount = 0
isabuButtonCount = 0
jysButtonCount = 0
GPGGA_LatDeg = 0
GPGGA_LonDeg = 0
Latitude = ''
Longitude =''
Heading=''
ip = '192.168.127.252'
port = int(9999)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    

# deg 변환 함수 (bae작성 코드)    
def LatLonTodegree(a):
        a = str(a)
        ddmm = int(float(a)) # 정수
        degree = int(ddmm/100)
        minute = (float(a)-(degree*100))/60
        ret = degree + minute
        return_data = str(ret)
        return return_data    

while True:
    sock.connect((ip,port))

    if ser.readable():
        res = ser.readline()
        data = (res.decode('utf-8'))
        gpsSampleTmp = data.split(",")
        if gpsSampleTmp[MessageID] == "$GPGGA" :
            Latitude  = gpsSampleTmp[2]
            Longitude = gpsSampleTmp[4]
            deg_lat = LatLonTodegree(Latitude)
            deg_lon = LatLonTodegree(Longitude)
            sendDeg_lan = deg_lat[0:6]
            sendDeg_lon = deg_lon[0:6]
            print('deg_lat',sendDeg_lan)
            print('deg_lon',deg_lon)
            
            send_L = 'L' +','+ sendDeg_lan +','
            send_L += sendDeg_lon + ','

            print('send_La',send_L)
            sendData_L = bytes(send_L,'utf-8')
            sock.sendto(sendData_L, (ip,port))
                 
        elif gpsSampleTmp[MessageID] == "$GPHDT" :
            Heading = gpsSampleTmp[1] 
            send_H = 'H' +','+ Heading + ','
            print('send_H',send_H)
            sendData_H = bytes(send_H,'utf-8')
            sock.sendto(sendData_H, (ip,port))
 
