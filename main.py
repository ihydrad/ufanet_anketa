from cgitb import text
from distutils.command.config import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import const
from time import sleep

test_name = "Системный администратор в отдел информационной безопасности"


class Anketa:
    def __init__(self, name) -> None:
        self.name = name
        self.driver = self.setup_browser()

    @staticmethod
    def setup_browser():
        chrome_bin_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_driver_path = "chromedriver.exe"
        options = Options()
        options.binary_location = chrome_bin_path
        options.add_argument("start-maximized")
        #options.add_argument("--disable-gpu-vsync") 
        #options.add_argument("--remote-debugging-port=9222")
        driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
        return driver

    def __get_item(self, item_name):
        self.driver.get(const.url_ufa)
        wait = WebDriverWait(self.driver, 10)
        sleep(5)
        items = self.driver.find_elements(By.CLASS_NAME, "vacancy__title")
        for item in items:
            if item_name in item.text:
                return item.find_element(By.XPATH, '..')

    def open(self):
        vacancy = self.__get_item(self.name)
        btns = vacancy.find_elements(By.TAG_NAME, "button")
        for btn in btns:
            if "Заполнить анкету" in btn.text:
                btn.click()

    def fill_page1(self):
        self.driver.find_element(By.NAME, "surname").send_keys(const.surname)
        self.driver.find_element(By.NAME, "name").send_keys(const.name)
        self.driver.find_element(By.NAME, "fat_name").send_keys(const.fat_name)
        self.driver.find_element(By.NAME, "citizenship").send_keys(const.citizenship)
        self.driver.find_element(By.NAME, "adress_registration").send_keys(const.adress_registration)
        self.driver.find_element(By.NAME, "adress_residence").send_keys(const.adress_registration)
        self.driver.find_element(By.NAME, "email").send_keys(const.email)
        phone_el = self.driver.find_element(By.NAME, "phone")
        phone_el.click()
        for i in range(9):
            phone_el.send_keys(Keys.CONTROL, 'LEFT')
        phone_el.send_keys(const.phone)
        bd_el = self.driver.find_element(By.NAME, "birthday")
        self.driver.execute_script("arguments[0].value = arguments[1]", bd_el, const.birthday)



vac = Anketa(test_name)
vac.open()
vac.fill_page1()