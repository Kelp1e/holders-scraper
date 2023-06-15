import os
from time import sleep
import urllib.parse

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

load_dotenv()

CAPTCHA_URL = "https://maximedrn.github.io/hcaptcha-solver-python-selenium/"
C = "https://2captcha.com/ru/demo/hcaptcha"
TOKEN = os.getenv("CAPTCHA_API")


class CaptchaSolver:
    def __init__(self, token, url):
        self.driver = webdriver.Chrome()
        self.token = token
        self.url = url

    def open_page_with_captcha(self):
        self.driver.get(self.url)
        self.__solve_captcha()

    def __solve_captcha(self):
        if self.__is_captcha():
            sitekey = self.__get_sitekey_from_url()
            count = self.__get_count_textarea()
            solve_result = self.__get_solve_result(sitekey)

            self.__init_textarea(count, solve_result)

            sleep(5)

    def __get_sitekey_from_url(self):
        iframe = self.driver.find_element(By.TAG_NAME, "iframe")
        sitekey_url = iframe.get_attribute("src")

        parsed_url = urllib.parse.urlparse(sitekey_url)
        query_params = urllib.parse.parse_qs(parsed_url.fragment)
        sitekey = query_params.get("sitekey", [""])[0]

        return sitekey

    def __get_count_textarea(self):
        count = len(self.driver.find_elements(By.TAG_NAME, "textarea"))

        return count

    def __get_solve_result(self, token_captcha):
        captcha_solver = TwoCaptcha(apiKey=self.token)
        captcha_solve_result = captcha_solver.hcaptcha(
            sitekey=token_captcha, url=self.url
        )

        return captcha_solve_result["code"]

    def __init_textarea(self, count, solve_result):
        if count == 1:
            h_captcha_response = self.driver.find_element(By.NAME, "h-captcha-response")
            self.__show_textarea(h_captcha_response)

            self.__send_solution_code(solve_result, h_captcha_response)
        elif count == 2:
            h_captcha_response = self.driver.find_element(By.NAME, "h-captcha-response")
            g_recaptcha_response = self.driver.find_element(
                By.NAME, "g-recaptcha-response"
            )
            self.__show_textarea(h_captcha_response, g_recaptcha_response)

            self.__send_solution_code(
                solve_result, h_captcha_response, g_recaptcha_response
            )

    def __show_textarea(self, *elements):
        for element in elements:
            self.driver.execute_script("arguments[0].style.display = 'block'", element)

    def __is_captcha(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "h-captcha")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def __send_solution_code(solve_result, *areas):
        for area in areas:
            area.send_keys(solve_result)


CaptchaSolver(TOKEN, CAPTCHA_URL).open_page_with_captcha()
