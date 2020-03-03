import configparser
from selenium import webdriver

# config
config = configparser.ConfigParser()
config.read('config.ini')

def init_driver():
	# chromedriver version : 2.35
	driver = webdriver.Chrome(config.get('SELENIUM', 'chromedriver'))
	return driver

def read_gallery_main_page(pageCount):
	for i in range(1, pageCount):
		page_url = 'http://gall.dcinside.com/board/lists/?id=drama_new2&page='+str(pageCount)
		driver = init_driver()
		driver.get(page_url)

		tr_list = driver.find_elements_by_class_name('tb')

		for tr in tr_list:
			detail_page_url = tr.find_element_by_css_selector('a').get_attribute('href')
			print(detail_page_url)

			detail_page_html = read_detail_page(driver, detail_page_url)
			file_name = detail_page_url.split('?')[-1]
			with open(file_name+'.html', 'w') as output:
				output.write(detail_page_html)	

			print(detail_page_html)
			#break

	driver.quit()

def read_detail_page(driver, url):
	driver.get(url)
	page_source = driver.page_source
	return page_source

def parse_html(url, f):
	page_url = 'file://'+url
	url_open = urllib.request.urlopen(page_url)
	soup = BeautifulSoup(url_open, 'html.parser', from_encoding='utf-8')
	div_top_left = soup.find('div', attrs={'class':'w_top_left'})
	dl_list = div_top_left.findAll('dl')
	subject = dl_list[0].find('dd').text.strip()
	author = dl_list[1].find('dd').text.strip()
	div_top_right = soup.find('div', attrs={'class':'w_top_right'})
	ul = div_top_right.find('ul')
	li_list = ul.findAll('li')
	timestamp = li_list[0].text.strip()
	datetime_timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
	utc_timestamp = calendar.timegm(datetime_timestamp.timetuple())
	print(subject, author, utc_timestamp)
	f.write(subject+'\t'+author+'\t'+str(utc_timestamp)+'\n')

def main():
    read_gallery_main_page()


if __name__ == '__main__':
    main()
