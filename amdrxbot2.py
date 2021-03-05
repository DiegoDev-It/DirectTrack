from time import sleep
from threading import Thread
import requests
import sys
import select

# headers are used to fool AMD website
headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
button = "btn-shopping-cart"  # the shopping button

class URLS:
    def __init__(self):
        self.urls = []
        self.availables = []
        self.names = []
    
    def add(self, url: str, name: str):
        '''
        Adds an url (AMD) and the name of the product
        '''
        self.urls.append(url)
        self.names.append(name)
        self.availables.append(False)
    
    def check_availability(self):
        '''
        Checks avialability of all added products
        '''
        for i in range(len(self.urls)):
            r = requests.get(self.urls[i], headers=headers)
            self.availables[i] = button in r.text
    
    def get_availables(self) -> list:
        '''
        Returns all available products (only name)
        '''
        availables_names = []
        for i in range(len(self.availables)):
            if self.availables[i]:
                availables_names.append(self.names[i])
        
        return availables_names

class Updater(Thread):
    def __init__(self, urls: URLS):
        Thread.__init__(self)
        self.urls = urls
    
    def run(self):
        self.urls.check_availability()


if __name__ == "__main__":
    update = True
    run = True
    urls = URLS()
    urls.add("https://www.amd.com/en/direct-buy/5458374100/it", "RX-6800XT")
    updater = Updater(urls)
    updater.start()
    while run:
        # get input non-blocking
        command = select.select([sys.stdin], [], [], 1)[0]
        if command:
            value = sys.stdin.readline().rstrip()
            value = value.split(" ")  # get the command
            if value[0] == "q":
                run = False  # stop the loop
                print("Exiting...")
            elif value[0] == "add" and len(value) == 3:  # add an url
                urls.add(value[1], value[2])
        else:
            # every loop is like tic-toc
            # tic = update
            # toc = check availibility
            if update:
                updater.run()
                update = False
            else:
                update = True
                print("Waiting for the updater...")
                updater.join()
                urls.check_availability()
                availables = urls.get_availables()  # get all availables
                if len(availables) == 0:
                    print("Nothing is available")
                else:
                    availables_str = availables[0]  # instatiate a string with the first available
                    if len(availables) > 1:  # if there are more than 1 available, add them to the string
                        for i in range(len(availables)-1):
                            availables_str = f"{availables_str}, {availables[i+1]}"
                        
                    print(f"Availables: {availables_str}")  # print all availables
        
        sleep(5)
