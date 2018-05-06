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
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image


def load_driver():
    """

    Loads the webdriver and gets the page with the game
    """
    driver = webdriver.Firefox()
    driver.get("http://foddy.net/Athletics.html?webgl=true")
    return driver


def get_game(driver):
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

def update_outputs(driver, key_states):
    """

    Takes in the state of the keys 'qwop' and changes the keyup/down
    state to the browser
    """
    actions = ActionChains(driver)
    if key_states[0]:
        actions.key_down("q")
    else:
        actions.key_up("q")
    
    if key_states[1]:
        actions.key_down("w")
    else:
        actions.key_up("w")
    
    if key_states[2]:
        actions.key_down("o")
    else:
        actions.key_up("o")
    
    if key_states[3]:
        actions.key_down("p")
    else:
        actions.key_up("p")

    actions.perform()

def test_for_failed(image):
    """

    Check every frame to see if it matches a failure state in the game
    """
    pass

def main():
    """

    Run many iterations and evolve the best combination of keys and time 
    """
    driver = load_driver()
    game = get_game(driver)
    num_iterations = 10
    states = (
        (True, False, False, False),
        (True, False, False, False),
        (False, True, False, False),
        (False, True, False, False),
        (False, False, True, False),
        (False, False, True, False),
        (False, False, False, True),
        (False, False, False, True))
    try:
        for state in states:
            update_outputs(driver, state)
            time.sleep(.5)
        time.sleep(3)
    except Exception as e:
        print(e)
    finally:
        #clean up
        driver.quit()

if __name__ == "__main__":
    main()
