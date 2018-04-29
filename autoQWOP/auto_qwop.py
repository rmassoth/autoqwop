"""

A fun program to automate the web game QWOP.
It will utilize scikit-learn for the neural net
automation and selenium for web browser automation.
"""
import time
import io

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from PIL import Image


def load_game():
    """

    Loads the webdriver and gets the page with the game
    """
    driver = webdriver.Firefox()
    driver.get("http://foddy.net/Athletics.html?webgl=true")
    return driver


def setup(driver):
    """

    Initialize the browser and click the game window to get started
    """
    try:
        game = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "window1")))
        print("Game window found")
        time.sleep(5)
        game.click()
        return game
    except TimeoutException:
        print("Game took too much time to load!")
        return False


def get_frame(game):
    """

    Gets a single frame of the game as a png file and returns it
    """
    image = Image.open(io.BytesIO(game.screenshot_as_png))
    return image

def main():
    """

    Where the magic happens
    """
    driver = load_game()
    game = setup(driver)
    if game:
        print(game)
        time.sleep(5)
        driver.quit()
    else:
        #clean up
        driver.quit()

if __name__ == "__main__":
    main()
