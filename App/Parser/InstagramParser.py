from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

from App.Config import inst_sessions_dirPath
from App.Logger import ApplicationLogger

from App.Parser.Xpath import *
from App.Parser.Parser import Parser
from App.Parser.ProxyExtension import ProxyExtension

import ssl
import pickle 
import time
import asyncio
import functools

logger = ApplicationLogger()

ssl._create_default_https_context = ssl._create_unverified_context

class InstagramParserExceptions():
    def __init__(self):
        self.IncorrectPasswordOrLogin = Exception("You have entered invalid password or login")
        self.PageNotFound = Exception("The channel name you have entered is invalid")
        self.SuspendedAccount = Exception("This instagram account has been suspended")
        self.PrivateAccount = Exception("Message cannot be sent to user, as they prhobited messaging them")
        self.ProxyConnectionFailed = Exception("unknown error: net::ERR_PROXY_CONNECTION_FAILED")
        self.CaptchaVerification = Exception("Instagrram inquiring captcha verification on this account")


class InstagramParser(Parser):
    def __init__(
            self, 
            login: str,
            password: str,
            proxy: str
        ):
        super().__init__()
        self.login = login
        self.password = password
        self.proxy = proxy

        ip, port, login, password = proxy.split(":")
        proxy_extension = ProxyExtension(ip, int(port), login, password)
        options = uc.ChromeOptions()
        options.add_argument(f"--load-extension={proxy_extension.directory}")
        self.driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        logger.log_info(f"InstagramParser initialization on {self.login}'s account")

    async def async_check_proxy(self):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.check_proxy)
        return result

    def check_proxy(self):
        try:   
            self.driver.get("https://whoer.net/ru")
            wait = WebDriverWait(self.driver, 15)
            ip = wait.until(EC.presence_of_element_located((By.XPATH, IP_XPATH))).text
            proxy_ip = self.proxy.split(":")[0]
            if (ip == proxy_ip): 
                logger.log_info(f"Proxy with proxy_ip {proxy_ip} is valid")
                return True
            else:
                logger.log_error(f"Proxy with proxy_ip {proxy_ip} is invalid")
                return False
        except Exception as e:
            logger.log_error(f"An error occured while checking proxy address: {e}")
            return e
        finally:
            self.close_parser()

    async def async_logging_in(self):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.logging_in)
        return result

    def logging_in(self):
        instagramExceptions = InstagramParserExceptions()
        try:
            self.driver.get(url="https://instagram.com/")
            wait = WebDriverWait(self.driver, 15)
            cookies = wait.until(EC.element_to_be_clickable((By.XPATH, COOKIES_AGREEMENT_XPATH)))
            cookies.click()

            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.XPATH, LOGIN_INPUT_XPATH))).send_keys(self.login) 
            wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH))).send_keys(self.password)
            wait.until(EC.element_to_be_clickable((By.XPATH, LOGIN_BUTTON_XPATH))).click()
            time.sleep(10)

            current_url = self.driver.current_url
            if ("suspended" in current_url):
                logger.log_error(f"Account {self.login} has been banned")
                raise instagramExceptions.SuspendedAccount
            
            # if ("challenge" in current_url):
            #     logger.log_error(f"Captcha verification is required for {self.login} to login in")
            #     raise instagramExceptions.CaptchaVerification         
            
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, PROBLEM_WITH_LOGGING_IN_XPATH)))
            except Exception as e:
                pass
            else:
                logger.log_error("Invalid login or password have been entered by the user for logging in")
                raise instagramExceptions.IncorrectPasswordOrLogin
            
            time.sleep(15)
            self.dump_cookies()
        
        except Exception as e:
            logger.log_error(f"An error occured while logging in user's instagram account: {e}")
            return e
        finally:
            self.close_parser()

    
    async def async_parse_follower(self, channel: str):
        loop = asyncio.get_event_loop()
        partial_parse_followers = functools.partial(self.parse_followers, channel)
        result = await loop.run_in_executor(None, partial_parse_followers)
        return result
        
    def parse_followers(self, channel: str):
        instagramParserExceptions = InstagramParserExceptions()
        try:
            wait = WebDriverWait(self.driver, 15)

            self.driver.get(url="https://instagram.com/")
            self.load_cookies()

            self.driver.get(url=f"https://instagram.com/{channel}/")

            try:
                self.driver.find_element(By.XPATH, PAGE_NOT_FOUND_XPATH)
            except Exception as e:
                pass
            else:
                logger.log_error(f"User with channel name {channel} has not been found, such page does not exist")
                raise instagramParserExceptions.PageNotFound
            
            followers_count = int(wait.until(EC.presence_of_element_located((By.XPATH, FOLLOWER_COUNT_XPATH))).text.replace(',', ''))

            wait.until(EC.element_to_be_clickable((By.XPATH, FOLLOWERS_BUTTON_XPATH))).click()
            time.sleep(5)

            dialogue = wait.until(EC.presence_of_element_located((By.CLASS_NAME, FOLLOWER_DIALOGUE_CLASS_NAME)))
            self.scroll_followers_dialogue(
                followers_count=followers_count,
                dialogue=dialogue
            )
            followers = dialogue.find_elements(By.CLASS_NAME, FOLLOWER_USERNAME_CLASS_NAME)
            usernames = list(set([follower.text for follower in followers]))
    
            return usernames
        except Exception as e:
            logger.log_error(f"An error occured while parsing {channel}'s followers")
            return e
        finally:
            self.close_parser()
    

    def scroll_followers_dialogue(self, dialogue, followers_count, step=12):
        curr_followers_count = 12
        while curr_followers_count + step <= followers_count:
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", dialogue)
            time.sleep(2)  
            curr_followers_count += step

    async def async_send_message(self, message: str, reels_link: str | None, channel: str):
        await asyncio.sleep(5)
        loop = asyncio.get_event_loop()
        partial_send_message = functools.partial(self.send_message, message, reels_link, channel)
        result = await loop.run_in_executor(None, partial_send_message)
        return result

    def send_message(self, message: str, reels_link: str | None, channel: str):
        try:
            wait = WebDriverWait(self.driver, 15)

            self.driver.get(url="https://instagram.com/")
            self.load_cookies()

            self.driver.get(url=f"https://instagram.com/{channel}/")
            try:
                self.driver.find_element(By.XPATH, PAGE_NOT_FOUND_XPATH)
            except Exception as e:
                pass
            else:
                logger.log_error(f"User with channel name {channel} has not been found, such page does not exist")
                raise None
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, MESSAGE_BUTTON_XPATH))).click()
            except Exception as e:
                logger.log_error(f"Message cannot be sent to user with channel name {channel}, as they prhobited messaging them")
                return None
                
            wait.until(EC.element_to_be_clickable((By.XPATH, TURN_ON_NOTIFICATIONS_BUTTON_XPATH))).click()
            send_message_field = wait.until(EC.presence_of_element_located((By.XPATH, SEND_MESSAGE_FIELD_XPATH)))

            if (reels_link != "Не указана"):
                send_message_field.send_keys(reels_link)
                send_message_field.send_keys(Keys.ENTER)
            if (message != "Не указано"):
                send_message_field.send_keys(message)
                send_message_field.send_keys(Keys.ENTER)
            time.sleep(5)

        except Exception as e:
            logger.log_error(f"An exception occured in send_message: {e}")
            return None
        finally:
            self.close_parser()
    
    async def async_send_reels(self, reels_link: str, message: str, channel: str):
        loop = asyncio.get_event_loop()
        partial_send_reels = functools.partial(self.send_reels, reels_link, message, channel)
        result = await loop.run_in_executor(None, partial_send_reels)
        return result

    def dump_cookies(self):
        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(f"{inst_sessions_dirPath}/{self.login}.cookies", "wb"))
        
            
        
    def load_cookies(self):
        try:
            cookies = pickle.load(open(f"{inst_sessions_dirPath}/{self.login}.cookies", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            return None
        except Exception as e:
            return e
