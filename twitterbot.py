from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

PROMISED_DOWNLOAD_SPEED = 300
PROMISED_UPLOAD_SPEED = 300
CHROME_DRIVER_PATH = r"C:\Users\HSapi\development\chromedriver_win32\chromedriver.exe"
TWITTER_EMAIL = "fred_chiang@outlook.com"
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
TWITTER_URL = "https://twitter.com"
INTERNET_SPEED_URL = "https://www.speedtest.net/"


class InternetSpeedTwitterBot:
    def __init__(self):
        # initialize chrome selenium
        # load Twitter page and sign in
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(executable_path=CHROME_DRIVER_PATH), options=chrome_options)
        self.up = None
        self.down = None


    def get_internet_speed(self):
        self.driver.get(INTERNET_SPEED_URL)
        dynamic_div_index = 0
        try: #Locating "GO" link while managing Dynmaic DOM....
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]"))).click()
        except TimeoutException:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[4]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a/span[4]"))).click()
            dynamic_div_index = 4
        else:
            dynamic_div_index = 3
        print("analyzing internet speed")
        WebDriverWait(self.driver, 120).until(EC.url_changes(INTERNET_SPEED_URL))
        download_speed = self.driver.find_element(By.XPATH, f"/html/body/div[{dynamic_div_index}]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span").get_attribute("innerHTML")
        upload_speed = self.driver.find_element(By.XPATH, f"/html/body/div[{dynamic_div_index}]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span").text
        self.up = upload_speed
        self.down = download_speed
        print(f"speed:{self.down}down, {self.up}up")

    def tweet_at_provider(self):
        self.driver.get(TWITTER_URL)
        try: # Select for different XPath due to dynamic DOM
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/a"))).click()
        except TimeoutException:
            WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a"))).click()
        time.sleep(1)

        # Fill in username input
        username_input = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")))
        username_input.send_keys(TWITTER_EMAIL)
        username_input.send_keys(Keys.RETURN)

        # Twitter may request for phone number input
        try:
            phone_input = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")))
        except TimeoutException:
            pass
        else:
            phone_input.send_keys("6047606289")
            phone_input.send_keys(Keys.ENTER)
        # Fill in Password Input
        try:
            password_input = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
        except TimeoutException:
            password_input = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
        finally:
            password_input.send_keys(TWITTER_PASSWORD)
            password_input.send_keys(Keys.RETURN)

        #Tweet Message
        message = f"Hey Hey @TELUSsupport why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWNLOAD_SPEED}down/{PROMISED_UPLOAD_SPEED}up in Vancouver BC?"
        message_input = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div/div/div/div")))
        message_input.send_keys(message)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys(Keys.RETURN).key_up(Keys.CONTROL).perform()
