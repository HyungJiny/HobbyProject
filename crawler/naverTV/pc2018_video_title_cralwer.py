# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# webdriver로 chrome 실행
driver = webdriver.Chrome('/Users/hyungjin/Downloads/chromedriver')
driver.implicitly_wait(3)

# naverTV 평창올림픽 비디오 페이지 접속
driver.get('http://tv.naver.com/b/pc2018/clips')

time.sleep(3)
# 비디오 추가 로드
'''
for i in range(3):
	driver.find_element_by_id('moreBtn').click()
	time.sleep(3)
'''

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
titles = soup.select('div.cds > div.cds_type > dl.cds_info > dt.title > a > tooltip')

for title in titles:
	print(title.text.strip())

print(len(titles))
