from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

class ChromeBrowser(Chrome):
    def __init__(self) -> None:
        return None       
    
    def __call__(self, arguments: list, prefs: dict)-> webdriver:
        option = Options() 
        for argument in arguments:
            option.add_argument(argument)
        option.add_experimental_option('prefs', prefs)
        return Chrome(options=option)