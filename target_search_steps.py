from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT = 15


@given('I open "{url}"')
def step_open(context, url):
    context.driver.get(url)


@when('I search for "{term}"')
def step_search(context, term):
    driver = context.driver
    wait = WebDriverWait(driver, WAIT)

    search_input = wait.until(EC.element_to_be_clickable((By.ID, "search")))
    search_input.clear()
    search_input.send_keys(term)

    search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    search_btn.click()


@then('search results for "{term}" are shown')
def step_verify_results(context, term):
    driver = context.driver
    wait = WebDriverWait(driver, WAIT)

    wait.until(lambda d: term.lower() in d.current_url.lower())
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/p/')]")))


from selenium.common.exceptions import StaleElementReferenceException

@then('I see 2 storycards under "{heading_text}"')
def step_circle_storycards(context, heading_text):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    heading_xpath = "//*[self::h1 or self::h2 or self::h3][normalize-space()='" + heading_text + "']"
    wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath)))

    region_xpaths = [
        heading_xpath + "/following::*[self::section or self::div][1]",
        heading_xpath + "/following::*[self::section or self::div][2]",
        heading_xpath + "/following::*[self::section or self::div][3]",
    ]

    def count_tiles(region):
        tile_candidates = region.find_elements(
            By.XPATH,
            ".//*[self::a or self::button][.//*[self::img or self::h2 or self::h3 or self::h4]]"
        )
        tile_candidates = [e for e in tile_candidates if e.is_displayed()]
        return len(tile_candidates)

    last = 0
    for _ in range(5):
        try:
            best = 0
            for rx in region_xpaths:
                region = driver.find_element(By.XPATH, rx)
                best = max(best, count_tiles(region))
            last = best
            if best >= 2:
                return
        except WebDriverException:
            continue

    assert False, f"Expected 2 storycards under '{heading_text}', but found {last}."
