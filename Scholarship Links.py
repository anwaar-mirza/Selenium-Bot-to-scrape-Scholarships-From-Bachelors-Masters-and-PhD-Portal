import pickle
import re
import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class StudyLinks:

    data = {}

    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.get('https://www.phdportal.com/')
        time.sleep(100)
        self.driver.refresh()
        time.sleep(3)
        
    def click_scholarships_and_get_links(self, continent, page_url, file_name_to_save):
        self.driver.get(page_url)
        time.sleep(2)
        body = self.driver.find_element(By.TAG_NAME, 'body')
        self.driver.implicitly_wait(5)
        for _ in range(0, 5):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        time.sleep(2)

        try:
            total_pages = self.driver.find_element(By.XPATH, '//p[@class="PageCountLabel"]').text.split(' of ')
            self.driver.implicitly_wait(15)
            print(total_pages[-1])
            for i in range(1, int(total_pages[-1])+1):
                self.driver.get(page_url+f"?page={str(i)}")
                time.sleep(1)
                listing_links = self.driver.find_elements(By.XPATH, '//a[@class="ScholarshipCard"]')
                self.driver.implicitly_wait(5)
                for l in listing_links:
                    self.data['links'] = l.get_attribute('href')
                    p = pd.DataFrame([self.data])
                    p.to_csv(f"C:/PyProjects/study_portal/phd/{continent}/links/{country}.csv", mode='a', header=not os.path.exists(f"C:/PyProjects/study_portal/phd/{continent}/links/{country}.csv"), index=False)
        except Exception as e:
            print(e)
            print("Links Issue.....")


data_set = {
   "america": {
       "usa": "https://www.bachelorsportal.com/search/scholarships/phd/united-states",
       "canada": "https://www.bachelorsportal.com/search/scholarships/phd/canada",
   },
    "africa": {
        "egypt": "https://www.bachelorsportal.com/search/scholarships/phd/egypt",
        "south africa": "https://www.bachelorsportal.com/search/scholarships/phd/south-africa",
        "zambia": "https://www.bachelorsportal.com/search/scholarships/phd/zambia"
    },
    "australia": {
        "australia": "https://www.bachelorsportal.com/search/scholarships/phd/australia",
    },
    "asia": {
        "bangladesh": "https://www.bachelorsportal.com/search/scholarships/phd/bangladesh",
        "china": "https://www.bachelorsportal.com/search/scholarships/phd/china",
        "hong kong": "https://www.bachelorsportal.com/search/scholarships/phd/hong-kong",
        "indonesia": "https://www.bachelorsportal.com/search/scholarships/phd/indonesia",
        "iran": "https://www.bachelorsportal.com/search/scholarships/phd/iran",
        "japan": "https://www.bachelorsportal.com/search/scholarships/phd/japan",
        "kyrgyzstan": "https://www.bachelorsportal.com/search/scholarships/phd/kyrgyzstan",
        "malaysia": "https://www.bachelorsportal.com/search/scholarships/phd/malaysia",
        "new zealand": "https://www.bachelorsportal.com/search/scholarships/phd/new-zealand",
        "russia": "https://www.bachelorsportal.com/search/scholarships/phd/russia",
        "saudi arabia": "https://www.bachelorsportal.com/search/scholarships/phd/saudi-arabia",
        "singapore": "https://www.bachelorsportal.com/search/scholarships/phd/singapore",
        "south korea": "https://www.bachelorsportal.com/search/scholarships/phd/south-korea",
        "thailand": "https://www.bachelorsportal.com/search/scholarships/phd/thailand",
        "turkey": "https://www.bachelorsportal.com/search/scholarships/phd/turkey",
        "uae": "https://www.bachelorsportal.com/search/scholarships/phd/united-arab-emirates"
    },
    "europe": {
        "austria": "https://www.bachelorsportal.com/search/scholarships/phd/austria",
        "belgium": "https://www.bachelorsportal.com/search/scholarships/phd/belgium",
        "denmark": "https://www.bachelorsportal.com/search/scholarships/phd/denmark",
        "estonia": "https://www.bachelorsportal.com/search/scholarships/phd/estonia",
        "finland": "https://www.bachelorsportal.com/search/scholarships/phd/finland",
        "france": "https://www.bachelorsportal.com/search/scholarships/phd/france",
        "germany": "https://www.bachelorsportal.com/search/scholarships/phd/germany",
        "greece": "https://www.bachelorsportal.com/search/scholarships/phd/greece",
        "ireland": "https://www.bachelorsportal.com/search/scholarships/phd/ireland",
        "italy" : "https://www.bachelorsportal.com/search/scholarships/phd/italy",
        "netherlands": "https://www.bachelorsportal.com/search/scholarships/phd/netherlands",
        "poland": "https://www.bachelorsportal.com/search/scholarships/phd/poland",
        "portugal": "https://www.bachelorsportal.com/search/scholarships/phd/portugal",
        "spain": "https://www.bachelorsportal.com/search/scholarships/phd/spain",
        "sweden": "https://www.bachelorsportal.com/search/scholarships/phd/sweden",
        "switzerland": "https://www.bachelorsportal.com/search/scholarships/phd/switzerland",
        "uk": "https://www.bachelorsportal.com/search/scholarships/phd/united-kingdom"
    }

}

bot = StudyLinks()
for continent, country_dict in data_set.items():
    for country, links in country_dict.items():
        links = links.replace("https://www.bachelorsportal.com/", "https://www.phdportal.com/").replace("phd", "phd")
        bot.click_scholarships_and_get_links(continent, links, country)