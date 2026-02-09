from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Header:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def search(self, text):
        # example: type text then submit/click
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "search"))
        )
        search_input.clear()
        search_input.send_keys(text)
