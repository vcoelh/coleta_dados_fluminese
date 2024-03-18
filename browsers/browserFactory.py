from .browsers.chrome import ChromeBrowser
from .browsers.edge import EdgeBrowser
from .browsers.firefox import FirefoxBrowser

class BrowserFactory:
    '''
    Class responsable for returning Webdriver objects, these objects
    can either be Chrome(), Edge() or Firefox()
    '''
    def __call__(self, webdriver: str, arguments: list,
                 prefs : dict={'disk-cache-size': 4096}):
        
        match webdriver: 
            case 'Chrome': 
                return ChromeBrowser()(arguments, prefs)
            case 'Edge':
                return EdgeBrowser()(arguments, prefs)
            case 'Firefox':
                return FirefoxBrowser()(arguments)
    