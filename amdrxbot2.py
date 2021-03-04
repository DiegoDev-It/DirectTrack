from time import sleep
import requests
import sys
import select

is_running = True
url = "https://www.amd.com/en/direct-buy/5458374100/it"
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
button = "btn-shopping-cart"

def check_availability():
    # headers are used to fool AMD website
    r = requests.get(url, headers=headers)
    if button in r.text:  # check the availability
        print("Available")
    else:
        print("Not available")

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
