from selenium import webdriver
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options

class EdgeBrowser(Edge):
    def __init__(self) -> None:       
        return None
        
    @staticmethod    
    def __call__(arguments: list, prefs: dict)-> webdriver:
        option = Options()
        for argument in arguments:
            option.add_argument(argument)
        option.add_experimental_option('prefs', prefs)
        return Edge(options=option)