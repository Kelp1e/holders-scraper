import os
import urllib.parse
from time import sleep

from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium.common import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha

load_dotenv()

CAPTCHA_TOKEN = os.getenv("CAPTCHA_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PROXY = os.getenv("PROXY")

CAPTCHA_URL_1 = "https://maximedrn.github.io/hcaptcha-solver-python-selenium/"
CAPTCHA_URL_2 = "https://2captcha.com/ru/demo/hcaptcha"
CAPTCHA_URL_3 = "https://accounts.hcaptcha.com/demo"

user_agent = UserAgent()

options = Options()
options.add_argument(f"--user-agent={user_agent.random}")

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US,en")
options.add_argument("--no-referrers")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--disable-setuid-sandbox")


class Driver:
    def __init__(self):
        self.driver = Chrome(options=options)


class CaptchaSolver(Driver):
    def __init__(self, captcha_token):
        super().__init__()
        self.captcha_token = captcha_token

    def open_test_page(self, url):
        self.driver.get(url)
        if self._is_captcha():
            self._solve_captcha()

    def _solve_captcha(self):
        sitekey = self.__get_sitekey_from_url()
        count = self.__get_count_textarea()
        solve_result = self.__get_solve_result(sitekey)

        self.__init_textarea(count, solve_result)

    def _is_captcha(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "h-captcha")
            return True
        except NoSuchElementException:
            return False

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

    def __get_solve_result(self, sitekey):
        captcha_solver = TwoCaptcha(apiKey=self.captcha_token)
        captcha_solve_result = captcha_solver.hcaptcha(
            sitekey=sitekey, url=self.driver.current_url
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

    def solve_captchas_on_page(self):
        while True:
            if self._is_captcha():
                self._solve_captcha()
            sleep(1)

    @staticmethod
    def __send_solution_code(solve_result, *elements):
        for element in elements:
            element.send_keys(solve_result)


class Discord(CaptchaSolver):
    def __init__(self, captcha_token, discord_token):
        super().__init__(captcha_token)
        self.discord_token = discord_token

    def process(self):
        self._register("vladbvbb2sdfsdf2@gmail.com", "Kelp1fghDevelopment", "aa0316icman")

    def _register(self, email, username, password):
        self.driver.get("https://discord.com/register/")
        sleep(5)

        email_input = self.driver.find_element(By.NAME, "email")
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")

        email_input.send_keys(email)
        username_input.send_keys(username)
        password_input.send_keys(password)

        sleep(10)

        self.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div[2]/div[1]/div[1]/div/div/div/form/div[2]/div/div[5]/button",
        ).click()

        sleep(10)

        try:
            captcha = self.driver.find_element(By.XPATH,
                                               "/html/body/div[2]/div[2]/div[1]/div[4]/div[2]/div/div/div/div[1]/div[4]/div/iframe")
            super()._solve_captcha()
        except NoSuchElementException:
            pass

        sleep(40)


discord = Discord(CAPTCHA_TOKEN, DISCORD_TOKEN)
discord.process()
