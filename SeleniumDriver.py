from logger import logger
try:
    from selenium.webdriver.common.by import By
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    logger.debug("Imported Selenium.")
except Exception as e:
    logger.error(f"Could not import Selenium: {e}, exiting.")
    exit()

from time import sleep
from constants import LOGIN_DISCORD_URL, QR_ELEMENT_SELECTOR, IMAGE_LOCATION, TOKEN_GRABBER_JS

class SeleniumDriver:
    def __init__(self):
        pass

    def start(self):
        logger.debug("Starting Firefox.")
        try:
            self.driver = webdriver.Firefox()
        except Exception as e:
            logger.error(f"Could not start Firefox: {e}, exiting.")
            exit()
        logger.debug("Opening Discord login page.")
        self.driver.get(LOGIN_DISCORD_URL)
        self.getQRCodeElementAndSave()

    def getQRCodeElementAndSave(self, screenshotPath: str = IMAGE_LOCATION) -> bool:
        logger.info("Sleeping 5 seconds for QR image to load.")
        sleep(5)
        logger.debug("Searching for QR HTML element.")
        try:
            self.qr_element = self.driver.find_element(
                By.CSS_SELECTOR, "div.qrCodeContainer_c6cd4b > div.qrCode_c6cd4b")
            logger.info("Found QR element.")
        except Exception as e:
            logger.error(f"Could not find QR HTML element: {e}, exiting.")
            exit()

        logger.info("Saving QR element as PNG.")
        try:
            self.qr_element.screenshot(screenshotPath)
            logger.info(f"Saved QR element as PNG at '{screenshotPath}'.")
            return True
        except Exception as e:
            logger.error(f"Could not save image: {e}, exiting.")
            exit()

    def waitForScan(self):
        try:
            logger.info("Waiting for QR scan.")
            element = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//h2[text()='Check your phone!']"))
            )
            logger.info("User scanned QR.")
            return True
        except Exception as e:
            logger.error(f"Could not find element: {e}.")
            return False

    def waitForLogin(self):
        try:
            logger.info("Waiting for login.")
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.current_url == "https://discord.com/channels/@me"
            )
            logger.info("Detected successful login at Discord channel page.")
            return True
        except Exception as e:
            logger.error(f"Could not detect login or reach the expected URL: {e}.")
            return False

    def getToken(self):
        logger.info("Trying to retrieve token.")
        try:
            token = self.driver.execute_script(TOKEN_GRABBER_JS)
            logger.info("Token retrieved successfully.")
            return token
        except Exception as e:
            logger.error(f"Failed to get token: {e}.")
            return None

    def stop(self):
        logger.debug("Closing the browser.")
        self.driver.quit()
