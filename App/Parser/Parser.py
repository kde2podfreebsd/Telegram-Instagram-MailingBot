import os
import time
from selenium import webdriver
# from pyvirtualdisplay import Display
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pickle 

basedir = os.path.abspath(os.path.dirname(__file__))


class Parser:
    __instance = None

    @classmethod
    def getInstance(cls):
        try:
            if not cls.__instance:
                cls.__instance = Parser()
            return cls.__instance
        except Exception as e:
            return e

    def __init__(self):
        if not Parser.__instance:
            self.__op = webdriver.ChromeOptions()
            # self.__op.add_argument("--no-sandbox") 
            # self.__op.add_argument("--disable-dev-shm-usage")
            # self.__op.add_argument(f"--log-path=parser.log")
            # self.__display = Display(visible=True, size=(1234, 1234))
            # self.__display.start()
            self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.__op)
        else:
            print("Instance already created:", self.getInstance())

    def close_parser(self):
        try:
            self.driver.quit()
            self.driver.close()
            # self.__display.stop()
        except Exception as e:
            return e

    # def create_session(self, url: str):
    #     try:
    #         self.driver.get(url=url)
    #         time.sleep(25)
    #         pickle.dump(self.driver.get_cookies(), open(f'sessions/{self.resource}', 'wb'))
    #         print(f"session saved! Service: {self.resource}")
    #     except Exception as e:
    #         return e
    #     finally:
    #         self.close_parser()

    # def load_cookie(self, url: str):
    #     try:
    #         self.driver.get(url)
    #         for cookie in pickle.load(open(f'App/{self.resource}', 'rb')):
    #             self.driver.add_cookie(cookie)
    #         self.driver.get(url)
    #     except Exception as e:
    #         return e
