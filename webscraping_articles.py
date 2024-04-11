from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

def get_articles():

    obj_list = []
    obj={}

    target_url = "https://www.nasdaq.com/market-activity/stocks/aapl/news-headlines"

    driver=webdriver.Chrome()

    driver.get(target_url)

    for page in range(1, 1251):
        pagination_buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pagination__page")))
        
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
                    obj["date"] = (datetime.today() - timedelta(hours=int(date))).strftime('%Y-%m-%d')
                elif "day ago" in date:
                    date = date.replace(" day ago", "")
                    obj["date"] = (datetime.today() - timedelta(days=int(date))).strftime('%Y-%m-%d')
                elif "days ago" in date:
                    date = date.replace(" days ago", "")
                    obj["date"] = (datetime.today() - timedelta(days=int(date))).strftime('%Y-%m-%d')
                else:
                    date_object = datetime.strptime(date, "%b %d, %Y")
                    obj["date"] = date_object.strftime('%Y-%m-%d')
                    

                obj["title"] = headline.find("p", class_="quote-news-headlines__item-title").text.strip()
                obj_list.append(obj)
                print(obj)
            except AttributeError:
                obj["title"] = None

        print(f"Scraping page {page}/1250")

    driver.quit()

    keys = obj_list[0].keys()
    with open('articles.csv', 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(obj_list)

get_articles()