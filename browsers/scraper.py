from datetime import datetime
from time import sleep
from re import findall
from os import path

from pandas import DataFrame
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .browserFactory import BrowserFactory
from .logger import LoggerClass


class Scraper(LoggerClass):
    '''
    This class has some very necessary methods  
    in every automatization using the Selenium library
    
    '''  
    def __init__(self,
                 SHIP: bool = False, 
                 Browser: bool = True,
                 WebDriver: str = 'Chrome',
                 Options: list = ['--start-maximized'],
                 Prefs: dict = {'disk-cache-size': 4096},
                 Wait: int = 5,
                 Log_file: str ='debug.log', 
                 Log_level: str ='INFO'
                 ) -> None:
        
        super().__init__(Log_file, Log_level)
      
        self.ship = SHIP
        
        if Browser:
            self.driver = BrowserFactory()(webdriver=WebDriver,
                                           arguments=Options, prefs=Prefs)
            self.wait = WebDriverWait(self.driver, Wait)
        
        self.product_price = [] 
        if self.ship: self.ship_price = []
  
    def get_value(self, by: str='css selector',
                  locator: str=None, value: str=None):
        '''
        Method responsable for getting price either for the 
        product or for the shipment and adding it to the list
        
        '''    
        try:
            text = self.driver.find_element(
                    by,locator
                ).text
            print(f'\nTEXT {value}: {text}')
            price = findall(r'R?\$?\s?(\d*\.?,?\d+,?\.?\d+)', text)[0]
            
            print(f'\n{value} PRICE COLLECTED: {price}')
        except Exception as e:
            print(f'\nERROR GET VALUE {value}: {e}')
            price = ''
            
        match value:
            case 'PRDCT': self.product_price.append(price)
            case 'SHIP': self.ship_price.append(price)

    def insert_value(
                    self,
                    by: str='css selector', 
                    locator: str=None, insert: str=None, 
                    value: str=None, clear: bool=False, 
                    click: bool=False, enter: bool=True
                    ) -> None:
        
        '''
        Method responsable for inserting some value, 
        either the quantity or the cep
        
        '''
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    (by,locator)
                    )
                )
            
            if click: element.click()
            
            if clear: element.clear()
            sleep(0.25)
            element.send_keys(value)
            
            if enter: element.send_keys(Keys.ENTER)
            
            self.info(f'SEND VALUE: {value}')
        
        except Exception as e:
            self.error(f'ERROR INSERT {insert}: {e}')

    def select_packet(self, by: str='css selector', 
                       locator: str=None, dict_spcs: list=[...]
                       ) -> None:
        try:
            elements = self.wait.until(
                EC.visibility_of_element_located(
                       (by, locator)
                    )
                )
            
            for element in elements:
                if element.text in dict_spcs: element.click()
                else: pass
        
        except Exception as e:
            self.error(f'ERROR SELECT PACKET {e}')

    def click(
             self, 
             by: str='css selector', 
             locator: str=None, 
             click: str=None,
             append_product_price: bool=False,
             append_ship_price: bool=False,
             ) -> bool:

        try:
            self.driver.find_element(
                    by, locator
                    ).click()
            return True
        
        except Exception as e:
            self.error(f'ERROR CLICK {click} {e}')
            
            if append_product_price: self.product_price.append('')
            if append_ship_price: self.ship_price.append('')
            return False

    def get_screenshot(self, inform_cod: str,
                       zoom_size: int = 1,
                       folder_prints: str = 'prints') -> None:
        '''
        Method responsable for getting a screenshot of the current page
        
        '''
        try:
            file_path = path.abspath(
                   folder_prints) + (f"\\{inform_cod}_"
                   f" {datetime.now().strftime('%d_%m_%Y')}.png")
            
            self.driver.execute_script(
                f"document.body.style.zoom={zoom_size}"
                )
            
            self.driver.save_screenshot(file_path)
            
            self.driver.execute_script("document.body.style.zoom=1")
            print('\nSCREENSHOT: ', file_path)
        except Exception as e:
            self.error(f'\nERROR GET SCREENSHOT: {e}')
   
    def go(self, url: str, append: bool = True) -> bool:
        '''
        Method responsable for going to the webpage,
        if the url isn't correct it'll append '' 
        to the product/ship price and return False by 
        default 
        
        Usually this method is used with a 
        if not condictional within 
        a for loop
        
        Ex.:
        
        for _, item in sheet.iterrows():
            if not go(url=item['URL']): continue 
        
        '''
        
        self.info(f'URL: {url}')
        try:
            self.driver.get(url=url)
            return True
        except Exception as e:
            self.error(f'ERROR GO URL {e}')
            if append:
                self.product_price.append('')
                if self.ship: self.ship_price.append('')
            return False

    def generate_cargo(self, sheet: DataFrame) -> DataFrame:
        '''
        Method responsable for adding the products prices or/and 
        the shipment prices collected in the sheet  
        
        '''
        
        
        sheet['preco_coleta'] = self.product_price
        if self.ship: sheet['frete_coleta'] = self.ship_price
        return sheet

    def scroll(self, Page: str,
               qtd: int = 1, by: str='xpath',
               locator: str="//html" 
            ):
        
        scroll: dict = {
            'DOWN': Keys.PAGE_DOWN,
            'UP': Keys.PAGE_UP,
            }
        
        for _ in range(qtd):
            self.wait.until(
                EC.visibility_of_element_located(
                    (by, locator)
                )
            ).send_keys(scroll[Page])

    def insert_cookie(self,
                      name: str=None,
                      value: str=None)-> None:
        try:
            self.driver.add_cookie(
                {'name': name, 'value': value}
                )
            self.driver.refresh()
        except Exception as e: 
            self.info(f'ERROR INSERT COOKIE: {e} ')   