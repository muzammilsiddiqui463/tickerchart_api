import json
import threading

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import requests
from ..host import HOST_URL
import os


class Scraper:
    
    def start_browser(self):


        # Define Chrome options
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH")

        # Initialize the WebDriver with Chrome options
        #
        self.driver = uc.Chrome(options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://www.tickerchart.net/app/en#")
        self.wait = WebDriverWait(self.driver, 25)
        self.actions = ActionChains(self.driver)

    def close_browser(self):
        self.driver.close()

    def login(self):
        # input("login?")
        wait = WebDriverWait(self.driver, 40)
        try:
            # try:
            #     wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="close-btn"]')))
            #     ad_closer = driver.find_element(By.XPATH, '//a[@class="close-btn"]')
            #     ad_closer.click()
            # except:
            #     pass
                
            wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="btn-small-text"]')))
            login = self.driver.find_element(By.XPATH, '//span[@class="btn-small-text"]/parent::a')
            self.actions.move_to_element(login).click().perform()
            wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="options"]//div[@class="action bold-font"]')))
            signin = self.driver.find_element(By.XPATH, '//div[@class="options"]//div[@class="action bold-font"]')
            signin.click()
            username = self.driver.find_element(By.XPATH, '//input[@name="username"]')
            username.clear()
            self.driver.save_screenshot("login.png")
            username.send_keys("jalmood", Keys.TAB)
            password = self.driver.find_element(By.XPATH, '//input[@name="password"]')
            password.clear()
            password.send_keys("saad", Keys.ENTER)
        except Exception as error:
            print(error)

    def table_data(self):
        wait = WebDriverWait(self.driver, 30)
        # self.driver.execute_script("document.body.style.zoom='25%'")
        actions = ActionChains(self.driver)
    
        time.sleep(4)
        # input("???")
        # self.driver.execute_script("document.body.style.zoom='25%'")
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@class="btn btn-purple btn-sm action-width"]')))
            elem = self.driver.find_element(By.XPATH, '//button[@class="btn btn-purple btn-sm action-width"]')
            actions.move_to_element(elem).click().perform()
            time.sleep(10)
        except Exception as e:
            print(e)
            print("not found")
            pass
        self.driver.refresh()
        time.sleep(4)
        self.driver.execute_script("document.body.style.zoom='25%'")
        self.driver.save_screenshot("img.png")
        wait = WebDriverWait(self.driver, 100)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@title="Symbol"]')))
    
        # self.driver.find_element(By.XPATH, '//div[@title="Symbol"]').click()
        history=[]
        while True:
            try:
                for i in range(0,2):
                    rows = self.driver.find_elements(By.XPATH, "//marketwatch//div[@class='grid-canvas']//div[contains(@class,'slick-row')]")
                    for row in rows:
                        try:
                            if row.text.split('\n') in history:
                                continue
                            else:
                                # print(row.text.split('\n'))
                                history.append(row.text.split('\n'))
                        except:
                            pass
                    #scroll

                    scroll = self.driver.find_element(By.XPATH, "//div[@class='slick-viewport']")
                    # current_scroll_position = self.driver.execute_script("return window.scrollY")
                    # self.driver.execute_script("window.scrollTo(0, window.scrollY + 2000)")
                    # new_scroll_position = self.driver.execute_script("return window.scrollY")
                    for _ in range(1):
                        actions.send_keys_to_element(scroll,Keys.PAGE_DOWN).perform()
                        # time.sleep(0.2)
            except:
                break

    
            # input()
            all_data = []
            for element in history:
                try:
                    # print(element)
                    # print(element)
                    # print(f"Symobol: {element[0]}, Close: {element[2]}, Open: {element[4]}, High: {element[5]}, Low: {element[6]}, Volume: {element[7]}")
                    data = {"Symbol": element[0], "close": element[2], "open": element[4], "high": element[5], "low": element[6], "volume": element[7]}
                    print(data)
                    all_data.append(data)
                    # add = requests.post("http://127.0.0.1:8000/data/", data=data).json()
                except:
                    pass
            def add_delete(all_data):
                delete_data = requests.delete(f"{HOST_URL}data/")
                add = requests.post(f"{HOST_URL}data/", json=all_data)
                print(add.json())
            s = threading.Thread(target=add_delete,args=(all_data,))
            s.start()

            for j in range(0, 3):
                actions.send_keys_to_element(scroll, Keys.PAGE_UP).perform()
            history = []

    def run_process(self):
        self.start_browser()
        self.login()
        self.table_data()

