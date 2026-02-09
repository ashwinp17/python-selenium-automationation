from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    # Locator for empty cart message (example; adjust if needed)
    EMPTY_CART_MESSAGE = (By.XPATH, "//*[normalize-space()='Your cart is empty']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def empty_cart_message_text(self) -> str:
        el = self.wait.until(EC.visibility_of_element_located(self.EMPTY_CART_MESSAGE))
        return el.text
