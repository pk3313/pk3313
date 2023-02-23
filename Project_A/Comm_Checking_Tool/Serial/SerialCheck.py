import serial.tools.list_ports # serial port 를 검색하기

for comPort in serial.tools.list_ports.comports(): # 사용할수 있는 Serial Device 리스트
    print(comPort)