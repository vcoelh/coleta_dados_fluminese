import logging 

class LoggerClass:    
    def __init__(self, log_file = 'debug.log', log_level = 'INFO'):
        log_format = "%(asctime)s:[%(levelname)s]: %(message)s"
        self.logger = logging.getLogger(log_file)
                
        # Create a FileHandler to write log messages to the specified log file
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(file_handler)
        
        match log_level:
            case "INFO":
                return self.logger.setLevel(logging.INFO)
            case "ERROR":
                return self.logger.setLevel(logging.ERROR)
            case "DEBUG":
                return self.logger.setLevel(logging.DEBUG)
    
    
    def info(self, message: str):
        self.logger.info(message)
        
    def error(self, message: str):
        self.logger.error(message)