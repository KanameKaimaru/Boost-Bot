import logging
from colorama import Fore, Style

def setup_logger():
    logger = logging.getLogger("BoostBot")
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        f"{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} {Fore.MAGENTA}[%(levelname)s]{Style.RESET_ALL} %(message)s",
        datefmt="%H:%M:%S"
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    return logger