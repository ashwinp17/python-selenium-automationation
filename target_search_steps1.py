from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def close_overlays(driver):
    selectors = [
        (By.CSS_SELECTOR, "button[aria-label='close']"),
        (By.CSS_SELECTOR, "button[aria-label='Close']"),
        (By.CSS_SELECTOR, "button[data-test='closeButton']"),
        (By.CSS_SELECTOR, "button[aria-label='Close dialog']"),
    ]
    for by, sel in selectors:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, sel))).click()
            break
        except Exception:
            pass


@given('I open "{url}"')
def step_open(context, url):
    context.driver.get(url)
    context.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")


@when('I search for "{query}"')
def step_search(context, query):
    driver = context.driver
    wait = context.wait

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    close_overlays(driver)

    candidates = [
        (By.CSS_SELECTOR, 'input[type="search"]'),
        (By.CSS_SELECTOR, 'input[aria-label*="search" i]'),
        (By.CSS_SELECTOR, 'input[id*="search" i]'),
        (By.CSS_SELECTOR, 'input[name*="search" i]'),
        (By.XPATH, '//input[@type="search"]'),
    ]

    search_input = None
    for by, locator in candidates:
        try:
            search_input = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((by, locator))
            )
            if search_input.is_displayed():
                break
        except Exception:
            search_input = None

    if search_input is None:
        raise AssertionError(
            f"Could not find a search input on page. URL={driver.current_url} TITLE={driver.title}"
        )

    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.ENTER)


@then('I see search results for "{query}"')
def step_verify_results(context, query):
    # wait for URL to indicate search
    context.wait.until(lambda d: "searchTerm=" in d.current_url or "/s?" in d.current_url)
    # wait for a results grid/card to exist
    context.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-test="product-grid"], [data-test="@web/site-top-of-funnel/ProductCard"]')
        )
    )
