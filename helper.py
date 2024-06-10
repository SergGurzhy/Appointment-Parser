from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waiter(driver, locator, event='visible', direction=True):
    wait = WebDriverWait(driver, 30)
    if event == 'visible' and direction is True:
        wait.until(EC.visibility_of_element_located(locator))
    elif event == 'visible' and direction is False:
        wait.until(EC.invisibility_of_element_located(locator))
    else:
        wait.until(EC.element_to_be_clickable(locator))
