import os
import time
from datetime import datetime, timedelta
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from playsound import playsound
import random
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler("ticket_bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger()
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

TICKET_URL = config.get('ticket', 'TICKET_URL')
START_TIME = config.get('ticket', 'START_TIME')
NOTIFY_SOUND = config.get('ticket', 'NOTIFY_SOUND', fallback='sound.mp3')
DEBUG_RAW = config.get('ticket', 'DEBUG', fallback='0').strip().lower()
DEBUG = DEBUG_RAW in ('1', 'true')
BROWSER = config.get('ticket', 'BROWSER', fallback='chrome').strip().lower()

log.info(f"Opening browser ({BROWSER}) and navigating to ticket page...")
driver = None
if BROWSER == 'chrome':
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
elif BROWSER == 'edge':
    from selenium.webdriver.edge.service import Service as EdgeService
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
    driver = EdgeDriver(service=EdgeService(EdgeChromiumDriverManager().install()))
else:
    log.error(f"Unsupported browser: {BROWSER}. Please use 'chrome' or 'edge'.")
    exit(1)
driver.get(TICKET_URL)

button_clicked = False

def wait_for_browser_close(driver):
    import sys
    while True:
        try:
            if not driver.window_handles:
                log.info("Browser window closed by user. Exiting program.")
                driver.quit()
                sys.exit()
        except Exception:
            log.info("Browser window closed by user (exception). Exiting program.")
            try:
                driver.quit()
            except Exception:
                pass
            sys.exit()
        time.sleep(1)

def find_and_click_buy(driver, max_attempts=None):
    attempts = 0
    while True:
        # Auto-exit if browser is closed
        try:
            if not driver.window_handles:
                log.info("Browser window closed by user. Exiting program.")
                driver.quit()
                exit()
        except Exception:
            log.info("Browser window closed by user (exception). Exiting program.")
            try:
                driver.quit()
            except Exception:
                pass
            exit()
        try:
            button = driver.find_element(By.CLASS_NAME, "load-button")
            button.click()
            log.info("Buy button clicked!")
            return True
        except Exception as e:
            attempts += 1
            log.debug(f"Buy button not found, attempt {attempts}.")
            if max_attempts and attempts >= max_attempts:
                return False
            time.sleep(0.1)

def main():
    button_clicked = False
    if not DEBUG:
        start_time = datetime.strptime(START_TIME, '%Y-%m-%d %H:%M:%S')
        log.info(f"Waiting until {start_time - timedelta(seconds=1)} to start refresh loop...")
        while datetime.now() < start_time - timedelta(seconds=1):
            time_left = (start_time - datetime.now()).total_seconds()
            log.info(f"Time left: {int(time_left)} seconds")
            if time_left > 10:
                time.sleep(1)
            else:
                time.sleep(0.1)
        log.info("Starting 0.1s refresh loop until sale starts...")
        while datetime.now() < start_time:
            try:
                if find_and_click_buy(driver, max_attempts=1):
                    button_clicked = True
                    break
            except Exception:
                pass
            driver.refresh()
            time.sleep(0.1)
        # After sale start, keep searching and refreshing until buy is pressed
        while not button_clicked:
            if find_and_click_buy(driver, max_attempts=1):
                button_clicked = True
                break
            driver.refresh()
            time.sleep(0.1)
    else:
        log.info("Debug mode enabled: ignoring start time, searching for Buy button.")
        while not button_clicked:
            if find_and_click_buy(driver, max_attempts=2):
                button_clicked = True
                break
            log.info("Buy button not found in 2 attempts, refreshing page (debug mode)...")
            driver.refresh()
            time.sleep()
    # Notify user
    log.info("Buy button pressed! Notifying user with sound...")
    try:
        playsound(NOTIFY_SOUND)
    except Exception as e:
        log.warning(f"Could not play sound: {e}")
    log.info("Please complete the purchase manually. Close browser to exit.")
    wait_for_browser_close(driver)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Stopped by user.")
        driver.quit()
        exit()
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        driver.quit()
        exit()
