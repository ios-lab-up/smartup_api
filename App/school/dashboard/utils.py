from school.student.utils import createStudent
from school.models import ChromeBrowser
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from school.tools.utils import color
from flask import session
import time
import logging
import traceback


def enterDashboard(browser: ChromeBrowser) -> str:
    '''Extracts the schedule link from the main page'''
    try:
        try:
            userName = browser.find_element(
                By.XPATH, "//div[@class='user-title pull-left hidden-xs']").find_element(By.XPATH, "//strong").text
            createStudent(**session['student'], name=userName)
        except NoSuchElementException:
            logging.error(
                f'{color(1,"Couldnt create student")} ❌ {traceback.format_exc().splitlines()[-3]}')

        # browser.find_element(By.LINK_TEXT, "Horarios").click()
        # time.sleep(3)
        # logging.info(f'{color(2,"Loading schedule...")} ✅')
    except NoSuchElementException:
        logging.error(f'{color(1,"Schedule link not found")} ❌')

    return f'Current URL after main menu: \033[94m{browser.current_url}\033[0m'


def enterDashboardUPSite(browser: ChromeBrowser) -> str:
    '''Extracts the schedule link from the main page'''
    try:
        upsite_subjecs = enterUPSiteSubjects(browser)
    except NoSuchElementException:
        logging.error(
            f'{color(1,"Something went wrong while being in dasboard")} ❌ {traceback.format_exc().splitlines()[-3]}')
        upsite_subjecs = None

    return upsite_subjecs


def enterUPSiteSubjects(browser) -> str:
    '''Fetches the subjects from the UPSite page'''
    try:
        browser.get(
            "https://upsite.up.edu.mx/psc/CAMPUS/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?ICType=Panel&ICElementNum=0&ICStateNum=21&ICResubmit=1&ICAJAX=1&")
        browser.find_element(
            By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ptModFrame_0"]')))
        browser.switch_to.frame(
            browser.find_elements(By.TAG_NAME, 'iframe')[0])
        browser.find_element(By.ID, "#ICSave").click()
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'win0div$ICField94')))

        logging.info(
            f'{color(2,"Enter Carrito de Inscripción...")} ✅')
    except NoSuchElementException:
        logging.error(
            f'{color(1,"Carrito de Inscripción link not found")} ❌ {traceback.format_exc().splitlines()[-3]}')
