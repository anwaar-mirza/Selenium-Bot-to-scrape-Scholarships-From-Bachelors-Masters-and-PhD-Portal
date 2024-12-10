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
class StudyPortal:

    data = {}

    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.action = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 20)

    def refresh_driver(self):
        self.driver.refresh()

    def land_required_page(self, page_url):
        self.driver.get(page_url)
        self.driver.implicitly_wait(5)

    def get_title(self):
        try:
            name = self.driver.find_element(By.XPATH, '//h1[@class="ScholarshipName"]').text
            self.driver.implicitly_wait(5)
            self.data['scholarship_title'] = name
        except:
            self.data['scholarship_title'] = "N/A"

    def get_scholarship_provider(self):
        try:
            provider = self.driver.find_element(By.XPATH, '//a[@class="ProviderName"]').text
            self.driver.implicitly_wait(5)
            self.data['scholarship_provider'] = provider
        except:
            try:
                provider = self.driver.find_element(By.XPATH, '//span[@class="ProviderName"]').text
                self.driver.implicitly_wait(5)
                self.data['scholarship_provider'] = provider
            except:
                self.data['scholarship_provider'] = "N/A"

    def get_scholarship_provider_about(self):
        try:
            sch_pro_about = self.driver.find_element(By.XPATH, '//section[@id="AboutSection"]/p[2]').text
            self.driver.implicitly_wait(5)
            self.data['about_scholarship_provider'] = sch_pro_about
        except:
            self.data['about_scholarship_provider'] = "N/A"

    def get_scholarship_type(self):
        try:
            sch_type = self.driver.find_element(By.XPATH, '//div[h3[text() = " Scholarship type "]]/div/span').text
            self.driver.implicitly_wait(5)
            self.data['scholarship_type'] = sch_type
        except:
            self.data['scholarship_type'] = "N/A"

    def get_no_of_scholarship_to_award(self):
        try:
            no_of_sch = self.driver.find_element(By.XPATH, '//div[h3[text() = "Number of scholarships to award"]]/div/span').text
            self.driver.implicitly_wait(5)
            self.data['no_of_sch_to_award'] = no_of_sch
        except:
            self.data['no_of_sch_to_award'] = "N/A"

    def get_grant(self):
        try:
            grant = self.driver.find_element(By.XPATH, '//div[h3[text() = "Grant"]]/div/span').text
            self.driver.implicitly_wait(5)
            self.data['grant'] = grant
        except:
            self.data['grant'] = "N/A"

    def get_scholarship_coverage(self):
        try:
            cover = self.driver.find_element(By.XPATH, '//div[@class="ArticleSection" and h3[text() = "Scholarship coverage"]]/ul').text
            self.driver.implicitly_wait(5)
            self.data['scholarship_coverage'] = cover.replace("\n", ", ")
        except:
            self.data['scholarship_coverage'] = "N/A"

    def get_scholarship_description(self):
        try:
            descript = self.driver.find_element(By.XPATH, '//article[h2[text() = "Description"]]').text
            self.driver.implicitly_wait(5)
            self.data['scholarship_descript'] = descript
        except:
            self.data['scholarship_descript'] = "N/A"

    def get_benefits(self):
        try:
            benefits = self.driver.find_element(By.XPATH, '//article[h2[text() = "Benefits"]]').text
            self.driver.implicitly_wait(5)
            self.data['benefits'] = benefits
        except:
            self.data['benefits'] = "N/A"

    def get_deadline(self):
        try:
            deadline = self.driver.find_element(By.XPATH, '//div[div[text() = " Application deadline "]]/div[1]').text
            self.driver.implicitly_wait(5)
            self.data['Application Deadline'] = deadline
        except:
            self.data['Application Deadline'] = "N/A"

    def call_overview_page(self):
        self.get_title()
        self.get_scholarship_provider()
        self.get_scholarship_provider_about()
        self.get_scholarship_type()
        self.get_no_of_scholarship_to_award()
        self.get_grant()
        self.get_deadline()
        self.get_scholarship_coverage()
        self.get_scholarship_description()
        self.get_benefits()

    def click_eligibility(self):
        try:
            click_now = self.driver.find_element(By.XPATH, '//button[text() = " Eligibility "]')
            self.driver.implicitly_wait(5)
            self.driver.execute_script('arguments[0].click();', click_now)
            time.sleep(2.5)
        except:
            print("Failed to Click Eligibility Button.......")

    def get_eligibility(self):
        try:
            eligibility = self.driver.find_element(By.XPATH, '//article[h2[text() = "Eligibility"]]/ul').text
            self.driver.implicitly_wait(5)
            self.data['eligibility'] = eligibility
        except:
            self.data['eligibility'] = "N/A"

    def get_descipline(self):
        try:
            des = self.driver.find_element(By.XPATH, '//div[@data-show-popup="DisciplinePopup"]')
            self.driver.implicitly_wait(5)
            self.action.click(des).perform()
            time.sleep(2)
            data = self.driver.find_element(By.XPATH, '//div[@id="DisciplinePopup"]/aside/ul').text
            self.driver.implicitly_wait(15)
            self.data['discipline'] = data.replace('\n', ', ')
            try:
                cross = self.driver.find_element(By.XPATH, '//button[@class="CloseButton"]')
                self.driver.implicitly_wait(5)
                self.action.click(cross).perform()
                time.sleep(1)
            except:
                print("Discipline not cross")
        except:
            try:
                descipline = self.driver.find_element(By.XPATH, '//div[h3[text() = "Disciplines"]]/div').text
                self.driver.implicitly_wait(5)
                self.data['discipline'] = descipline
            except:
                self.data['discipline'] = "N/A"

    def get_location(self):
        try:
            loc = self.driver.find_element(By.XPATH, '//div[@class="ItemBlock RequirementsItemBlock ClickableBlock js-showMoreAboutEligibilityField" and @data-show-popup="LocationPopup"]')
            self.driver.implicitly_wait(10)
            self.action.click(loc).perform()
            time.sleep(2)
            loc_list = self.driver.find_element(By.XPATH, '//div[@id="LocationPopup"]/aside/ul').text
            self.driver.implicitly_wait(5)
            self.data['location'] = loc_list.replace('\n', ', ')
            try:
                cross = self.driver.find_element(By.XPATH, '//button[@class="CloseButton"]')
                self.driver.implicitly_wait(5)
                self.action.click(cross).perform()
                time.sleep(1)

            except:
                print("Location not cross")
        except:
            try:
                loc = self.driver.find_element(By.XPATH, '//div[h3[text() = "Locations"]]/div/span').text
                self.driver.implicitly_wait(5)
                self.data['location'] = loc
            except:
                self.data['location'] = "N/A"

    def get_nationality(self):
        try:
            nat = self.driver.find_element(By.XPATH, '//div[@class="ItemBlock RequirementsItemBlock ClickableBlock js-showMoreAboutEligibilityField" and @data-show-popup="NationalityPopup"]')
            self.driver.implicitly_wait(10)
            self.action.click(nat).perform()
            time.sleep(1)
            nat_list = self.driver.find_element(By.XPATH, '//div[@id="NationalityPopup"]/aside/ul').text
            self.driver.implicitly_wait(10)
            self.data['nationality'] = nat_list.replace('\n', ', ')
            try:
                cross = self.driver.find_element(By.XPATH, '//button[@class="CloseButton"]')
                self.driver.implicitly_wait(5)
                self.action.click(cross).perform()
                time.sleep(1)
            except:
                print("Nationality not cross")
        except:
            try:
                loc = self.driver.find_element(By.XPATH, '//div[h3[text() = "Nationality"]]/div/span').text
                self.driver.implicitly_wait(5)
                self.data['nationality'] = loc
            except:
                self.data['nationality'] = "N/A"

    def get_study_experience(self):
        try:
            experience = self.driver.find_element(By.XPATH, '//div[h3[text() = " Study experience required "]]/div/span').text
            self.driver.implicitly_wait(5)
            self.data['study_experience'] = experience
        except:
            self.data['study_experience'] = "N/A"

    def scrape_email(web_url):
        response = requests.get(web_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, soup.text)
        return emails

    def get_provider_website_and_email(self):
        try:
            web = self.driver.find_element(By.XPATH, '//a[text() = " provider website"]').get_attribute('href')
            self.driver.implicitly_wait(5)
            self.data['provider_website'] = web
            try:
                mail = self.scrape_email(web)
                self.data['email'] = mail
            except:
                self.data['email'] = "N/A"
        except:
            self.data['provider_website'] = "N/A"
            self.data['email'] = "N/A"


    def call_eligibility_page(self):
        self.click_eligibility()
        self.get_eligibility()
        self.get_descipline()
        self.get_location()
        self.get_nationality()
        self.get_study_experience()
        self.get_provider_website_and_email()

    def show_data(self, cu, country, continent):
        self.data['country'] = country
        self.data['continent'] = continent
        self.data['current_url'] = cu
        for key, value in self.data.items():
            print(str(key)+": "+str(value))

        p = pd.DataFrame([self.data])
        p.to_csv(f"C:/PyProjects/study_portal/phd/{continent}/{country}.csv", mode='a',
                 header=not os.path.exists(f"C:/PyProjects/study_portal/phd/{continent}/{country}.csv"), index=False)
        p.to_csv(f"C:/PyProjects/study_portal/phd/phd1.csv", mode='a',
                 header=not os.path.exists(f"C:/PyProjects/study_portal/phd/phd1.csv"), index=False)


file_dict = {
    "africa": ["egypt", "south africa", "zambia"],
    "australia": ["australia"],

    #"america": ["usa", "canada"],
    "europe": [
        "estonia", "finland", "france", "germany", "greece", "ireland", "italy",
        "netherlands", "portugal", "spain", "sweden",
        "austria", "belgium", "denmark", "poland", "switzerland"],
    "asia": [
    "bangladesh", "china", "indonesia", "iran", "japan", "malaysia", "russia",
    "saudi arabia", "south korea", "thailand", "turkey", "uae", "hong kong", 'kyrgyzstan', "new zealand", "singapore"]
}
bot = StudyPortal()
bot.land_required_page('https://www.phdportal.com/')
time.sleep(100)
bot.refresh_driver()
for key, value in file_dict.items():
    for v in value:
        with open(f"C:/PyProjects/study_portal/phd/{key}/links/{v}.csv") as file:
            next(file)
            for f in file:
                try:
                    bot.land_required_page(f)
                    bot.call_overview_page()
                    bot.call_eligibility_page()
                    bot.show_data(f, v, key)
                except Exception as e:
                    print(e)
                    time.sleep(4000)