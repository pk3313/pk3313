

class repeatControl():
    repeatControl = False
    
class data():
    data = [0,0,0] # GPS 데이터를 화면 출력하기 위한 리스트
     
    ####################
    # FOG로 전송하기 위해 변수에 담음 (str -> float 변환 위해)
    # 버튼을 클릭할 찰나의 데이터를 변수에 담기 위함
    heading = 0.1
    latitude =0.1
    longitude =0.1
    ####################
    standard_deviation = []*3 # 표준 편차
    
    # GPS 데이터를 화면에 출력하기 위한 변수 
    LatitudeData =''
    LongitudeData ='' 
    HeadingData =''
    
    # 소켓 데이터를 반복적으로 받아오기 위해      
    rotate = True