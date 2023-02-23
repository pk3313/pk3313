import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# 크롬드라이버 창 띄우지 않기 옵션
# options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('window-size=1980x1080')
options.add_argument('disable-gpu')
options.add_argument('--ignore-cetificate-errors')

#driver = webdriver.Chrome(executable_path='/home/peacek/Downloads/craw/data/chromedriver',chrome_options=options)
# 옵션 추가시 
driver = webdriver.Chrome(executable_path='C:/Users/평강/Desktop/크롤링/craw_Program/data/chromedriver',chrome_options=options)
# 옵션 없이 실행

#driver = webdriver.Chrome(executable_path='C:/Users/평강/Desktop/크롤링/craw_Program/data/chromedriver')
#driver = webdriver.Chrome(executable_path='/Users/pyeong-gang/Desktop/craw/data/chromedriver')
global keyword
keyword = '놀다'
verb =['벗다','하다','박다','사다','받다','주다','타다','먹다','접다','치다','잡다']
#driver.get('https://ko.dict.naver.com/#/search?range=example&query='+keyword)
driver.get('https://stdict.korean.go.kr/search/searchDetailWords.do')

ht = driver.page_source
soup = BeautifulSoup(ht, 'html.parser')
global url

# text 추출
def text(html):
	soup = BeautifulSoup(html, 'html.parser')
	driver.switch_to_window(driver.window_handles[1])
	driver.get_window_position(driver.window_handles[1])
	result = soup.select_one('body').get_text()
	if result !=None:
		print("saving file...")
		return result

def newtab(url):
	
	driver.execute_script('window.open("about:blank","_blank");')
	driver.get(url)
	print(url)
	html = driver.page_source

	return html

# Save text file
def Savefile(data):
	f=open('C:/Users/평강/Desktop/크롤링/craw_Program/text/'+keyword+'.txt','w')
	f.write(data)
	f.close()

href = driver.find_element_by_xpath('//*[@id="searchKeywords0"]').send_keys('먹다')
time.sleep(3)
driver.find_element_by_class_name('btn_search').click()
textt=[]
textt.append(driver.find_elements_by_class_name('dataLine'))
# print(textt.text)
for i in textt:
    for j in range(len(i)):
        print(i[j].text)
# for href in soup.find_all('input',{'class':'white2 searchKeywords icellp_100wp'}) :
#     #print(href)
#     url = href.find
#     print(url)
#     html = newtab(url)
#     re = text(html)
#     Savefile(re)
	


    
