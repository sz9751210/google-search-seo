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
import os

dbfile = "test.db"
conn = sqlite3.connect(dbfile)
c = conn.cursor()
# 判斷用網址
check_url = "https://mtmgseo.com/"
check_list = ["https://mtmgseo.com/"]
# 存放所有資料
infoAll = []
# 放關鍵字
company = "A公司"
country = "google.tw"
splitOn = ',' 
keywords = []
with open("keywords.txt",'r', encoding = 'utf8') as f: 
    keywords = f.read().split(splitOn) 
count = 0
sum = 0
for keyword in keywords:
    # create instance of webdriver
    options = webdriver.ChromeOptions() 
    options.add_argument('–log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options,service_log_path=os.devnull, executable_path=r'D:\test\chromedriver.exe')
    url = "https://www.google.com"
    driver.get(url)
    
    # 找到google搜尋欄位
    searchBar = driver.find_element_by_name("q")
    
    # 放入關鍵字
    searchBar.send_keys(keyword)
    searchBar.send_keys("\n")

    def scrape(count):
        pageInfo = []
        # try:
        #     # 透過try/catch等待網頁爬取到所有搜尋結果
        #     WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "g"))
        #     )

        # except Exception as e:
        #     print(e)
        #     driver.quit()
        # 把搜尋結果放入list
        searchResults = driver.find_elements_by_class_name("g")
        # print(len(searchResults))
        for result in searchResults:
            print(result)
            count = count +1
            sum = count
            # print(sum)
            element = result.find_element_by_css_selector("a")
            link = element.get_attribute("href")
            header = result.find_element_by_css_selector("h3").text
            now = datetime.date.today().strftime("%Y-%m-%d")
            print(header)
            if link in check_list:
                # sql_check = "select url from url where url = '';"
                print(1)
                sql_check = "select url from url where url = '{}';".format(check_url)
                print(sql_check)
                c.execute(sql_check)
                check = c.fetchone()
                # print(check)
                # 確認url是否已存在
                if check is None:
                    sql_url = "insert into url(url, company) values('{}','{}');".format(link, company )
                    c.execute(sql_url)
                    get_uid = "select id from url where url ='{}';".format(check_url)
                    c.execute(get_uid)
                    uid = c.fetchone()
                    sql_keyword = "insert into keyword(keyword, rank, date, uid) values('{}','{}','{}',{});".format(keyword, count, now, uid[0] )
                    c.execute(sql_keyword)
                    print("if")
                else:
                    print("else")
                    get_uid = "select id from url where url ='{}';".format(check_url)
                    c.execute(get_uid)
                    uid = c.fetchone()
                    sql_check_keyword = "select keyword from keyword where keyword = '{}' and uid = {} and date = '{}';".format(keyword,uid[0],now)
                    print(sql_check_keyword)
                    c.execute(sql_check_keyword)
                    check_keyword = c.fetchone()
                    print(check_keyword)
                    if check_keyword is None:
                        print("insert keyowrd")
                        print(now)
                        sql_keyword = "insert into keyword(keyword, rank, date, uid) values('{}','{}','{}',{});".format(keyword, count, now, uid[0] )
                        print(sql_keyword)
                        c.execute(sql_keyword)
                    else:
                        print("already exist")
                # get_test = "select keyword, rank, date from keyword where keyword ='{}' and (date between '2021-05-08' and '2021-05-09') ;".format(keyword)
                # c.execute(get_test)
                # test = c.fetchall()
                # for i in test:
                #     print("關鍵字: '{}' 排名: '{}' 時間: '{}'".format(i[0],i[1],i[2]))

                conn.commit()
                    
                # sql_show = "select * from url"
                # test = c.execute(sql_show)
                # print(test)
                # pageInfo.append({ "公司":company, "搜尋國家":country, "關鍵字": keyword, "排名": count, "網址": link,"爬取時間": now})
                # conn.close()
        return sum


    # 爬取頁面
    numPages = 5
    
    # 先爬取首頁
    rank = scrape(0)
    sum == rank
    # infoAll.extend(page_info)
    
    for i in range(0, numPages - 1):
        sleep(3) #睡覺
        nextButton = driver.find_element_by_link_text("下一頁")
        nextButton.click()
        rank = scrape(sum)
        sum = sum + rank
        # infoAll.extend(page_info)
        
    driver.close()
# 存成excel
# df = pd.DataFrame(infoAll)
# df.to_csv('./'+ company +'.csv', index=False)
# print("Done! 檔案已存入當前目錄")