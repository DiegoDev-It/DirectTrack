import time
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
while True:
        browser = webdriver.Firefox()
        browser.get("https://www.amd.com/en/direct-buy/5458374100/it")
        try:
            instock = browser.find_element_by_class_name("btn-shopping-cart")
            if instock:
                print("Disponibile")
        except(NoSuchElementException):
            print("Non disponibile")
            browser.quit()
            time.sleep(5.5)

                
