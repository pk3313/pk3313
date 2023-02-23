import serial
import time

BufferSize = 100

seri = serial.Serial(port= "COM18",
                     baudrate= 57600,
                     bytesize= 8,
                     timeout= 1)

data = "Serial Test..."

breakCount = 0
while breakCount < 100:
    # seri.write(bytes(data.encode())) # encode 대신 bytes를 사용한 경우
    seri.write(data.encode())
    print("SendData : {}".format(data.encode()))
    time.sleep(0.1)
    recv = seri.read(BufferSize) # read up to BufferSize bytes
    print("RecvData : {}".format(recv.decode()))
    breakCount += 1
    time.sleep(0.1)

seri.close()