# /usr/bin/python3.5.2
# dcinsideTitle.py
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import calendar
import configparser
import random
import time
import sys
import os

gallerys = ['drama', 'lol', 'starcraft', 'football', 'baseball_k', 'etc_program']

# import config data
config = configparser.ConfigParser()
config.read('config.ini')

class DCinsideParser:
	def __init__(self, gallery, today):
		self.gallery = gallery
		self.url = config.get('COMUNITY', 'dcinside')+\
			config.get('DC_GALL', gallery)+'&page='
		self.page = 1
		#self.today = datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
		self.today = today
	
	def setpage(self, number):
		self.page = number

	def isNumber(self, number):
		try:
			int(number)
			return True
		except ValueError:
			return False

	def getTitles(self, soup):
		result = list()
		numbers = soup.select('td.gall_num')
		titles = soup.select('td.gall_tit.ub-word > a')
		titles = [title for title in titles if title.text[0] != '[' and len(title.text) != 3]
		dates = soup.select('td.gall_date')
		
		for index in range(len(titles)):
			if dates[index].get('title') is None: continue
			if not self.isNumber(numbers[index].text): continue
			#posting_time = str(dates[index].get('title'))
			result.append(numbers[index].text+'\t'+titles[index].text+"\t"+str(dates[index].get('title')))
		return result
	
	def isYesterday(self, date):
		try:
			today = datetime.date(self.today)
			input_date = datetime.date(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))
		except ValueError as e:
			pass
		except IndexError as e:
			pass
		return (today-input_date) == timedelta(1)
	
	def getPageSoup(self):
		try:
			req = requests.get(self.url + str(self.page), timeout=5)
			html = req.text
			soup = BeautifulSoup(html, 'html.parser')
			print('current page:',self.page)
			return soup
		except requests.exceptions.Timeout as e:
			print(e)
			return self.getPageSoup()
	
	def changeNextPage(self):
		self.page += 1
		time.sleep(random.randint(4, 10))
		return self.getPageSoup()
	
	def getFirstYesterdayPageSoup(self):
		datas = self.getTitles(self.getPageSoup())
		while(not self.isYesterday(datas[-1].split("\t")[2])):
			datas = self.getTitles(self.changeNextPage())
		return datas
	
	def isOvertime(self, time):
		try:
			today = self.today.date()
			time_date = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').date()
		except ValueError as e:
			return False
		if (today-time_date) > timedelta(1): return True
		else: return False
	
	def getYesterdayDataToCSV(self):
		yesterday = datetime.strftime(self.today-timedelta(1), "%Y%m%d")
		datas = self.getFirstYesterdayPageSoup()
		csvfile = open(config.get('OUTPUT_FILE','dirpath')+\
			config.get('DC_GALL', self.gallery)+"/"+\
			yesterday+".csv", 'w')
		csvfile.write("posting_number\ttitle\tposting_time\n")
		overtime = False
		while(True):
			for data in datas:
				data_time = data.split('\t')[2]
				if self.isYesterday(data_time):
					csvfile.write(data+"\n")
				elif self.isOvertime(data_time):
					overtime = True
					break
			if overtime: break
			datas = self.getTitles(self.changeNextPage())
		csvfile.close()

def crawlingADayAll(gallery):
	date = datetime.today()
	current_page = 1
	dcparser = DCinsideParser(gallery, date)
	dcparser.setpage(current_page)
	print("*** Start "+gallery+" gall, "+str(date)+" ***")
	dcparser.getYesterdayDataToCSV()
	current_page = dcparser.page

def crawlingADay(gallery, date, startpage=1):
	dcparser = DCinsideParser(gallery, date)
	dcparser.setpage(startpage)
	print("*** Start "+gallery+" gall, "+str(date)+" ***")
	dcparser.getYesterdayDataToCSV()

if __name__ == '__main__':
	if len(sys.argv) == 1:
		# python3 dcinsideTitleParser.py - 오늘 기준 어제 데이터 전체
		for gallery in gallerys:
			crawlingADayAll(gallery)	
	elif len(sys.argv) == 2:
		# python3 dcinsideTitleParser.py [gallery]
		# 갤러리 선택
		crawlingADayAll(gallerys[int(sys.argv[1])])
	elif len(sys.argv) >= 3:
		date = datetime.today()-timedelta(int(sys.argv[2]))
		if len(sys.argv) == 3:
			# python3 dcinsideTitleParser.py [gallery] [date] 
			# 갤러리, 날짜 선택
			crawlingADay(gallerys[int(sys.argv[1])], date)
		elif len(sys.argv) == 4:
			# python3 dcinsideTitleParser.py [gallery] [date] [page]
			# 갤러리, 날짜, 페이지 선택
			crawlingADay(gallerys[int(sys.argv[1])], date, int(sys.argv[3]))
			
