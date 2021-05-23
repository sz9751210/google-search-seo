import pandas as pd
import sqlite3
import selenium 
from selenium import webdriver
import time
import datetime
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

def scrape(count):

    # 把搜尋結果放入list
    searchResults = driver.find_elements_by_class_name("g")
    for result in searchResults:
        count = count +1
        sum = count
        element = result.find_element_by_css_selector("a")
        link = element.get_attribute("href")
        # header = result.find_element_by_css_selector("h3").text
        now = datetime.date.today().strftime("%Y-%m-%d")

        # 找到網址並確認資料庫是否存在
        if link == check_url:
            sql_check = "select url from url where url = '{}';".format(check_url)
            c.execute(sql_check)
            check = c.fetchone()

            # 確認url是否已存在,如果不存在就寫入url並直接寫入關鍵字
            if check is None:
                sql_url = "insert into url(url, company) values('{}','{}');".format(link, company )
                c.execute(sql_url)
                get_uid = "select id from url where url ='{}';".format(check_url)
                c.execute(get_uid)
                uid = c.fetchone()
                sql_keyword = "insert into '{}'(keyword, rank, date, uid) values('{}','{}','{}',{});".format(company,keyword, count, now, uid[0] )
                c.execute(sql_keyword)
                print("結果已儲存")
            else:
                get_uid = "select id from url where url ='{}';".format(check_url)
                c.execute(get_uid)
                uid = c.fetchone()
                sql_check_keyword = "select keyword from '{}' where keyword = '{}' and uid = {} and date = '{}';".format(company,keyword,uid[0],now)
                c.execute(sql_check_keyword)
                check_keyword = c.fetchone()

                # 確認關鍵字是否存在
                if check_keyword is None:
                    sql_keyword = "insert into '{}'(keyword, rank, date, uid) values('{}','{}','{}',{});".format(company,keyword, count, now, uid[0] )
                    c.execute(sql_keyword)
                    print("結果已儲存")
                else:
                    print("搜尋結果已存在")

            # get_test = "select keyword, rank, date from keyword where keyword ='{}' and (date between '2021-05-08' and '2021-05-09') ;".format(keyword)
            # c.execute(get_test)
            # test = c.fetchall()
            # for i in test:
            #     print("關鍵字: '{}' 排名: '{}' 時間: '{}'".format(i[0],i[1],i[2]))

            conn.commit()
                
            sql_show = "select keyword, rank, date from '{}' where keyword = '{}' and  date = '{}'".format(company,keyword,now)
            c.execute(sql_show)
            test = c.fetchall()
            for i in test:
                print("關鍵字: '{}' 排名: '{}' 時間: '{}'".format(i[0],i[1],i[2]))
            # pageInfo.append({ "公司":company, "搜尋國家":country, "關鍵字": keyword, "排名": count, "網址": link,"爬取時間": now})
            
    return sum



dbfile = "test.db"
conn = sqlite3.connect(dbfile)
c = conn.cursor()
# 判斷用網址
url_txt = open("url.txt","r",encoding = 'utf8')
check_url = url_txt.read()
url_txt.close()
# 存放所有資料
infoAll = []

# 公司名稱
company_txt = open("company.txt","r",encoding = 'utf8')
company = company_txt.read()
company_txt.close()

# 建立資料表
command = '''CREATE TABLE if not exists '{}' (
	"kid"	INTEGER NOT NULL,
	"keyword"	TEXT,
	"rank"	TEXT,
	"date"	TEXT,
	"uid"	INTEGER NOT NULL,
	PRIMARY KEY("kid" AUTOINCREMENT),
	FOREIGN KEY("uid") REFERENCES "url"("id")
);'''.format(company)
c.execute(command)
# 關鍵字
splitOn = ','
keywords = []
with open("keyword.txt",'r', encoding = 'utf8') as f: 
    keywords = f.read().split(splitOn)

count = 0
sum = 0

# create instance of webdriver
options = webdriver.ChromeOptions() 
options.add_argument('–log-level=3')
options.add_argument('-headless')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,service_log_path=os.devnull, executable_path=r'D:\test\chromedriver.exe')
url = "https://www.google.com"
driver.get(url)



for keyword in keywords:

    print("開始查詢關鍵字:" + keyword)

    # 找到google搜尋欄位
    searchBar = driver.find_element_by_name("q")
    
    # 放入關鍵字

    searchBar.send_keys(Keys.CONTROL, 'a')
    searchBar.send_keys(keyword)
    searchBar.send_keys("\n")




    # 爬取頁面
    numPages = 10
    
    # 先爬取首頁
    rank = scrape(0)
    sum == rank

    
    for i in range(0, numPages - 1):
        driver.implicitly_wait(3)
        nextButton = driver.find_element_by_link_text("下一頁")
        nextButton.click()
        rank = scrape(sum)
        sum = sum + rank

# 關閉瀏覽器
driver.close()
conn.close()