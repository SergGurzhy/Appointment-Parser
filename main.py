import json
import pickle
import time
import urllib

from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select

from helper import waiter
from locators import MainPage, InformationPage, ServiceSelection
from selen_driver import get_chrome_driver, get_undetected_chromedriver

test_1 = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
test_2 = 'https://www.vindecoderz.com/EN/check-lookup/ZDMMADBMXHB001652'
test_3 = 'https://anycoindirect.eu'
test_4 = 'https://otv.verwalt-berlin.de/ams/TerminBuchen'


# Функция для получения localStorage и sessionStorage
def get_storage(driver, storage_type):
    return driver.execute_script(f"""
    var items = {{}};
    for (var i = 0; i < window.{storage_type}.length; i++) {{
        var key = window.{storage_type}.key(i);
        items[key] = window.{storage_type}.getItem(key);
    }}
    return items;
    """)


def main(url):
    driver = get_chrome_driver()
    # driver = get_undetected_chromedriver()
    action = ActionChains(driver)

    driver.get(url)
    waiter(driver=driver, locator=MainPage.TERMIN_BUCHEN_BUTTON, event='clickable')
    time.sleep(2)

    # Click TERMIN BUCHEN
    driver.find_element(*MainPage.TERMIN_BUCHEN_BUTTON).click()
    waiter(driver=driver, locator=InformationPage.NEXT_BUTTON)

    # Check checkbox and click NEXT Button
    driver.find_element(*InformationPage.CHECKBOX).click()
    time.sleep(2)
    driver.find_element(*InformationPage.NEXT_BUTTON).click()
    waiter(driver=driver, locator=ServiceSelection.NATIONALITY)
    time.sleep(2)

    # Select Nationality
    nationality = Select(driver.find_element(*ServiceSelection.NATIONALITY))
    nationality.select_by_visible_text('Ukraine') # val = "166"
    waiter(driver, locator=ServiceSelection.COUNT_OF_MEMBERS)
    time.sleep(2)

    # Select Nationality
    members = Select(driver.find_element(*ServiceSelection.COUNT_OF_MEMBERS))
    members.select_by_visible_text('eine Person')
    waiter(driver, locator=ServiceSelection.IS_YOU_BERLINERS)
    time.sleep(2)

    # Select Berliner
    berliner = Select(driver.find_element(*ServiceSelection.IS_YOU_BERLINERS))
    # berliner.select_by_visible_text('ja')
    berliner.select_by_value(value='1')
    waiter(driver, locator=ServiceSelection.NATIONALITY_OF_MEMBER)
    time.sleep(2)

    # Select residents nationality
    resident = Select(driver.find_element(*ServiceSelection.NATIONALITY_OF_MEMBER))
    resident.select_by_visible_text('Ukraine')
    waiter(driver, locator=ServiceSelection.RESIDENT_PROLONG)
    time.sleep(2)

    # Click Resident Prolong
    resident = driver.find_element(*ServiceSelection.RESIDENT_PROLONG)
    next_button = driver.find_element(*ServiceSelection.WAITER)
    action.move_to_element(next_button).perform()

    action.move_to_element(resident).click(resident).perform()
    waiter(driver, locator=ServiceSelection.FAMILIE)
    time.sleep(2)

    # Open list box Paragraphs
    element = driver.find_element(*ServiceSelection.FAMILIE)
    action.move_to_element(element).click(element).perform()

    waiter(driver, locator=ServiceSelection.PARAGRAPH)
    time.sleep(2)

    # Select Paragraph 33
    driver.find_element(*ServiceSelection.PARAGRAPH).click()
    time.sleep(1)
    waiter(driver, locator=ServiceSelection.NEXT_BUTTON)
    time.sleep(2)

    # Click Next button
    button = driver.find_element(*ServiceSelection.WAITER)
    action.move_to_element(button).perform()
    action.click(button).perform()

    # button.click()
    waiter(driver, locator=ServiceSelection.NATIONALITY, direction=False)
    waiter(driver, locator=ServiceSelection.PARAGRAPH)
    time.sleep(2)

    error = driver.find_elements(*ServiceSelection.ERROR)
    # if len(error) > 0:
    #     return False
    # return True

    # Сохраняем куки, localStorage, sessionStorage и текущий URL
    cookies = driver.get_cookies()
    local_storage = get_storage(driver, "localStorage")
    session_storage = get_storage(driver, "sessionStorage")
    current_url = driver.current_url

    # Кодируем данные в формат JSON и затем в URL-формат
    cookies_json = json.dumps(cookies)
    local_storage_json = json.dumps(local_storage)
    session_storage_json = json.dumps(session_storage)

    encoded_cookies = urllib.parse.quote(cookies_json)
    encoded_local_storage = urllib.parse.quote(local_storage_json)
    encoded_session_storage = urllib.parse.quote(session_storage_json)

    # Формируем URL для восстановления сессии
    local_ip = "127.0.0.1"  # замените на ваш локальный IP
    session_restoration_url = (f"http://{local_ip}:5000/restore_session?url={urllib.parse.quote(current_url)}"
                               f"&cookies={encoded_cookies}&local_storage={encoded_local_storage}"
                               f"&session_storage={encoded_session_storage}")

    driver.quit()

    return True, session_restoration_url


if __name__ == '__main__':
    # print(main(url=test_4))

    # Пример вызова функции
    result = main(test_4)
    if result:
        success, session_restoration_url = result
        print("Success:", success)
        print("URL для восстановления сессии:", session_restoration_url)
    else:
        print("Failed to complete the process")