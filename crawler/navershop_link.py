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
driver = webdriver.Chrome(config.get('SELENIUM', 'chromedriver'))
driver.implicitly_wait(5)

def open_navershoppage():
    # 네이버 쇼핑 접속 접속
    driver.get('https://shopping.naver.com/')
    time.sleep(3)

def get_items_form_csv(filepath):
    csv_df = pd.read_csv(filepath)
    return ['{},{}'.format(csv_df['manufacture'][i], csv_df['name'][i]) for i in range(csv_df['name'].count())]

def search(item):
    # 제품 검색
    driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(item)
    driver.find_element_by_xpath('//*[@id="autocompleteWrapper"]/input[1]').send_keys(Keys.ENTER)
    print(item)
    time.sleep(2)

def page_wait(id):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id"))
        )
    finally:
        pass

if __name__ == "__main__":
    today = date.today()
    input_filename = 'sample_db.csv'
    items = get_items_form_csv(input_filename)
    with open('./output/sample_link_db-{}.csv'.format(today.strftime("%Y%m%d")), 'w') as output:
        output.write('manufacture,name,link')
        for item in items:
            open_navershoppage()
            search(item.replace(',',' '))
            # page_wait('info')
            time.sleep(5)
            link = driver.current_url
            print(link)
            output.write('\n{item},{link}'.format(item=item, link=link))
            time.sleep(random.randrange(2,4))
    
    driver.close()
    
