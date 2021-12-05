import time
import sys
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from db.models import Course, Semester, Student


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
            print("You can add add driver path using -d/--driver or select a different browser using -b/--browser.")
            sys.exit(1)
            
    
    def get_student_details_page(self, roll_no): 
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
        
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "tdcolor"))
            )
            element.click()
        except TimeoutException as exception:
            logging(f"[ERROR] Loading webpage. {exception.msg}")
            sys.exit(1)

        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.TAG_NAME, "a"))
            )
        except TimeoutException as exception:
            logging(f"[ERROR] Loading webpage. {exception.msg}")
            sys.exit(1)

        return BeautifulSoup(self.driver.page_source, "html.parser")

    def get_student_details(self, soup):
        span = soup.find("span", id="snamedetail")
        details_text_list = span.text.split("\xa0")
        student_name = details_text_list[0].split(" : ")[1].title()
        student_roll_no = details_text_list[5].split(" : ")[1]
        student_program = details_text_list[10].split(" : ")[1]
        student_branch = details_text_list[15].split(" : ")[1]
        return student_name, student_roll_no, student_program, student_branch

    def get_semester_details(self, link):
        WebDriverWait(self.driver, 1).until(
            EC.element_to_be_clickable(link)
        )
        link.click()
    
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, "subjectcode"))
        )
        
        courses = list()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = soup.find("tbody", id="gradeid")
        subject_rows = table.find_all("tr")
        for subject_row in subject_rows:
            subject_cols = subject_row.find_all("td")
            course = Course(
                name = subject_cols[0].text, 
                code = subject_cols[1].text, 
                course_credits = int(subject_cols[2].text), 
                grade = subject_cols[3].text
            )
            courses.append(course)
        self.driver.find_element_by_class_name("ui-dialog-titlebar-close").click()
        time.sleep(2)
        return courses

    def get_student_results(self, soup):
        results_table = soup.find("tbody", id="examgradeid")
        results = list()
        semester_rows = results_table.find_all("tr")
        semester_dialogbox_links = self.driver.find_elements_by_tag_name("a")
        for index, (semester, link) in enumerate(zip(semester_rows, semester_dialogbox_links)):
            semester_cols = semester.find_all("td")
            sem = Semester(
                number = index+1, 
                earned_credits = int(semester_cols[1].text), 
                sgpa = float(semester_cols[2].text), 
                cgpa = float(semester_cols[3].text), 
                courses=self.get_semester_details(link)
            )
            results.append(sem)

        return results

    def get_student_data(self, roll_no):
        soup = self.get_student_details_page(roll_no)
        student_details = self.get_student_details(soup)
        semesters = self.get_student_results(soup)
        student = Student(
            name = student_details[0], 
            roll_no = student_details[1], 
            program = student_details[2], 
            branch = student_details[3], 
            cgpa = semesters[-1].cgpa,
            semesters = semesters
        )
        return student