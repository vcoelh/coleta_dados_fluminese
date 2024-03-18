from time import sleep

from BrowserFactory import BrowserFactory
driver = BrowserFactory()(webdriver='Chrome', arguments=['--start-maximized'])
driver.get('https://curso.mairovergara.com/login')

sleep(10)