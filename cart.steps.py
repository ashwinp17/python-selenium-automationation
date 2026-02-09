from behave import given, when, then
from pages.home_page import HomePage
from pages.cart_page import CartPage

@given("I am on the Target home page")
def step_open_home(context):
    context.home = HomePage(context.driver)
    context.home.open()

@when("I open the cart")
def step_open_cart(context):
    context.home.open_cart()
    context.cart = CartPage(context.driver)

@then("I should see the empty cart message")
def step_verify_empty_cart(context):
    actual = context.cart.empty_cart_message_text()
    assert "Your cart is empty" in actual, f"Expected empty cart message, got: {actual}"
