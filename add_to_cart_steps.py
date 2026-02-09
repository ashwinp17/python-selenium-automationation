from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def wait(context, seconds=15):
    return WebDriverWait(context.driver, seconds)


def safe_click(context, by, value, timeout=12):
    el = WebDriverWait(context.driver, timeout).until(EC.element_to_be_clickable((by, value)))
    try:
        el.click()
    except ElementClickInterceptedException:
        context.driver.execute_script("arguments[0].click();", el)


def try_close_popups(context):
    """
    Target may show:
    - cookie banner
    - location/store modal
    - privacy modal
    We'll attempt a few common close patterns without failing the test if not present.
    """
    d = context.driver

    # 1) Cookie / privacy banners often have close or accept buttons
    possible_buttons = [
        (By.XPATH, "//button[contains(.,'Accept') or contains(.,'I Accept')]"),
        (By.XPATH, "//button[contains(.,'OK') or contains(.,'Got it')]"),
        (By.XPATH, "//button[@aria-label='close' or @aria-label='Close']"),
        (By.XPATH, "//button[contains(@data-test,'close') or contains(@id,'close')]"),
        (By.XPATH, "//div[@role='dialog']//button[contains(.,'Close') or contains(.,'No thanks')]"),
    ]

    for by, value in possible_buttons:
        try:
            btn = WebDriverWait(d, 2).until(EC.element_to_be_clickable((by, value)))
            btn.click()
        except TimeoutException:
            pass
        except Exception:
            pass


@given("I open Target home page")
def step_open_target(context):
    opts = Options()
    opts.add_argument("--incognito")
    opts.add_argument("--start-maximized")

    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    context.driver.get("https://www.target.com/")
    try_close_popups(context)


@when('I search for "{query}"')
def step_search(context, query):
    try_close_popups(context)

    # Target search input (commonly name="searchTerm")
    search_input = wait(context, 15).until(
        EC.presence_of_element_located((By.NAME, "searchTerm"))
    )
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)

    # Wait for results area to load
    wait(context, 15).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@data-test,'product-grid') or @data-test='product-grid']"))
    )


@when("I open the first product result")
def step_open_first_result(context):
    try_close_popups(context)

    # Click first product link/card in the grid
    first_product = wait(context, 15).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "(//a[contains(@href,'/p/') and (ancestor::div[@data-test='product-grid'] or ancestor::div[contains(@data-test,'product-grid')])])[1]"
        ))
    )
    first_product.click()

    # Product page: wait for an Add to cart button to exist
    wait(context, 15).until(
        EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(.,'Add to cart') or contains(.,'Add to Cart') or @data-test='addToCartButton']"
        ))
    )


@when("I add the product to the cart")
def step_add_to_cart(context):
    try_close_popups(context)

    # Click Add to cart
    safe_click(
        context,
        By.XPATH,
        "//button[contains(.,'Add to cart') or contains(.,'Add to Cart') or @data-test='addToCartButton']",
        timeout=15
    )

    # Sometimes Target shows a side sheet with “View cart & checkout”
    try:
        safe_click(
            context,
            By.XPATH,
            "//a[contains(.,'View cart') or contains(.,'View Cart') or contains(.,'cart & checkout')]"
            " | //button[contains(.,'View cart') or contains(.,'View Cart')]",
            timeout=6
        )
    except TimeoutException:
        # Fallback: go directly to cart page
        context.driver.get("https://www.target.com/cart")


@then("I should see at least 1 item in the cart")
def step_verify_cart_has_item(context):
    try_close_popups(context)

    # Wait for cart page to load
    wait(context, 15).until(
        EC.presence_of_element_located((By.XPATH, "//h1[contains(.,'Cart') or contains(.,'cart')]"))
    )

    # Verify cart is not empty:
    # Target often shows quantity/count, or cart line items.
    # We'll assert we can find at least one line item OR a quantity > 0.
    cart_items = context.driver.find_elements(
        By.XPATH,
        "//div[contains(@data-test,'cartItem') or contains(@data-test,'CartItem') or @data-test='cartItem']"
        " | //li[contains(@data-test,'cart-item')]"
    )

    if len(cart_items) == 0:
        # Alternate check: look for "empty cart" message; if present => fail
        empty = context.driver.find_elements(
            By.XPATH,
            "//*[contains(.,'Your cart is empty') or contains(.,'cart is empty')]"
        )
        assert len(empty) == 0, "Cart is empty (found empty cart message)."

        # Another fallback: cart count badge in header (if available)
        badges = context.driver.find_elements(
            By.XPATH,
            "//*[@data-test='cartCount' or contains(@aria-label,'cart') and contains(.,'1')]"  # best-effort fallback
        )
        assert len(badges) > 0, "Could not find cart items or a reliable cart count indicator."
    else:
        assert len(cart_items) >= 1, "Expected at least 1 cart item, but found 0."

    context.driver.quit()
