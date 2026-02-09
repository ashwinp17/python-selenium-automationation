from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait

from pages.target_home_page import TargetHomePage


@then('I should see search results related to "{expected_keyword}"')
def step_verify_results(context, expected_keyword):
    WebDriverWait(context.driver, 10).until(lambda d: expected_keyword.lower() in d.page_source.lower())
