from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By

@given("I open Target")
def step_open_target(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.target.com/")

@when("I click the Account button")
def step_click_account(context):
    context.driver.find_element(By.ID, "account-sign-in").click()

@when("I click Sign In from the side navigation")
def step_click_side_nav_sign_in(context):
    context.driver.find_element(By.XPATH, "//button[@data-test='accountNav-signIn']").click()

@then("I should see the Sign In form")
def step_verify_sign_in_form(context):
    header_text = context.driver.find_element(
        By.XPATH, "//h1[normalize-space()='Sign in or create account']"
    ).text
    assert header_text == "Sign in or create account"
    context.driver.find_element(By.XPATH, "//button[@type='submit']")

    context.driver.quit()
