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

        #load old dataframes
        old_contacts_df = pd.read_csv('current_contacts.csv')

        old_full_members_df = pd.read_csv('full_members.csv')
        old_trial_members_df = pd.read_csv('trial_members.csv')
        old_all_members_df = pd.read_csv('all_members.csv')
        old_alumni_df = pd.read_csv('alumni.csv')
        old_helpers_df = pd.read_csv('helpers.csv')

        #create new dataframes
        full_members_df = self.fetch_from_app(full_members_query)
        trial_members_df = self.fetch_from_app(trial_members_query)
        all_members_df = pd.concat([full_members_df, trial_members_df])
        alumni_df = self.fetch_from_app(alumni_query)
        helpers_df = self.fetch_from_app(helper_query)  

        current_contacts_df = pd.concat([all_members_df, alumni_df, helpers_df])


        #compare changes in users and save changes to files
        added_contacts_df, deleted_contacts_df = self.diff_df(old_contacts_df, current_contacts_df)

        #remove unnecessary columns from distrolist dataframes
        full_members_df = full_members_df.filter(['email'])
        trial_members_df = trial_members_df.filter(['email'])
        all_members_df = all_members_df.filter(['email'])
        alumni_df = alumni_df.filter(['email'])
        helpers_df = helpers_df.filter(['email'])

        #compare changes in distrolists and save changes to files
        added_full_members_df, deleted_full_members_df = self.diff_df(old_full_members_df, full_members_df)
        added_trial_members_df, deleted_trial_members_df = self.diff_df(old_trial_members_df, trial_members_df)
        added_all_members_df, deleted_all_members_df = self.diff_df(old_all_members_df, all_members_df)
        added_alumni_df, deleted_alumni_df = self.diff_df(old_alumni_df, alumni_df)
        added_helpers_df, deleted_helpers_df = self.diff_df(old_helpers_df, helpers_df)

        #save everything to files
        current_contacts_df.to_csv('current_contacts.csv', index=False)
        added_contacts_df.to_csv('added_contacts.csv', index=False)
        deleted_contacts_df.to_csv('deleted_contacts.csv', index=False)

        full_members_df.to_csv('full_members.csv', index=False)
        trial_members_df.to_csv('trial_members.csv', index=False)
        all_members_df.to_csv('all_members.csv', index=False)
        alumni_df.to_csv('alumni.csv', index=False)
        helpers_df.to_csv('helpers.csv', index=False)

        added_full_members_df.to_csv('added_full_members.csv', index=False)
        added_trial_members_df.to_csv('added_trial_members.csv', index=False)
        added_all_members_df.to_csv('added_all_members.csv', index=False)
        added_alumni_df.to_csv('added_alumni.csv', index=False)
        added_helpers_df.to_csv('added_helpers.csv', index=False)

        deleted_full_members_df.to_csv('deleted_full_members.csv', index=False)
        deleted_trial_members_df.to_csv('deleted_trial_members.csv', index=False)
        deleted_all_members_df.to_csv('deleted_all_members.csv', index=False)
        deleted_alumni_df.to_csv('deleted_alumni.csv', index=False)
        deleted_helpers_df.to_csv('deleted_helpers.csv', index=False)
    
    # returns users in the form of {email: email, fullName: fullName, firstName: firstName, lastName: lastName}
    def fetch_from_app(self, query):
        res = requests.get(app_url + query, headers = {"Authorization": self.scraper.bearer, "Origin": "https://tumi.esn.world"})      
        users = res.json()["data"]["users"]
        df = pd.json_normalize(users)
        
        return df

    def diff_df(self, old_df, new_df):
        return new_df[~new_df['email'].isin(old_df['email'])], old_df[~old_df['email'].isin(new_df['email'])]
        
    
class TokenScraper:
    def __init__(self):
        
        with open('credentials.txt', 'r') as file:
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
