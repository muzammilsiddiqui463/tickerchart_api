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
from bs4 import BeautifulSoup
from ..host import HOST_URL
import pickle
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
        return False


    def close_browser(self):
        self.driver.close()

    def login(self):
        # input("login?")
        wait = WebDriverWait(self.driver, 40)
        print("login into account")
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
            time.sleep(5)
            print("Login DONE")
        except Exception as error:
            print(error)

    def setup(self):
        print("Setting up things...")
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
            # print(e)
            print("Popup Not Found")
            pass
        self.driver.refresh()
        time.sleep(4)
        self.driver.execute_script("document.body.style.zoom='25%'")
        self.driver.save_screenshot("img.png")
        wait = WebDriverWait(self.driver, 100)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@title="Symbol"]')))
        print("Setup Done")
    
        # self.driver.find_element(By.XPATH, '//div[@title="Symbol"]').click()
    def table_data(self):
        results = []
        def sub_process(row_data):
            try:
                col = row_data.select("div[class*='slick-cell']")
                temp = []
                for c in col:
                    temp.append(c.text)
                results.append(temp)
            except:
                pass


            # try:
            #     # if row_data.text.split('\n') in history:
            #     #     return
            #     # else:
            #     #     # print(row.text.split('\n'))
            #     results.append(row_data.split('\n'))
            #     return row_data.split('\n')
            # except Exception as e:
            #     print(e)
            #     pass
        wait = WebDriverWait(self.driver, 30)
        # self.driver.execute_script("document.body.style.zoom='25%'")
        actions = ActionChains(self.driver)

        print("Fetching Data")
        if True:
            try:
                last_length = 0
                self.driver.save_screenshot("table.png")
                scroll = self.driver.find_element(By.XPATH, "//div[@class='slick-viewport']")
                # Get the initial height of the scrollable element
                initial_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll)

                # Get the current height of the scrollable element
                # current_height = 999999
                # print(initial_height,'===intial heigh')
                # print(current_height,"==current height")
                for _ in range(0,2):
                    # initial_height = current_height
                    # rows = self.driver.find_elements(By.XPATH,
                    #                                  "//marketwatch//div[@class='grid-canvas']//div[contains(@class,'slick-row')]")
                    # print(len(rows))
                    threads  =[]
                    # Get the complete HTML content of the page
                    complete_html =self.driver.page_source

                    # Store the HTML content somewhere (you can save it to a file, a variable, or a database)
                    # Example: Save to a file
                    with open("page_content.html", "w", encoding="utf-8") as file:
                        file.write(complete_html)
                    # for r in range(0,len(rows)):
                    #     try:
                    #         row = self.driver.find_elements("xpath",f"//marketwatch//div[@class='grid-canvas']//div[contains(@class,'slick-row')]")[r].text
                    #         # print(row)
                    #     except:
                    #         continue
                    #
                    #     s = threading.Thread(target=sub_process,args=(row,))
                    #     threads.append(s)

                    # Load the saved HTML content
                    with open("page_content.html", "r", encoding="utf-8") as file:
                        saved_html = file.read()

                    # Parse the HTML using BeautifulSoup
                    soup = BeautifulSoup(saved_html, 'lxml')

                    # Find elements using your XPath expression
                    elements = soup.select("div.grid-canvas div[class*='slick-row']")
                    print(len(elements))
                    # Perform actions on the found elements
                    for element in elements:
                        row = element
                        s = threading.Thread(target=sub_process,args=(row,))
                        threads.append(s)



                        # try:
                        #     if row.text.split('\n') in history:
                        #         continue
                        #     else:
                        #         # print(row.text.split('\n'))
                        #         history.append(row.text.split('\n'))
                        # except:
                        #     pass
                    # scroll
                    for t in threads:
                        t.start()
                        # time.sleep(0.1)
                    for t in threads:
                        t.join()


                    # current_scroll_position = self.driver.execute_script("return window.scrollY")
                    # self.driver.execute_script("window.scrollTo(0, window.scrollY + 2000)")
                    # new_scroll_position = self.driver.execute_script("return window.scrollY")
                    actions.send_keys_to_element(scroll, Keys.PAGE_DOWN).perform()
                    time.sleep(1)
                    # current_height = self.driver.execute_script("return arguments[0].scrollHeight;", scroll)
            except Exception as e:
                print(e)
                return False

            # input()
            all_data = []
            print(len(results),"==results")
            for element in results:
                try:
                    # print(element)
                    # print(element)
                    # print(f"Symobol: {element[0]}, Close: {element[2]}, Open: {element[4]}, High: {element[5]}, Low: {element[6]}, Volume: {element[7]}")
                    data = {"Symbol": element[3], "close": element[5], "open": element[18], "high": element[19],
                            "low": element[20], "volume": element[15]}
                    print(data)
                    all_data.append(data)
                    # add = requests.post("http://127.0.0.1:8000/data/", data=data).json()
                except:
                    print(element)
                    pass

            def add_delete(all_data):
                delete_data = requests.delete(f"{HOST_URL}data/")
                add = requests.post(f"{HOST_URL}data/", json=all_data)
                print(add.json())
            print(len(all_data),"===all data")
            s = threading.Thread(target=add_delete, args=(all_data,))
            s.start()

            for j in range(0, 3):
                actions.send_keys_to_element(scroll, Keys.PAGE_UP).perform()
            history = []

    def run_process(self):
        cookie = self.start_browser()
        if cookie == False:
            self.login()
        self.setup()
        self.output = True
        while True:
            self.output = self.table_data()
            if self.output==False:
                try:
                    self.driver.close()
                except:
                    pass
                self.start_browser()
                self.login()
                self.setup()
            time.sleep(0.5)


