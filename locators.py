from selenium.webdriver.common.by import By


class MainPage:
    TERMIN_BUCHEN_BUTTON = (By.XPATH, "//div//a[contains(text(),'Termin buchen')]")


class InformationPage:
    CHECKBOX = (By.XPATH, "//input[contains(@id,'xi-cb-1')]")
    NEXT_BUTTON = (By.XPATH, "//button[contains(@id,'applicationForm:managedForm:proceed')]")


class ServiceSelection:
    NATIONALITY = (By.XPATH, "//select[contains(@id,'xi-sel-400')]")
    COUNT_OF_MEMBERS = (By.XPATH, "//select[contains(@id,'xi-sel-422')]")
    IS_YOU_BERLINERS = (By.XPATH, "//select[contains(@id,'xi-sel-427')]")
    NATIONALITY_OF_MEMBER = (By.XPATH, "//select[contains(@id,'xi-sel-428')]")

    RESIDENT_PROLONG = (By.XPATH, "//label[contains(@for,'SERVICEWAHL_DE3166-0-2')]")
    FAMILIE = (By.XPATH, "//label[contains(@for,'SERVICEWAHL_DE_166-0-2-4')]")
    PARAGRAPH = (By.XPATH, "//label[contains(@for,'SERVICEWAHL_DE166-0-2-4-305289')]") # Выбор уже в меню
    NEXT_BUTTON = (By.XPATH, "//button[contains(@id,'applicationForm:managedForm:proceed')]")
    WAITER = (By.XPATH, "//button[contains(@id, 'applicationForm:managedForm:proceed')]") # applicationForm:managedForm:proceed

    ERROR = (By.XPATH, "//li[contains(@class,'errorMessage')]")
