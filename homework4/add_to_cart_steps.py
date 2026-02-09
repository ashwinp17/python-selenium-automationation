from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


TARGET_URL = "https://www.target.com/"


def w(context, timeout=25):
    return WebDriverWait(context.driver, timeout)


def close_popups(context):
    # Best-effort popup closers (ignore if not present)
    candidates = [
        (By.XPATH, "//button[@aria-label='Close']"),
        (By.XPATH, "//button[contains(.,'Accept')]"),
        (By.XPATH, "//button[contains(.,'I agree')]"),
        (By.XPATH, "//button[contains(.,'Got it')]"),
    ]
    for loc in candidates:
        try:
            w(context, 3).until(EC.element_to_be_clickable(loc)).click()
        except Exception:
            pass


@given("I open Target home page")
def step_open_target_home(context):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--start-maximized")

    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    context.driver.get(TARGET_URL)
    close_popups(context)

    # Wait until search box exists to confirm page is ready
    w(context).until(EC.presence_of_element_located((By.ID, "search")))


@when('I search for "{query}"')
def step_search_for_query(context, query):
    close_popups(context)

    search_box = w(context).until(EC.element_to_be_clickable((By.ID, "search")))
    search_box.clear()
    search_box.send_keys(query)

    search_btn = w(context).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='@web/Search/SearchButton']"))
    )
    search_btn.click()

    # Wait for results page
    w(context).until(EC.url_contains("/s"))


from urllib.parse import urljoin

from urllib.parse import urljoin

@when("I open the first product result")
def step_open_first_product(context):
    close_popups(context)

    w(context).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href,'/p/')]")))
    anchors = context.driver.find_elements(By.XPATH, "//a[contains(@href,'/p/')]")

    hrefs = []
    for a in anchors:
        href = a.get_attribute("href")
        if href and "/p/" in href:
            hrefs.append(urljoin("https://www.target.com", href))

    # de-dupe
    seen = set()
    hrefs = [h for h in hrefs if not (h in seen or seen.add(h))]

    assert hrefs, "No product links found on results page."

    # Try a handful until we find a product page that has an add-type button
    addable_xpath = (
        "//button["
        "(@data-test='addToCartButton' or @id='addToCartButton' or "
        "contains(.,'Add to cart') or contains(.,'Ship it') or contains(.,'Pick it up') or contains(.,'Add for shipping'))"
        " and not(contains(.,'Notify')) and not(contains(.,'Out of stock'))"
        " and not(@disabled) and not(@aria-disabled='true')"
        "]"
    )

    for url in hrefs[:12]:
        context.driver.get(url)
        close_popups(context)

        # Ensure it's a product page
        try:
            title = w(context, 8).until(EC.presence_of_element_located((By.XPATH, "//h1")))
            context.product_title = title.text.strip()
        except Exception:
            continue

        # If an add-type button appears, we found a usable product
        try:
            w(context, 8).until(EC.presence_of_element_located((By.XPATH, addable_xpath)))
            return
        except Exception:
            continue

    raise AssertionError("Could not find a product page with an Add-to-cart style button from the search results.")

from selenium.common.exceptions import TimeoutException

from selenium.common.exceptions import TimeoutException

@when("I add the product to the cart")
def step_add_product_to_cart(context):
    close_popups(context)
    w(context, 25).until(EC.presence_of_element_located((By.XPATH, "//h1")))

    def click_first_add_button():
        # Prefer stable selectors first
        candidates = [
            (By.CSS_SELECTOR, "button[data-test='addToCartButton']"),
            (By.CSS_SELECTOR, "button#addToCartButton"),
            (By.XPATH, "//button[contains(.,'Add to cart')]"),
            (By.XPATH, "//button[contains(.,'Add for shipping')]"),
            (By.XPATH, "//button[contains(.,'Ship it')]"),
            (By.XPATH, "//button[contains(.,'Pick it up')]"),
        ]

        for by, value in candidates:
            try:
                btn = w(context, 4).until(EC.presence_of_element_located((by, value)))
                if btn.is_displayed():
                    context.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    try:
                        w(context, 4).until(EC.element_to_be_clickable((by, value)))
                        btn.click()
                    except Exception:
                        context.driver.execute_script("arguments[0].click();", btn)
                    return True
            except Exception:
                continue
        return False

    def select_first_variant_if_any():
        # Best-effort click something selectable (size/flavor/etc.)
        variant_xpaths = [
            "//button[@role='radio' and not(@aria-disabled='true')]",
            "//label[.//input[@type='radio' and not(@disabled)]]",
            "//button[contains(@data-test,'variation') and not(@disabled)]",
        ]
        for xp in variant_xpaths:
            els = context.driver.find_elements(By.XPATH, xp)
            for el in els[:10]:
                if el.is_displayed():
                    context.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                    try:
                        el.click()
                    except Exception:
                        context.driver.execute_script("arguments[0].click();", el)
                    return True
        return False

    def wait_for_added_confirmation():
        # Any of these indicates the add actually happened
        confirm_locators = [
            (By.XPATH, "//*[contains(.,'Added to cart') or contains(.,'added to your cart')]"),
            (By.XPATH, "//a[contains(@href,'/cart') and (contains(.,'View cart') or contains(.,'cart'))]"),
            # Cart count badge sometimes exists
            (By.XPATH, "//*[(@data-test='cartItemCount' or contains(@aria-label,'cart')) and contains(.,'1')]"),
        ]
        for loc in confirm_locators:
            try:
                w(context, 6).until(EC.presence_of_element_located(loc))
                return True
            except Exception:
                continue
        return False

    # Try click add
    clicked = click_first_add_button()

    # If no button found/clicked, try selecting a variant and try again
    if not clicked:
        select_first_variant_if_any()
        close_popups(context)
        clicked = click_first_add_button()

    assert clicked, "Could not click any Add/Ship/Pick button on the product page."

    # Confirm it was added (or at least UI indicates it)
    confirmed = wait_for_added_confirmation()

    # If not confirmed, one more variant selection + retry
    if not confirmed:
        select_first_variant_if_any()
        close_popups(context)
        click_first_add_button()
        confirmed = wait_for_added_confirmation()

    assert confirmed, (
        "Clicked an add button but no confirmation appeared. "
        "Target likely required fulfillment/variant choice or the item couldn't be added."
    )

    # If View cart appears, click it to land in cart reliably
    try:
        view_cart = w(context, 8).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/cart') and (contains(.,'View cart') or contains(.,'cart'))]"))
        )
        view_cart.click()
    except TimeoutException:
        pass



@then("I open the cart")
def step_open_cart(context):
    close_popups(context)
    context.driver.get("https://www.target.com/cart")
    w(context).until(EC.url_contains("/cart"))


from selenium.common.exceptions import TimeoutException
import re

@then("the cart is not empty")
def step_cart_not_empty(context):
    close_popups(context)

    # Make sure we are on the cart page
    w(context, 20).until(EC.url_contains("/cart"))

    # --- Strategy A: Look for an "empty cart" message (fast fail) ---
    empty_markers = [
        "your cart is empty",
        "cart is empty",
        "no items in your cart",
    ]
    page_text = context.driver.page_source.lower()
    if any(m in page_text for m in empty_markers):
        raise AssertionError("Cart appears to be empty (empty-cart message detected).")

    # --- Strategy B: Try multiple cart-item locators (Target changes these a lot) ---
    cart_item_locators = [
        # data-test patterns (commonly used by Target)
        (By.XPATH, "//*[contains(@data-test,'cartItem') or contains(@data-test,'CartItem')]"),
        # common container roles/classes
        (By.XPATH, "//*[@role='listitem' and (contains(.,'Qty') or contains(.,'Quantity') or contains(.,'$'))]"),
        (By.XPATH, "//*[contains(@class,'CartItem') or contains(@class,'cartItem')]"),
        # product title links inside cart
        (By.XPATH, "//a[contains(@href,'/p/')]"),
        # quantity selector often exists per line item
        (By.XPATH, "//*[contains(@aria-label,'quantity') or contains(@aria-label,'Quantity')]"),
    ]

    found_items = False
    for by, value in cart_item_locators:
        try:
            els = w(context, 6).until(EC.presence_of_all_elements_located((by, value)))
            # Filter to visible elements to avoid hidden templates
            visible = [e for e in els if e.is_displayed()]
            if len(visible) >= 1:
                found_items = True
                break
        except TimeoutException:
            continue

    if found_items:
        # Optional: verify product title appears somewhere
        if getattr(context, "product_title", None):
            assert context.product_title.lower()[:15] in context.driver.page_source.lower(), (
                f"Expected product title to appear in cart. Title was: {context.product_title}"
            )
        context.driver.quit()
        return

    # --- Strategy C: Parse "X items" from cart header (fallback) ---
    # This is a last resort when DOM is heavily obfuscated.
    m = re.search(r"(\d+)\s+items?", page_text)
    if m and int(m.group(1)) >= 1:
        context.driver.quit()
        return

    # If we got here, we couldn't prove items exist
    raise AssertionError(
        "Could not confirm cart has items: no cart-item elements matched, and no item count text found."
    )
