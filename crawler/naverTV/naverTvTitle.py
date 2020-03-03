# /usr/bin/python3.5.2
# naverTvTitle.py
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import configparser
import time

# config
config = configparser.ConfigParser()
config.read('config.ini')

# webdriver로 chrome 실행
driver = webdriver.Chrome(config.get('SELENIUM', 'chromedriver'))
driver.implicitly_wait(5)

# naverTV top100 페이지 접속
driver.get('https://tv.naver.com/r')

time.sleep(3)
# 비디오 추가 로드
'''
for i in range(3):
	driver.find_element_by_id('moreBtn').click()
	time.sleep(3)
'''

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
# 제목들을 리스트에 저장
titles = []
# top3 영상은 상단 박스에 따로 표시되어 있음
top3_titles = soup.select('a.box > div.info._top_ani_area > strong.tit > span')
for title in top3_titles:
    title_text = title.text.strip()
    titles.append(title_text)
    print(title_text)
# top97 영상은 아래에
top97_titles = soup.select('div.cds > div.cds_type > dl.cds_info > dt.title > a > tooltip')
for title in top97_titles:
    title_text = title.text.strip()
    titles.append(title_text)
    print(title_text)
# 제목 갯수 출력
print('title count:{0}'.format(len(titles)))
