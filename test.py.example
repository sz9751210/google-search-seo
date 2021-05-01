import pandas as pd
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
# 判斷用網址
check_list = ["https://www.fatfoodieshop.com.tw/%E8%82%89%E9%AC%86%E9%A4%85"]
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
        try:
            # 透過try/catch等待網頁爬取到所有搜尋結果
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "g"))
            )

        except Exception as e:
            print(e)
            driver.quit()
        # 把搜尋結果放入list
        searchResults = driver.find_elements_by_class_name("g")
        for result in searchResults:
            count = count +1
            sum = count
            element = result.find_element_by_css_selector("a")
            link = element.get_attribute("href")
            header = result.find_element_by_css_selector("h3").text
            now = datetime.date.today().strftime("%d-%m-%Y")
            if link in check_list:
                pageInfo.append({ "公司":company, "搜尋國家":country, "關鍵字": keyword, "排名": count, "網址": link,"爬取時間": now})
        return pageInfo,sum


    # 爬取頁面
    numPages = 5
    
    # 先爬取首頁
    page_info, rank = scrape(0)
    sum == rank
    infoAll.extend(page_info)
    
    for i in range(0, numPages - 1):
        sleep(3) #睡覺
        nextButton = driver.find_element_by_link_text("下一頁")
        nextButton.click()
        page_info, rank = scrape(sum)
        sum = sum + rank
        infoAll.extend(page_info)
        
    driver.close()
# 存成excel
df = pd.DataFrame(infoAll)
df.to_csv('./'+ company +'.csv', index=False)
print("Done! 檔案已存入當前目錄")