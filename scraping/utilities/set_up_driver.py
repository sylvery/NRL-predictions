"""
Module to set up Chrome Web Driver for Web Scraping.

This module provides a function to set up the Chrome WebDriver with specific options
for automated web scraping tasks related to NRL data collection.
"""

import logging
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

chromedriver_autoinstaller.install()


def set_up_driver():
    """Set up the Chrome Web Driver for web scraping.

    This function sets up the Chrome WebDriver with specified options.
    
    :return: WebDriver object for Chrome
    """
    logger.info("Setting up Chrome WebDriver...")
    
    options = Options()
    # Ignore certificate errors from the NRL website
    options.add_argument('--ignore-certificate-errors')
    
    # Run Selenium in headless mode
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    
    # Exclude logging to assist with errors caused by NRL website
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Additional options for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    driver = webdriver.Chrome(options=options)
    logger.info("Chrome WebDriver initialized successfully")
    
    return driver


def quit_driver(driver):
    """Quit the WebDriver and cleanup resources.
    
    :param driver: WebDriver instance to quit
    """
    if driver:
        logger.info("Quitting Chrome WebDriver...")
        driver.quit()
        logger.info("WebDriver quit successfully")
