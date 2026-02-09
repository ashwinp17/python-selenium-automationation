from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    URL = "https://www.target.com/"

    # Locator (example; you may need to adjust based on current DOM)
    CART_ICON = (By.CSS_SELECTOR, "a[href*='/cart']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)

    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_ICON)).click()
