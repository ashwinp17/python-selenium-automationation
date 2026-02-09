from behave_steps import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from behave_steps import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_HOME_URL = "https://www.target.com/"
DEFAULT_WAIT = 15

def wait_for(context, condition, timeout=DEFAULT_WAIT):
    return WebDriverWait(context.driver, timeout).until(condition)

@given("I open the Target home page")
def step_open_target_home(context):
    context.driver.get(TARGET_HOME_URL)
    wait_for(context, EC.presence_of_element_located((By.ID, "search")))


@then('search results for "{search_term}" are shown')
def step_verify_results(context, search_term):
    # Wait for a results page element
    results_heading = (By.XPATH, "//*[self::h1 or self::h2][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'results')]")
    wait_for(context, EC.presence_of_element_located(results_heading))
