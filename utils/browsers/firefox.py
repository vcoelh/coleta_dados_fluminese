from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

class FirefoxBrowser(Firefox):
    def __init__(self) -> None:
        return None
    
    @staticmethod
    def __call__(arguments: list = ['--start-maximized'])-> webdriver:
        option = Options()
        for argument in arguments:
            option.add_argument(argument)
        return Firefox(options=option)      