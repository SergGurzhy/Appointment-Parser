import json
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


# Основная функция
def main(url):
    driver = get_chrome_driver()
    action = ActionChains(driver)

    driver.get(url)
    waiter(driver=driver, locator=MainPage.TERMIN_BUCHEN_BUTTON, event='clickable')
    time.sleep(2)
    print("Initial Load")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Click TERMIN BUCHEN
    driver.find_element(*MainPage.TERMIN_BUCHEN_BUTTON).click()
    waiter(driver=driver, locator=InformationPage.NEXT_BUTTON)
    print("After Clicking TERMIN BUCHEN")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Check checkbox and click NEXT Button
    driver.find_element(*InformationPage.CHECKBOX).click()
    time.sleep(2)
    driver.find_element(*InformationPage.NEXT_BUTTON).click()
    waiter(driver=driver, locator=ServiceSelection.NATIONALITY)
    time.sleep(2)
    print("After Clicking NEXT on InformationPage")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Select Nationality
    nationality = Select(driver.find_element(*ServiceSelection.NATIONALITY))
    nationality.select_by_visible_text('Ukraine')  # val = "166"
    waiter(driver, locator=ServiceSelection.COUNT_OF_MEMBERS)
    time.sleep(2)
    print("After Selecting Nationality")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Select Nationality
    members = Select(driver.find_element(*ServiceSelection.COUNT_OF_MEMBERS))
    members.select_by_visible_text('eine Person')
    waiter(driver, locator=ServiceSelection.IS_YOU_BERLINERS)
    time.sleep(2)
    print("After Selecting Count of Members")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Select Berliner
    berliner = Select(driver.find_element(*ServiceSelection.IS_YOU_BERLINERS))
    berliner.select_by_value(value='1')
    waiter(driver, locator=ServiceSelection.NATIONALITY_OF_MEMBER)
    time.sleep(2)
    print("After Selecting Berliner")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Select residents nationality
    resident = Select(driver.find_element(*ServiceSelection.NATIONALITY_OF_MEMBER))
    resident.select_by_visible_text('Ukraine')
    waiter(driver, locator=ServiceSelection.RESIDENT_PROLONG)
    time.sleep(2)
    print("After Selecting Resident's Nationality")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Click Resident Prolong
    element = driver.find_element(*ServiceSelection.RESIDENT_PROLONG)
    action.move_to_element(element).click(element).perform()
    waiter(driver, locator=ServiceSelection.FAMILIE)
    time.sleep(2)
    print("After Clicking Resident Prolong")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Open list box Paragraphs
    element = driver.find_element(*ServiceSelection.FAMILIE)
    action.move_to_element(element).click(element).perform()
    waiter(driver, locator=ServiceSelection.PARAGRAPH)
    time.sleep(2)
    print("After Clicking Familie")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Select Paragraph 33
    driver.find_element(*ServiceSelection.PARAGRAPH).click()
    time.sleep(1)
    waiter(driver, locator=ServiceSelection.NEXT_BUTTON)
    time.sleep(2)
    print("After Selecting Paragraph 33")
    print(json.dumps(driver.get_cookies(), indent=2))

    # Click Next button
    button = driver.find_element(*ServiceSelection.WAITER)
    action.move_to_element(button).perform()
    action.click(button).perform()
    waiter(driver, locator=ServiceSelection.NATIONALITY, direction=False)
    waiter(driver, locator=ServiceSelection.PARAGRAPH)
    time.sleep(2)
    print("After Clicking Next Button")
    print(json.dumps(driver.get_cookies(), indent=2))

    error = driver.find_elements(*ServiceSelection.ERROR)
    # if len(error) > 0:
    #     driver.quit()
    #     return False

    # Сохраняем куки и текущий URL
    cookies = driver.get_cookies()
    current_url = driver.current_url

    # Сохраняем данные в файл
    session_data = {'url': current_url, 'cookies': cookies}
    with open('session_data.json', 'w') as f:
        json.dump(session_data, f)

    driver.quit()

    # Формируем URL для восстановления сессии
    encoded_session_data = urllib.parse.quote(json.dumps(session_data))
    local_ip = "127.0.0.1"  # замените на ваш локальный IP
    session_restoration_url = f"http://{local_ip}:5000/restore_session?data={encoded_session_data}"

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