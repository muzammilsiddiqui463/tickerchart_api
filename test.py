# import requests
#
# r = requests.get("https://web-production-8a109.up.railway.app/data/")
# print(r.json())

from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import os

# Define Chrome options
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Run Chrome in headless mode
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH")

# Initialize the WebDriver with Chrome options
driver = uc.Chrome(options=chrome_options, driver_executable_path=os.environ.get("CHROMEDRIVER_PATH"))
driver.maximize_window()
driver.get("https://www.tickerchart.net/app/en#")
driver.close()