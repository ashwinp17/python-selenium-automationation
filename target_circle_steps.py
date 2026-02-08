from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from behave import given, then

@given("I open the Target Circle page")
def step_open_circle_page(context):
    pass

@then('I should see "{expected_cards}" story cards under "Unlock added value"')
def step_verify_storycards(context, expected_cards):
    pass
