from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
#może stąd jeszcze https://markets.businessinsider.com/news/aapl-stock?p=398&

def get_nasdaq_articles():

    obj_list = []
    obj={}

    target_url = "https://www.nasdaq.com/market-activity/stocks/aapl/news-headlines"

    driver=webdriver.Chrome()

    driver.get(target_url)

    for page in range(1, 1251):      
        next_page_button = driver.find_element(By.CLASS_NAME, "pagination__next")
        driver.execute_script("arguments[0].click();", next_page_button)
        

        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        headlines = page_soup.find_all("li", class_="quote-news-headlines__item")
        
        for headline in headlines:
            obj = {}
            try:
                date = headline.find("span", class_="quote-news-headlines__date").text.strip()
                if "hours ago" in date:
                    date = date.replace(" hours ago", "")
                    obj["date"] = (datetime.now() - timedelta(hours=int(date))).strftime('%Y-%m-%d')
                elif "day ago" in date:
                    date = date.replace(" day ago", "")
                    obj["date"] = (datetime.now() - timedelta(days=int(date))).strftime('%Y-%m-%d')
                elif "days ago" in date:
                    date = date.replace(" days ago", "")
                    obj["date"] = (datetime.now() - timedelta(days=int(date))).strftime('%Y-%m-%d')
                else:
                    date_object = datetime.strptime(date, "%b %d, %Y")
                    obj["date"] = date_object.strftime('%Y-%m-%d')
                    

                obj["title"] = headline.find("p", class_="quote-news-headlines__item-title").text.strip()
                obj_list.append(obj)
                # print(obj)
            except AttributeError:
                print("AttributeError")

        # print(f"Scraping page {page}/1250")

    driver.quit()

    return obj_list

def get_businessInsider_articles():
    
    obj_list = []
    obj={}

    driver=webdriver.Chrome()

    for page in range(1, 399):
        target_url = f"https://markets.businessinsider.com/news/aapl-stock?p={page}"
        driver.get(target_url)

        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        headlines = page_soup.find_all("div", class_="latest-news__story")
        
        for headline in headlines:
            obj = {}
            try:
                date = headline.find("time", class_="latest-news__date").text.strip()
                if 'h' in date:
                    hours = int(date.replace('h', ''))
                    date = datetime.now() - timedelta(hours=hours)
                else:
                    days = int((date.replace('d', '')).replace(',', ''))
                    date = datetime.now() - timedelta(days=days)

                obj["date"] = date.strftime('%Y-%m-%d')
                    
                obj["title"] = headline.find("a", class_="news-link").text.strip()
                obj_list.append(obj)
                # print(obj)
            except AttributeError:
                print("AttributeError")

        # print(f"Scraping page {page}/388")

    driver.quit()

    return obj_list

def encode_dict(d):
    encoded_dict = {}
    for key, value in d.items():
        if isinstance(value, str):
            encoded_dict[key] = value.encode('utf-8', errors='ignore').decode('utf-8')
        else:
            encoded_dict[key] = value
    return encoded_dict
    

obj_list = get_businessInsider_articles() + get_nasdaq_articles()
obj_list = [dict(t) for t in {tuple(d.items()) for d in obj_list}]
obj_list = [encode_dict(d) for d in obj_list]

keys = obj_list[0].keys()
with open('articles.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(obj_list)