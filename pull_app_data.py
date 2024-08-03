import requests
import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app_url = "https://tumi.esn.world/graphql?query="

full_members_query = "{users(statusList:[FULL]){fullName firstName lastName email}}"
trial_members_query = "{users(statusList:[TRIAL]){fullName firstName lastName email}}"
alumni_query = "{users(statusList:[ALUMNI]){fullName firstName lastName email}}"
helper_query = "{users(statusList:[HELPER]){fullName firstName lastName email}}"

class AppDataFetcher:
    def __init__(self):
        self.username = None
        self.scraper = TokenScraper()

    def start(self):
        full_members_df = self.fetch_from_app(full_members_query)
        trial_members_df = self.fetch_from_app(trial_members_query)
        all_members_df = pd.concat([full_members_df, trial_members_df])
        alumni_df = self.fetch_from_app(alumni_query)
        helpers_df = self.fetch_from_app(helper_query)  
        
        full_members_df.to_csv('full_members.csv', index=False)
        trial_members_df.to_csv('trial_members.csv', index=False)
        all_members_df.to_csv('all_members.csv', index=False)
        alumni_df.to_csv('alumni.csv', index=False)
        helpers_df.to_csv('helpers.csv', index=False)
        
        #time.sleep(2* 60 * 60)
    
    # returns users in the form of {email: email, fullName: fullName, firstName: firstName, lastName: lastName}
    def fetch_from_app(self, query):
        res = requests.get(app_url + query, headers = {"Authorization": self.scraper.bearer, "Origin": "https://tumi.esn.world"})      
        users = res.json()["data"]["users"]
        df = pd.json_normalize(users)
        
        df = df.rename(columns={"fullName": "Kontaktperson", "firstName": "Vorname", "lastName": "Nachname", "email": "E-Mail"})
        df["Unternehmen"] = ""
        df["Telefon (geschäftlich)"] = ""
        df["Mobiltelefon"] = ""
        df["Faxnummer"] = ""
        df["Titel"] = ""
        df["Website"] = ""
        df["Straße und Hausnummer"] = ""
        df["Straße und Hausnummer 2"] = ""
        df["Ort"] = ""
        df["Bundesland"] = ""
        df["Postleitzahl"] = ""
        df["Land oder Region"] = ""
        
        return df
        
    
class TokenScraper:
    def __init__(self):
        
        with open('/home/justin/Dokumente/Projekte/tumi-mailinglists/credentials.txt', 'r') as file:
            lines = file.readlines()
            self.esn_login = lines[0].split()[0]
            self.esn_password = lines[0].split()[1]
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.updateBearer()
        
    def updateBearer(self):        
        self.driver.get("https://tumi.esn.world/events")
        
        while self.loading():
            time.sleep(1)
        
        elements = self.driver.find_elements(By.TAG_NAME, "span")
        for element in elements:
            if element.text == "Log in":
                self.loginESN()
                break
        
        bearer_string = self.driver.execute_script("return window.localStorage.getItem(\"@@auth0spajs@@::9HrqRBDGhlb6P3NsYKmTbTOVGTv5ZgG8::esn.events::openid profile email\");")
        self.bearer = "Bearer " + json.loads(bearer_string)["body"]["access_token"]
        
    def loginESN(self):
        self.driver.get("https://tumi.esn.world/profile")
        
        while self.loading():
            time.sleep(1)
        element = self.driver.find_element(By.ID, "username")
        element.send_keys(self.esn_login)
        
        while self.loading():
            time.sleep(1)
        elements = self.driver.find_elements(By.NAME, "action")
        for element in elements:
            if element.get_attribute("type") == "submit":
                element.click()
                break
        
        while self.loading():
            time.sleep(1)
        
        element = self.driver.find_element(By.ID, "password")
        element.send_keys(self.esn_password)
        
        
        while self.loading():
            time.sleep(1)
        elements = self.driver.find_elements(By.NAME, "action")
        for element in elements:
            if element.get_attribute("type") == "submit":
                element.click()
                break
        
        while self.loading():
            time.sleep(1)
        
    def loading(self):
        elements = self.driver.find_elements(By.TAG_NAME, "img")
        for element in elements:            
            if element.get_attribute("alt") == "ESN Star" and "/assets/logos/star-white.svg" not in element.get_attribute("src"):
                return True
            
        return False

bot = AppDataFetcher()   
bot.start()
