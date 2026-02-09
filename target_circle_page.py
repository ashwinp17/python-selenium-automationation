from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TargetCirclePage:
    URL = "https://www.target.com/circle"

    HEADING = (By.XPATH, "//h2[normalize-space()='Unlock added value']")

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)

    def _scroll_to_heading(self):
        h = self.wait.until(EC.presence_of_element_located(self.HEADING))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", h)
        self.wait.until(EC.visibility_of_element_located(self.HEADING))
        return h

    def unlock_added_value_tile_count(self) -> int:
        heading = self._scroll_to_heading()

        # Get the nearest container that holds the two tiles.
        # On Target pages, the 2 promo tiles are typically <a> elements in the first section/div after the heading.
        container = self.driver.execute_script(
            """
            const h = arguments[0];
            // Move up a bit to a stable wrapper
            const wrapper = h.closest('section, div');
            // Then look for the next block-level container after the heading area
            // that actually contains multiple links (the tiles).
            let n = wrapper;
            for (let i=0; i<6 && n; i++) {
              // candidate: next sibling that contains at least 2 visible links
              let sib = n.nextElementSibling;
              while (sib) {
                const links = Array.from(sib.querySelectorAll('a'))
                  .filter(a => a.offsetParent !== null);
                if (links.length >= 2) return sib;
                sib = sib.nextElementSibling;
              }
              n = n.parentElement;
            }
            return null;
            """,
            heading
        )

        if not container:
            raise AssertionError('Could not locate the tiles container under "Unlock added value"')

        # Count only the *top-level* visible tile links inside that container.
        # The two big tiles are usually the largest visible links; we filter small/nav links out by size.
        tiles = self.driver.execute_script(
            """
            const c = arguments[0];
            const links = Array.from(c.querySelectorAll('a'))
              .filter(a => a.offsetParent !== null);

            // Keep only "tile-like" links by size (big clickable cards)
            const big = links.filter(a => {
              const r = a.getBoundingClientRect();
              return r.width > 200 && r.height > 200; // tiles are large
            });

            return big.length;
            """,
            container
        )

        return int(tiles)
