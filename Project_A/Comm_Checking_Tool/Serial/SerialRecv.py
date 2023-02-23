import serial
import time

BufferSize = 100

seri = serial.Serial(port= "COM17",
                     baudrate= 57600,
                     bytesize= 8,
                     timeout= 1)


breakCount = 0
while breakCount < 100:
    
    # data = seri.read()
    data = seri.readline() # 보내는쪽이 "\n"을 붙여서 보내는 경우
    
    print("RecvData : {}".format(data))
    breakCount += 1
    time.sleep(0.1)

seri.close()


##======================== 참고용 코드 ========================##
# with serial.Serial("COM4", 57600, bytesize= 8, timeout=1) as ser:
#     x = ser.read()          # read one byte
#     s = ser.read(10)        # read up to ten bytes (timeout)
#     line = ser.readline()   # read a '\n' terminated line