# -*- coding: utf-8 -*-
import configparser
import time
import pandas as pd
import random
from datetime import date
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


# config
config = configparser.ConfigParser()
config.read('config.ini')

# webdriver로 chrome 실행
driver = webdriver.Chrome(config.get('Selenium', 'chromedriver'))
driver.implicitly_wait(5)

def open_navershoppage():
    # 네이버 쇼핑 접속 접속
    driver.get('https://shopping.naver.com/')
    time.sleep(3)

def get_items_form_csv(filepath):
    csv_df = pd.read_csv(filepath)
    return csv_df['title'].to_list()

def search(item):
    # 제품 검색
    driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(item)
    driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(Keys.ENTER)
    time.sleep(1)
    print(item)

def page_wait(id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id"))
        )
    finally:
        pass

def move_review_page():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 리뷰 페이지 링크 가져오기
    links = soup.find('div',{'class':'info'}).find('span',{'class':'etc'}).findAll('a', href=True)
    driver.get(links[0].attrs['href'])
    time.sleep(random.randrange(2,5))

def get_reviews():
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    stars = []
    for star in soup.select('#_review_list > li > div > div.avg_area > a > span.curr_avg > strong'):
        stars.append(star.text)
    reviews = []
    for review in soup.select('#_review_list > li > div > div.atc'):
        reviews.append(review.text)
    return (stars, reviews)

if __name__ == "__main__":
    today = date.today()
    input_filename = 'nshop-cream.csv'
    items = get_items_form_csv(input_filename)
    with open('./output/{}-{}.csv'.format(input_filename.split('.')[0], today.strftime("%Y%m%d")), 'w') as output:
        output.write('title,review,star')
        for item in items:
            open_navershoppage()
            search(item)
            # page_wait('info')
            time.sleep(3)
            move_review_page()
            stars, reviews = get_reviews()
            for i in range(len(stars)):
                output.write('\n{title},"{review}",{star}'.format(title=item, review=reviews[i], star=stars[i]))
            time.sleep(random.randrange(2,4))
    
    driver.close()
    
