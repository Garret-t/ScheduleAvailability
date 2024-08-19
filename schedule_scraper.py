from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime

SCHEDULE_URL = 'https://consumer.scheduling.athena.io/?locationId=21276-1&practitionerId=21276-1'

VISIT_ID = 'visitReason'

MONTH_YEAR_CLASS = 'src-consumer-portal-workflow-filters-calendar-calendar-module__month-label--hbXEe'
AVAILABLE_DAY_CLASS = 'src-consumer-portal-workflow-filters-calendar-calendar-module__is-available--pz8Db'
LOADING_CLASS = 'src-consumer-portal-workflow-filters-calendar-calendar-module__loading--ONP3U'

NEXT_MONTH_CSS_SELECTOR = 'button[data-cy="monthlyNavright"]'

def _get_available_days(driver):
    month_year_text = driver.find_element(by=By.CLASS_NAME, value=MONTH_YEAR_CLASS).text
    current_month_date = datetime.strptime(month_year_text, '%B %Y')

    days = driver.find_elements(by=By.CLASS_NAME, value=AVAILABLE_DAY_CLASS)

    available_days = []
    for day in days:
        date_str = day.get_attribute('data-date')
        if current_month_date.month == datetime.strptime(date_str, "%Y-%m-%d").month:
            available_days.append(date_str)
    
    return available_days


def init_scraper_driver():
    options = Options()
    options.add_argument('--disable-proxy-certificate-handler')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


def get_scraped_availability(driver, visit_reason='Annual Physical'):
    driver.get(url=SCHEDULE_URL)
    driver.maximize_window()

    # Wait for page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, VISIT_ID)))
    visit_reason_select = Select(driver.find_element(by=By.ID, value=VISIT_ID))
    visit_reason_select.select_by_visible_text(text=visit_reason)

    # Wait for calendar to load days
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, LOADING_CLASS)))
    current_month_available_days = _get_available_days(driver=driver)

    next_month_button = driver.find_element(by=By.CSS_SELECTOR, value=NEXT_MONTH_CSS_SELECTOR)
    next_month_button.click()

    # Wait for calendar to load days
    WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.CLASS_NAME, LOADING_CLASS)))
    next_month_available_days = _get_available_days(driver=driver)

    return {'current_month': current_month_available_days, 'next_month': next_month_available_days}
