from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import sys
import select

is_running = True

def check_availability():
    browser = webdriver.Firefox()  # Instantiate a new Firefox window
    browser.get("https://www.amd.com/en/direct-buy/5458374100/it")  # go to AMD website
    try:  # check if there's the Buy button
        instock = browser.find_element_by_class_name("btn-shopping-cart")
        print("Available")
    except(NoSuchElementException):  # if there isn't
        print("Not available")
    
    browser.quit()  # stop Firefox

while is_running:
    sleep(10)  
    input = select.select([sys.stdin], [], [], 1)[0]  # get input non-blocking

    if input:  # if there's some input
        value = sys.stdin.readline().rstrip()  # get the value of the input
        if value == "q":
            is_running = False  # stop the loop
            print("Exiting")
    else:  # if there isn't input
        check_availability()
