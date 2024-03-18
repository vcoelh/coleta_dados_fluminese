import yaml
from re import findall

from pandas import concat, DataFrame
from tqdm import tqdm

from utils.helper import DataBuilder, DataReader
from utils.scraper import Scraper



class Collect:
    def collect(self, sheet):
        if 'multiclubes' in sheet['URL DO INSUMO'].iloc[0]:
            return Collect0().collect(sheet=sheet)
        return Collect1().collect(sheet)


class Collect0(Scraper):
    def __init__(self,
                 Ship: bool = False,
                 Browser: bool = True,
                 WebDriver: str = 'Edge',
                 Options: list =['window-size=1920,1080', 'headless'],
                 Prefs: dict = {'disk-cache-size': 4096},
                 Wait: int = 5,
                 Log_file: str = 'debug.log',
                 Log_level: str = 'INFO',
                ) -> None:
        super().__init__(Ship, Browser,
                         WebDriver, Options,
                         Prefs, Wait,
                         Log_file, Log_level
                        )
                                                      
    def _get_screenshot(self, sheet, zoom_size: int = 1, folder_prints: str =   'prints') -> None:
         cod1,cod2 = sheet['NR_SEQ_INSINF']
         informant_code = f'{cod1}_{cod2}'        
         return super().get_screenshot(informant_code, zoom_size, folder_prints)
    
    def _get_value(self, sheet: DataFrame, by: str = 'css selector',
                   locator: str = None
                   ):
        elements = self.driver.find_elements(by, locator)
        texts = [e.text for e in elements]
        sheet['preco_coleta'] = [
            findall(r'(\d+,\d{2}) Mensais', e)[0] for e in texts
            ]
        
        return sheet
    
    def collect(self, sheet: DataFrame) -> DataFrame:
            url = sheet['URL DO INSUMO'].iloc[0]
            print('\nURL: ', url)
            self.go(url, append=True)
            sheet = self._get_value(
                locator='.full-button .data',
                sheet=sheet
            )
            self._get_screenshot(
                sheet=sheet,
                zoom_size=1.1
            )
            return sheet
        

class Collect1(Scraper):
    def __init__(self,
                 Ship: bool = False,
                 Browser: bool = True,
                 WebDriver: str = 'Chrome',
                 Options: list =['window-size=1920,1080', 'headless'],
                 Prefs: dict = {'disk-cache-size': 4096},
                 Wait: int = 5,
                 Log_file: str = 'debug.log',
                 Log_level: str = 'INFO',
                ) -> None:
        super().__init__(Ship, Browser,
                         WebDriver, Options,
                         Prefs, Wait,
                         Log_file, Log_level
                        )
                                 
    def collect(self, sheet: DataFrame) -> DataFrame:

        for _, item in tqdm(sheet.iterrows(), total=sheet.shape[0]):
            url = item['URL DO INSUMO']
            print('\nURL: ', url)
            self.go(url, append=False)
            
            self.get_value(
                locator='.item:nth-child(1) .green+ .green',
                value='PRDCT',
            )
            
            print('\nCOD: ', item['NR_SEQ_INSINF'])
            self.get_screenshot(
                inform_cod=item['NR_SEQ_INSINF'],
                zoom_size=1,
            )
        cargo = self.generate_cargo(sheet)
        return cargo
    
if __name__ == '__main__':
    with open('config.yml') as file:
        CONFIG = yaml.safe_load(file)

    informant_cod = CONFIG['informant_cod']
    name_folder = CONFIG['name_folder']
    date_filter = CONFIG['date_filter']

    
    data_reader = DataReader()
    data_reader.create_folder(name_folder=name_folder,
        informant_code=informant_cod)
    
    sheet = data_reader.read_table(informant_code=informant_cod,
        date_filter=date_filter)

    collects = []
    sheet0 = sheet[sheet['URL DO INSUMO'].str.contains('multiclubes')]
    sheet1 = sheet[~(sheet['URL DO INSUMO'].str.contains('multiclubes'))]
    
    sheets = [sheet0, sheet1]
    for sheet in sheets:
        collects += [Collect().collect(sheet)]
        
    collect = concat(collects, ignore_index=True)
    DataBuilder().load_creator(sheet=collect, name_website=name_folder,
        informant_code=informant_cod)
