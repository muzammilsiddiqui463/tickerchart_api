from ast import literal_eval
import time
import requests
from selenium import webdriver
# import webdriver_manager

def get_profiles():
        res = requests.get("http://localhost:35000/profile/all").json()
        profiles = []
        for profile in res['profileData']:
            profile_id = profile["general_profile_information"]['browser_id']
            profiles.append(profile_id)
        return profiles

def stop_driver(incogniton_profile_id):
        try:
            stop_url = 'http://127.0.0.1:35000/profile/stop/' + incogniton_profile_id
            resp = requests.get(stop_url)

        except Exception as e:
            pass

        time.sleep(6)

def initiate_driver(incogniton_profile_id):
        # localhost:35000/profile/launch/{profile_id}/force/cloud

        try:
            stop_url = 'http://127.0.0.1:35000/profile/stop/' + incogniton_profile_id
            resp = requests.get(stop_url)
            print(resp.json())
        except Exception as e:
            print("Failed to stop")

        incogniton_url = 'http://127.0.0.1:35000/automation/launch/python/'
        time.sleep(6)

        data = {"profileID": incogniton_profile_id}
        for i in range(12):
            try:
                resp = requests.post(incogniton_url, data)
                incomingJson = resp.json()

                python_dict = literal_eval(incomingJson['dataDict'])
                options = webdriver.ChromeOptions()
                options.add_argument('--disable-browser-side-navigation')
                driver = webdriver.Remote(
                    command_executor=incomingJson['url'], options=options)

                time.sleep(2)

                # driver.get("https://www.incogniton.com")
                return driver
            except Exception as e:
                print(e)
                continue