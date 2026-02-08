from behave import given, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given('I open the product page "{url}"')
def step_open_product(context, url):
    context.driver.get(url)


@then("I can select every color option and it becomes selected")
def step_select_all_colors(context):
    driver = context.driver
    wait = WebDriverWait(driver, 15)

    color_section = wait.until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//*[self::section or self::div][.//*[normalize-space()='Color' or contains(normalize-space(),'Color')]]")
        )
    )

    def get_swatches():
        return color_section.find_elements(
            By.XPATH,
            ".//button[@aria-label] | .//*[@role='radio']"
        )

    swatches = get_swatches()
    assert swatches, "No color swatches found. Update the locator to match the page."

    for i in range(len(swatches)):
        swatches = get_swatches()
        swatch = swatches[i]

        name = swatch.get_attribute("aria-label") or swatch.text or f"swatch[{i}]"

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", swatch)
        wait.until(EC.element_to_be_clickable(swatch)).click()

        def is_selected(el):
            aria_pressed = (el.get_attribute("aria-pressed") or "").lower()
            aria_checked = (el.get_attribute("aria-checked") or "").lower()
            cls = (el.get_attribute("class") or "").lower()
            return (
                aria_pressed == "true"
                or aria_checked == "true"
                or "selected" in cls
                or "active" in cls
            )

        wait.until(lambda d: is_selected(get_swatches()[i]))
        print(f"Selected color OK: {name}")
