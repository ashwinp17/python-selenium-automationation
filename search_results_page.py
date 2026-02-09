from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SearchResultsPage(BasePage):
    PRODUCT_TILE = (By.CSS_SELECTOR, "[data-test*='product']")

    def __init__(self, driver):
        super().__init__(driver)  # <-- THIS creates self.wait

    def verify_search_results(self, product_result):
        self.wait.until(EC.presence_of_element_located(self.PRODUCT_TILE))
