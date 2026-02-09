from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


@given("I open the Target Circle page")
def step_open_target_circle(context):
    context.driver.get("https://www.target.com/circle")

    # Wait until page has some stable content (header search box usually appears)
    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[aria-label*='search' i]"))
    )

    # Best-effort close common overlays (cookies / location / sign-in prompts)
    _dismiss_overlays(context)


from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


from behave import then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@then('I see {expected_count:d} storycards under "{section_title}"')
def step_verify_storycards_under_section(context, expected_count, section_title):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    heading_xpath = (
        "//*[self::h1 or self::h2 or self::h3 or self::div or self::p]"
        f"[normalize-space()='{section_title}']"
    )
    heading = wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", heading)
    time.sleep(0.8)

    # IMPORTANT: only consider tiles *after* the heading in document order,
    # and only within a limited window (next ~30 anchors with images).
    candidates_xpath = (
        f"({heading_xpath})"
        "/following::a[.//img or .//picture][position()<=30]"
    )

    candidates = driver.find_elements(By.XPATH, candidates_xpath)
    visible = [el for el in candidates if el.is_displayed()]

    # Keep only big tiles, then take the first N of them (this avoids grabbing tiles from the next section).
    big_tiles = []
    for el in visible:
        sz = el.size
        if sz["width"] >= 250 and sz["height"] >= 180:
            big_tiles.append(el)
        if len(big_tiles) == expected_count:
            break

    actual = len(big_tiles)

    assert actual == expected_count, (
        f'Expected {expected_count} storycards under "{section_title}", '
        f"but found {actual}. (Candidates={len(candidates)}, Visible={len(visible)})"
    )


def _dismiss_overlays(context):
    """
    Best-effort: closes common Target popups (cookies/location/sign-in).
    Safe if nothing appears.
    """
    driver = context.driver
    wait = WebDriverWait(driver, 2)

    xpaths = [
        # Generic close buttons
        "//button[@aria-label='Close' or @aria-label='close' or @title='Close']",
        # Cookie banners / accept buttons
        "//button[contains(.,'Accept') or contains(.,'I Accept') or contains(.,'Got it')]",
        # Dialog close buttons
        "//*[@role='dialog']//button[contains(@aria-label,'Close') or contains(@aria-label,'close')]",
    ]

    for xp in xpaths:
        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            time.sleep(0.2)
        except TimeoutException:
            pass
        except Exception:
            pass
