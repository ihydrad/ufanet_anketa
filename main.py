from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
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
        options.add_argument("--window-size=375,667")
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

    def __set_element_by_js(self, type_elem, elem, val):
        self.driver.execute_script(
                                    "arguments[0].value = arguments[1]",
                                    self.driver.find_element(type_elem, elem),
                                    val
                                   )    
    
    def sel_drop_menu(self, type_elem, elem, val):
        select_type = Select(self.driver.find_element(type_elem, elem))
        select_type.select_by_visible_text(val)

    def fill_page1(self):
        self.driver.find_element(By.NAME, "another_vacancies").send_keys(const.another_vacancies)
        self.driver.find_element(By.NAME, "surname").send_keys(const.surname)
        self.driver.find_element(By.NAME, "name").send_keys(const.name)
        self.driver.find_element(By.NAME, "fat_name").send_keys(const.fat_name)
        self.driver.find_element(By.NAME, "citizenship").send_keys(const.citizenship)
        self.driver.find_element(By.NAME, "adress_registration").send_keys(const.adress_registration)
        self.driver.find_element(By.NAME, "adress_residence").send_keys(const.adress_registration)
        self.driver.find_element(By.NAME, "email").send_keys(const.email)
        self.__set_element_by_js(By.ID, "id_phone", const.phone) # +7(999)999-99-99
        self.__set_element_by_js(By.ID, "id_birthday", const.birthday)

    def fill_page2(self):
        self.__set_element_by_js(By.ID, "id_educations-0-ed_time", const.id_educations0_time)
        self.driver.find_element(By.NAME, "educations-0-institution").send_keys(const.educations0)
        self.driver.find_element(By.NAME, "educations-0-speciality").send_keys(const.speciality)
        self.driver.find_element(By.NAME, "graph").send_keys(const.graph)
        self.sel_drop_menu(By.ID, 'id_educations-0-ed_type', 'очная')
        self.driver.find_element(By.NAME, "current_work").click()
        self.__set_element_by_js(By.NAME, "works-0-work_time", const.cur_work_time)
        self.driver.find_element(By.NAME, "works-0-comp_name").send_keys(const.cur_work_name)
        self.driver.find_element(By.NAME, "works-0-comp_func").send_keys(const.works0comp_func)
        self.driver.find_element(By.NAME, "works-0-post").send_keys(const.works0post)
        self.driver.find_element(By.NAME, "works-0-dis_reason").send_keys(const.reason0)
        self.fill_recommendation(give=False, reason="Не хочу раскрывать свои намерения")
        self.driver.find_element(By.NAME, "salary_min").send_keys(const.salary_min)
        self.driver.find_element(By.NAME, "salary_opt").send_keys(const.salary_opt)
        self.driver.find_element(By.NAME, "skills").send_keys(const.skills)
        
    def fill_page3(self):
        self.driver.find_element(By.NAME, "wishes").send_keys(const.wishes)
        self.set_check_box_menu("ms", "0")
        self.set_check_box_menu("how_about_us_parts", "Совет друзей")
        self.driver.find_element(By.NAME, "test_question-0-ball").send_keys(const.q[0])
        self.submit_page()
        self.driver.find_element(By.NAME, "test_question-1-ball").send_keys(const.q[1])
        self.submit_page()
        self.driver.find_element(By.NAME, "test_question-2-ball").send_keys(const.q[2])
        self.submit_page()
        self.driver.find_element(By.NAME, "test_question-3-ball").send_keys(const.q[3])
        self.submit_page()
        self.driver.find_element(By.NAME, "test_question-4-ball").send_keys(const.q[4])
        self.submit_page()
        self.driver.find_element(By.NAME, "test_question-5-ball").send_keys(const.q[5])
        self.driver.find_element(By.NAME, "test_sentence-0-ball").send_keys(const.s[0])
        self.driver.find_element(By.NAME, "test_sentence-1-ball").send_keys(const.s[1])
        self.driver.find_element(By.NAME, "test_sentence-2-ball").send_keys(const.s[2])
        self.driver.find_element(By.NAME, "test_sentence-3-ball").send_keys(const.s[3])
        self.driver.find_element(By.NAME, "test_sentence-4-ball").send_keys(const.s[4])
        self.driver.find_element(By.ID, "i687").click()
     
    def set_check_box_menu(self, name, val):
        all = self.driver.find_elements(By.NAME, name)
        for item in all:
            if item.get_attribute("value") == val:
                item.click()

    def fill_recommendation(self, give, reason):
        res = self.driver.find_elements(By.NAME, "recommendation_exist")
        if res:
            for item in res:
                val = item.get_attribute("value")
                val = False if val == "False" else True
                if  val == give:
                    item.click()
                    if not give:
                        self.driver.find_element(By.NAME, "dis_rec_reas").send_keys(reason)
                    else:
                        pass

    def submit_page(self):
        self.driver.find_element(By.ID, "submit-resume").click()    

if __name__ == "__main__":
    vac = Anketa(test_name)
    vac.open()
    vac.fill_page1()
    vac.submit_page()
    vac.fill_page2()
    vac.submit_page()
    vac.fill_page3()
    vac.submit_page()
