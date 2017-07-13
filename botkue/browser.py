import sqlite3
from os.path import expanduser as euser
from time import sleep
from bs4 import BeautifulSoup as bs
from subprocess import Popen
from openpyxl import load_workbook

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

ranks = ('Not ranked', 'Recruit', 'Corporal', 'Sergeant', 'Lieutenant', 'Captain', 'General')

urls = ('https://docs.google.com/spreadsheets/d/1C3Hz78SaDe2F0w0NRfmbEWS_lUjtko6Lv4P4-bpNQzI',
	'http://runescape.com/companion/comapp.ws'
)
home = euser('~')

conn = sqlite3.connect('%s/.botkuerc/dwd.sqlite' % (home))
c = conn.cursor()

usern = ''
passw = ''

xp_login_gl = '//*[@id="gb_70"]'
xp_usern_gl = ('//*[@id="identifierId"]',
	 '//*[@id="identifierNext"]/content'
)
xp_passw_gl = ('//*[@id="password"]/div[1]/div/div[1]/input',
	 '//*[@id="passwordNext"]/content'
)
xp_dnlss_gl = ('//*[@id="docs-file-menu"]',
	'//*[@id=":5t"]/div/span[1]',
	'//html/body/div[46]/div[1]'
)
xp_imprt_gl = ('//*[@id="docs-file-menu"]',
	'picker-frame',
	'//*[@id=":8"]/div',
	'//*[@id=":z"]/div',
	'//*[@id="destinationOptions"]/div[3]/div',
	'import'
)

xp_login_rs = 'icon-login'
xp_usern_rs = '//*[@id="username"]'
xp_passw_rs = '//*[@id="password"]'
xp_dnlss_rs = ('//*[@id="modal"]/div/div/div/div[1]/a[1]', 
	'//*[@id="main-menu"]/div/nav/ul/li[4]/a',
	'//html/body/div[3]/div[1]/section/nav/ul/li[3]/a',
	'//html/body/div[3]/div[1]/section/footer/a[2]'
)

workbook = load_workbook('%s/.botkuerc/files/xlsx/ss_template.xlsx' % (home))

with open('%s/.botkuerc/files/data.html' % (home)) as fp:
	soup = bs(fp, 'lxml')

class browser(object):

	def __init__(self, usern, passw, url, f):
		self.driver = webdriver.Chrome(executable_path='%s/.botkuerc/files/chromedriver' % (home))
		self.usern = usern
		self.passw = passw
		self.url = url
		self.f = f

	def login_google(self, login, xp_n, xp_nc, xp_p, xp_pc):
		self.driver.get(self.url)
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, login))).click()
		
		usern_login = self.driver.find_element(By.XPATH, xp_n)
		usern_login.send_keys(self.usern)
		self.driver.find_element(By.XPATH, xp_nc).click()

		passw_login = wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp_p)))
		passw_login.send_keys(self.passw)
		self.driver.find_element(By.XPATH, xp_pc).click()

	def login_rs(self, login, xp_n, xp_p):
		self.driver.get(self.url)
		sleep(3)
		Popen('%s/projects/botkue/botkue/do_block.sh' % (self.f), shell=True)
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.TAG_NAME, 'iframe')))
		self.driver.switch_to.frame(self.driver.find_element(By.TAG_NAME, 'iframe'))
		
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp_n)))
		usern_login = self.driver.find_element(By.XPATH, xp_n)
		usern_login.send_keys(self.usern)
		
		passw_login = self.driver.find_element(By.XPATH, xp_p)
		passw_login.send_keys(self.passw)

		self.driver.find_element(By.CLASS_NAME, login).click()

	def dl_rs(self, xp1, xp2, xp3, xp4):
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp1))).click()
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp2))).click()
		sleep(4)
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp3))).click()
		sleep(4)
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp4))).click()
		sleep(4)
		fi = open('%s/.botkuerc/files/data.html' % (self.f), 'w')
		fi.write(self.driver.page_source)
		fi.close()
		
		self.driver.close()

	def dl_ss(self, f_menu, dl_btn, f_sele):
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, f_menu))).click()	
		
		sleep(1)
		actions = ActionChains(self.driver)
		actions.send_keys('e').perform()

		sleep(1)
		actions.send_keys(u'\ue007').perform()

		sleep(1)
		Popen('mv %s/Downloads/*xlsx %s/.botkuerc/files/xlsx/ss_template.xlsx' % (self.f, self.f), shell=True)
		
	def im_ss(self, xp1, xp2, xp3, xp4, cn1, nm1):
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp1))).click()

		sleep(1)
		actions = ActionChains(self.driver)
		actions.send_keys('c').perform()

		sleep(1)
		self.driver.switch_to.frame(self.driver.find_element(By.CLASS_NAME, cn1))
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp2))).click()
		Popen('%s/projects/botkue/tests/file_select.sh' % (self.f), shell=True)

		sleep(1)
		wdw(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, xp4))).click()

		sleep(1)
		self.driver.find_element(By.NAME, nm1).click()

		sleep(10)
		self.driver.close()

class data_parse(object):
	
	def __init__(self, name, home):
		self.name = name
		self.home = home
		self.i = 6
		self.current_ranks = []
		self.updated_ranks = []


	def get_current_names_ranks(self):
		count = len(ranks)
		for nums in range(1, count + 1):
			c.execute("SELECT name, rank_id FROM member WHERE rank_id='%s'" % (count))
			for data in c.fetchall():
				if count in data[0:2]:
					self.current_ranks.append(data[0:2])
			count -= 1
	
	def database_insert_names_ranks(self):
		while self.i >= 0:
			for names in soup.find_all('div', attrs={'class': 'left'}):
				if names.get_text().replace('\n', '').endswith(self.name):
					if self.name == ranks[self.i]:
						remove_newline = names.get_text().replace('\n', '')
						fix_spaces = remove_newline.replace(u'\xa0', u' ')
						remove_rank_title = fix_spaces.replace(self.name, '')
						with_num = remove_rank_title, self.i + 1
						self.updated_ranks.append(with_num)
						c.execute("INSERT OR IGNORE INTO member (name, rank_id) VALUES('%s', '%s')" % (
							remove_rank_title, self.i + 1))
			self.i -= 1
		conn.commit()
		self.i = 6

	def update_names_ranks(self):
		for names in self.updated_ranks:
			if names not in self.current_ranks:
				c.execute("UPDATE member SET rank_id='%s' WHERE name='%s'" % (names[1], names[0]))
				conn.commit()

	def spreadsheet_insert_names_ranks(self, num):
		while self.i >= 0:
			c.execute("SELECT name, date_ranked FROM member WHERE rank_id='%s' ORDER BY name COLLATE NOCASE" % (self.i + 1))
		
			for names in c.fetchall():
				if self.i == 0:
					worksheet_active = workbook.get_sheet_by_name('Friends')
					num += 1
					worksheet_active['A%s' % (num + 1)] = names[0]
					worksheet_active['B%s' % (num + 1)] = names[1]
				else:
					worksheet_active = workbook.get_sheet_by_name('%ss' % (ranks[self.i]))
					num += 1
					worksheet_active['A%s' % (num + 1)] = names[0]
					worksheet_active['B%s' % (num + 1)] = names[1]
			num = 0
			self.i -= 1
			workbook.save('%s/.botkuerc/files/xlsx/final.xlsx' % (self.home))

doit_rs = browser(usern, passw, urls[1], home)
doit_rs.login_rs(xp_login_rs, xp_usern_rs, xp_passw_rs)
doit_rs.dl_rs(xp_dnlss_rs[0], xp_dnlss_rs[1], xp_dnlss_rs[2], xp_dnlss_rs[3])

doit_google = browser(usern, passw, urls[0], home)
doit_google.login_google(xp_login_gl, xp_usern_gl[0], xp_usern_gl[1], xp_passw_gl[0], xp_passw_gl[1])
#doit_google.dl_ss(xp_dnlss_gl[0], xp_dnlss_gl[1], xp_dnlss_gl[2])

for each in ranks:
	start_data_parse = data_parse(each, home)	
	start_data_parse.database_insert_names_ranks()
	start_data_parse.get_current_names_ranks()
	start_data_parse.update_names_ranks()
start_data_parse.spreadsheet_insert_names_ranks(0)

doit_google.im_ss(xp_imprt_gl[0], xp_imprt_gl[2], xp_imprt_gl[3], xp_imprt_gl[4], xp_imprt_gl[1], xp_imprt_gl[5])
