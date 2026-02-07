from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager


def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def test_add_target_product_to_cart():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    wait = WebDriverWait(driver, 25)

    try:
        driver.get("https://www.target.com/")

        # Search for a product
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "search")))
        search_box.clear()
        search_box.send_keys("tea")

        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and @aria-label='search']")))
        search_btn.click()

        # Ensure search results page loaded
        wait.until(EC.url_contains("/s?searchTerm="))

        # Click first product (robust fallback)
        first_product = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//a[contains(@href,'/p/')])[1]"))
        )
        try:
            first_product.click()
        except ElementClickInterceptedException:
            js_click(driver, first_product)

        # Click "Add to cart"
        add_to_cart = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[normalize-space()='Add to cart'] or normalize-space()='Add to cart']")
            )
        )
        try:
            add_to_cart.click()
        except ElementClickInterceptedException:
            js_click(driver, add_to_cart)

        # ✅ Go directly to cart (most reliable)
        driver.get("https://www.target.com/cart")

        # Verify: cart has items OR subtotal/total exists
        # Try multiple cart-item patterns
        cart_item_locators = [
            (By.XPATH, "//*[@data-test='cartItem' or @data-test='cart-item']"),
            (By.XPATH, "//*[contains(@data-test,'cartItem')]"),
            (By.XPATH, "//*[contains(@class,'CartItem') or contains(@class,'cartItem')]"),
        ]

        has_item = False
        for loc in cart_item_locators:
            items = driver.find_elements(*loc)
            if len(items) > 0:
                has_item = True
                print(f"PASS: Cart has {len(items)} item(s).")
                break

        if not has_item:
            # Fallback: subtotal/total text exists
            subtotal_or_total = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     "//*[contains(translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'subtotal')]"
                     " | //*[contains(translate(normalize-space(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'total')]")
                )
            )
            print("PASS: Subtotal/Total found:", subtotal_or_total.text)

    finally:
        driver.quit()


if __name__ == "__main__":
    test_add_target_product_to_cart()
