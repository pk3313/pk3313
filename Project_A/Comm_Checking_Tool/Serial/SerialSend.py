import serial
import time

BufferSize = 100

seri = serial.Serial(port= "COM18",
                     baudrate= 57600,
                     bytesize= 8,
                     timeout= 1)

data = "Serial Test..."
# data = "Serial Test...\n" # 받는 쪽이 readline이면 "\n" 필요

breakCount = 0
while breakCount < 100:
    # seri.write(bytes(data.encode())) # encode 대신 bytes를 사용한 경우
    seri.write(data.encode())
    print("SendData : {}".format(data.encode()))
    breakCount += 1
    time.sleep(0.1)

seri.close()