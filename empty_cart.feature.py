from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By

@given("I open Target")
def step_open_target(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.target.com/")

@when("I go to the cart")
def step_go_to_cart(context):
    context.driver.get("https://www.target.com/cart")

@then("I should see the cart is empty")
def step_cart_empty(context):
    body_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert "Your cart is empty" in body_text
    context.driver.quit()

