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
from selenium.webdriver.common.keys import Keys

from PIL import Image
import numpy as np

from genetic import *


class AUTOQWOP:
    """

    Class to wrap all the methods for automatically playing the game QWOP
    """
    
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.game = None

    def __del__(self):
        self.driver.quit()


    def load_website(self):
        """

        Loads the webdriver and gets the page with the game
        """
        self.driver.get("http://foddy.net/Athletics.html?webgl=true")


    def get_game(self):
        """

        Initialize the browser and click the game window to get started
        """
        try:
            self.game = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "window1")))
            print("Game window found")
            time.sleep(5)
            self.game.click()
        except TimeoutException:
            print("Game took too much time to load!")


    def get_frame(self):
        """

        Gets a single frame of the game as a png file and returns it
        """
        image = Image.open(io.BytesIO(self.game.screenshot_as_png))
        return image

    def update_outputs(self, key_state):
        """

        Takes in the state of the keys 'qwop' and changes the keyup/down
        state to the browser
        """

        actions = ActionChains(self.driver)
        if key_state == '0':
            actions.key_up("q")
            actions.key_up("w")
            actions.key_up("o")
            actions.key_up("p")
        elif key_state == '1':
            actions.key_down("q")
            actions.key_up("w")
            actions.key_up("o")
            actions.key_up("p")
        elif key_state == '2':
            actions.key_up("q")
            actions.key_down("w")
            actions.key_up("o")
            actions.key_up("p")
        elif key_state == '3':
            actions.key_up("q")
            actions.key_up("w")
            actions.key_down("o")
            actions.key_up("p")
        elif key_state == '4':
            actions.key_up("q")
            actions.key_up("w")
            actions.key_up("o")
            actions.key_down("p")
        elif key_state == '5':
            actions.key_down("q")
            actions.key_down("w")
            actions.key_up("o")
            actions.key_up("p")
        elif key_state == '6':
            actions.key_down("q")
            actions.key_up("w")
            actions.key_down("o")
            actions.key_up("p")
        elif key_state == '7':
            actions.key_down("q")
            actions.key_up("w")
            actions.key_up("o")
            actions.key_down("p")
        elif key_state == '8':
            actions.key_up("q")
            actions.key_down("w")
            actions.key_down("o")
            actions.key_up("p")
        elif key_state == '9':
            actions.key_up("q")
            actions.key_down("w")
            actions.key_up("o")
            actions.key_down("p")
        elif key_state == 'a':
            actions.key_up("q")
            actions.key_up("w")
            actions.key_down("o")
            actions.key_down("p")
        elif key_state == 'b':
            actions.key_down("q")
            actions.key_down("w")
            actions.key_down("o")
            actions.key_up("p")
        elif key_state == 'c':
            actions.key_down("q")
            actions.key_up("w")
            actions.key_down("o")
            actions.key_down("p")
        elif key_state == 'd':
            actions.key_down("q")
            actions.key_down("w")
            actions.key_up("o")
            actions.key_down("p")
        elif key_state == 'e':
            actions.key_up("q")
            actions.key_down("w")
            actions.key_down("o")
            actions.key_down("p")
        elif key_state == 'f':
            actions.key_down("q")
            actions.key_down("w")
            actions.key_down("o")
            actions.key_down("p")
        actions.perform()


    def test_for_game_over(self, image):
        """

        Compare an image to the master failed image. Return True if they
        are similar, False if not.
        """
        failed_threshold = 5000
        image_offset = (126, 99, 510, 297,)
        cropped_image = image.crop(image_offset)
        failed_image = Image.open("autoQWOP/images/failed_test.png")
        mse = self.mse(np.array(cropped_image), np.array(failed_image))
        #print(mse)

        if mse < failed_threshold:
            return True
        else:
            return False


    def mse(self, image1, image2):
        """

        Get the mean squared error between two images. Must be numpy arrays.
        Borrowed from pyimagesearch.com.
        """
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image1.shape[1])

        # return the MSE, the lower the error, the more "similar"
        # the two images are
        return err

    def restart(self):
        actions = ActionChains(self.driver)
        actions.key_down(Keys.SPACE).key_up(Keys.SPACE)
        actions.perform()
    

def main():
    """

    Run many iterations and evolve the best combination of keys and time 
    """
    auto_qwop = AUTOQWOP()
    auto_qwop.load_website()
    auto_qwop.get_game()
    num_iterations = 10
    chromo = Chromosome()
    chromo.sequence = get_random_sequence(10)
    game_over = False
    try:
        while not game_over:
            for state in chromo.sequence:
                auto_qwop.update_outputs(state)
                time.sleep(.03)
            game_over = auto_qwop.test_for_game_over(
                auto_qwop.get_frame())
        time.sleep(2)
    except Exception as e:
        print(e)
    finally:
        #clean up
        auto_qwop.driver.quit()

if __name__ == "__main__":
    main()
