# -*- coding: utf-8 -*-
import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


# config
config = configparser.ConfigParser()
config.read('config.ini')

# webdriver로 chrome 실행
driver = webdriver.Chrome(config.get('Selenium', 'chromedriver'))
driver.implicitly_wait(5)

def openKakaoMapPage():
    # 카카오맵 접속
    driver.get('https://map.kakao.com')
    time.sleep(3)

def clickFindPathButton():
    # '길찾기' 버튼 클릭
    find_load_button = driver.find_elements_by_id('search.tab2')[0]
    driver.execute_script("arguments[0].click();", find_load_button)
    time.sleep(1)

def searchPath(start_point, destination):
    # 경로 검색
    driver.find_elements_by_id('info.route.waypointSuggest.input0')[0].send_keys(start_point)
    driver.find_elements_by_id('info.route.waypointSuggest.input0')[0].send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_elements_by_id('info.route.waypointSuggest.input1')[0].send_keys(destination)
    driver.find_elements_by_id('info.route.waypointSuggest.input1')[0].send_keys(Keys.ENTER)
    time.sleep(1)
    driver.find_elements_by_id('dimmedLayer')[0].click()
    time.sleep(1)
    driver.find_elements_by_id('cartab')[0].click()
    time.sleep(1)

def printTollFee(soup):
    toll_fee = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > div > span.toll > span')[0].text
    print('통행료 : {0}원'.format(toll_fee))

def printTaxiFee(soup):
    taxi_fee = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > div > span.taxi > span')[0].text
    print('택시비 : {0}원'.format(taxi_fee))
    
def printOilFee(soup):
    oil_fee = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > div > span.oil > span')[0].text
    print('주유비 : {0}원'.format(oil_fee))

def printDistance(soup):
    distance = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > p > span.distance > span.num')[0].text
    distance_unit = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > p > span.distance > span.text')[0].text
    print('거리 : {0}{1}'.format(distance, distance_unit))

def printSpendTime(soup):
    spendtime = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > p > span.time > span.num')
    spendtime_unit = soup.select('#info\.flagsearch > div.CarRouteResultView > ul > li > div.summary > div > div.contents > p > span.time > span.text')
    result = '시간 : '
    for i in range(len(spendtime)): result += spendtime[i].text+spendtime_unit[i].text+' '
    print(result)

def main():
    openKakaoMapPage()
    clickFindPathButton()

    searchPath("서울역", "충남대학교")

    # 통행료, 택시비, 주유비, 거리, 시간 구해오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    printTollFee(soup)
    printTaxiFee(soup)
    printOilFee(soup)
    printDistance(soup)
    printSpendTime(soup)
    
    driver.close()

if __name__ == "__main__":
    main()

