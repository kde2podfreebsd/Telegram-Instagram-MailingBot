from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from App.Config import inst_sessions_dirPath

from App.Parser.Xpath import *

from App.Parser.Parser import Parser
from App.Parser.ProxyExtension import ProxyExtension
import ssl

import pickle 
import time
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

ssl._create_default_https_context = ssl._create_unverified_context

class InstagramParser(Parser):
    def __init__(
            self, 
            login: str,
            password: str
        ):
        super().__init__()
        self.login = login
        self.password = password

        ip, port, login, password = os.getenv("PROXY_ADDRESS").split(":")
        proxy_extension = ProxyExtension(ip, int(port), login, password)
        options = uc.ChromeOptions()
        options.add_argument(f"--load-extension={proxy_extension.directory}")
        self.driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    # def click_cookie_agreement(self):
    #     time.sleep(5)
    #     wait = WebDriverWait(self.driver, 15)
    #     cookies = wait.until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREEMENT_XPATH)))
    #     print("HEEEERRRRREEEEE")
    #     while(not(cookies)):
    #         cookies = wait.until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREEMENT_XPATH)))
    #         time.sleep(10)
    #         print("IN CYCLE")
    #     cookies.click()
        
    # async def async_click_cookie_agreement(self):
    #     loop = asyncio.get_event_loop()
    #     result = await loop.run_in_executor(None, self.click_cookie_agreement)
    #     return result 


    async def async_logging_in(self):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.logging_in)
        return result

    def logging_in(self):
        try:
            self.driver.get(url="https://instagram.com/")
            wait = WebDriverWait(self.driver, 15)

            # cookies = wait.until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREEMENT_XPATH)))
            # cookies.click()
            time.sleep(10)
            wait.until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREEMENT_XPATH))).click()
            print("CLICKED")
            wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_INPUT_XPATH))).send_keys(self.login) 
            wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))).send_keys(self.password)
            wait.until(EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))).click()
            try:
                result = self.driver.find_element(By.CLASS_NAME, INCORRECT_PASS_OR_LOGIN_ERROR_CLASS_NAME)
                if (result):
                    raise Exception("Incorrect password or login")
                else:
                    time.sleep(15)
                    self.dump_cookies()
                    return None
            except Exception as e:
                return None
        except Exception as e:
            return str(e)
        finally:
            self.close_parser()

        
    def parse_followers(self, channel: str):
        try:
            wait = WebDriverWait(self.driver, 15)

            self.driver.get(url="https://instagram.com/")
            js_click_script = """
var button = document.evaluate("//button[@class='_a9-- _ap36 _a9_1']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
button.click();
"""
            self.driver.execute_script(js_click_script)
            self.load_cookies()
            time.sleep(5)

            self.driver.get(url=f"https://instagram.com/{channel}/")
            wait.until(EC.element_to_be_clickable((By.XPATH, FOLLOWERS_BUTTON_XPATH))).click()
            time.sleep(5)

            dialogue = wait.until(EC.presence_of_element_located((By.CLASS_NAME, FOLLOWER_DIALOGUE_CLASS_NAME)))
            self.scroll_followers_dialogue(
                wait=wait,
                dialogue=dialogue
            )
            time.sleep(10)
            followers = dialogue.find_elements(By.CLASS_NAME, FOLLOWER_USERNAME_CLASS_NAME)
            usernames = list(set([follower.text for follower in followers]))
            print(usernames, len(usernames))

            time.sleep(60)
        except Exception as e:
            return e
        finally:
            self.close_parser()
    
    def scroll_followers_dialogue(self, wait, dialogue, step=12):
        followers_count = int(wait.until(EC.presence_of_element_located((By.XPATH, FOLLOWER_COUNT_XPATH))).text.replace(',', ''))
        curr_followers_count = 12
        while curr_followers_count + step <= followers_count:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", dialogue)
            time.sleep(2)  
            curr_followers_count += step


    def dump_cookies(self):
        try:
            cookies = self.driver.get_cookies()
            pickle.dump(cookies, open(f"{inst_sessions_dirPath}/{self.login}.cookies", "wb"))
        except Exception as e:
            return e 
        
    def load_cookies(self):
        try:
            cookies = pickle.load(open(f"{inst_sessions_dirPath}/{self.login}.cookies", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception as e:
            return e
    

