import time
import sys
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class WebScraper():
    
    page_url = "https://erp.nitdelhi.ac.in/CampusLynxNITD/studentonindex.jsp"
    
    def __init__(self, browser, driver_path=None):
        self.driver = self.get_driver(browser=browser, driver_path=driver_path)

    @staticmethod
    def get_driver(browser, driver_path):
        try:
            if browser == "chrome":
                if driver_path is None:
                    return webdriver.Chrome()
                else:
                    return webdriver.Chrome(executable_path=driver_path)
            elif browser == "firefox":
                if driver_path is None:
                    return webdriver.Firefox()
                else:
                    return webdriver.Firefox(executable_path=driver_path)
            elif browser == "edge":
                if driver_path is None:
                    return webdriver.Edge()
                else:
                    return webdriver.Edge(executable_path=driver_path)
            elif browser == "safari":
                if driver_path is None:
                    return webdriver.Safari()
                else:
                    return webdriver.Safari(executable_path=driver_path)
        except WebDriverException as exception:
            logging.error(f"[ERROR] Loading driver for {browser}. {exception.msg}")
            print("You can add add driver path using -d or --driver")
            sys.exit(1)
            
    
    def enter_student_details(self, roll_no): 
        self.driver.get(WebScraper.page_url)
        iframe = self.driver.find_elements_by_tag_name('iframe')[0]
        self.driver.switch_to.frame(iframe)
        
        rollno_field = self.driver.find_element_by_id("studentrollno")
        rollno_field.send_keys(roll_no)
        
        captchatext = self.driver.find_element_by_id("ebcaptchatext").text
        
        captcha_field = self.driver.find_element_by_id("ebcaptchainput")
        captcha_field.send_keys(captchatext)

        submit_button = self.driver.find_elements_by_id('cbutton')[0]
        submit_button.click()
        
        # time.sleep(3)
        self.driver.find_element_by_class_name("tdcolor").click()
        # time.sleep(3)
