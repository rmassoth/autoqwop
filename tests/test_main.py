import time

import pytest
from selenium.webdriver.firefox.webelement import FirefoxWebElement
from PIL import Image
import numpy as np

from autoqwop.auto_qwop import AUTOQWOP


@pytest.fixture(scope="module")
def qwop():
    qwop_obj = AUTOQWOP()
    yield qwop_obj
    qwop_obj.driver.quit()


def test_loadwebsite(qwop):
    qwop.load_website()
    assert qwop.driver.title == "QWOP"


def test_getgame(qwop):
    qwop.get_game()
    assert type(qwop.game) == FirefoxWebElement


def test_get_image(qwop):
    """

    Tests that the image is the correct format and size
    """
    image = qwop.get_frame()
    assert image.format == "PNG"
    assert image.height == 400
    assert image.width == 640

def test_mse(qwop):
    image1 = np.array(Image.open("tests/images/failed1.png"))
    image2 = np.array(Image.open("tests/images/failed2.png"))
    assert qwop.mse(image1, image2) > 0.0
    assert qwop.mse(image1, image1) == 0.0

def test_failed_state(qwop):
    image1 = Image.open("tests/images/failed1.png")
    image2 = Image.open("tests/images/failed2.png")
    image3 = Image.open("tests/images/failed3.png")
    image4 = Image.open("tests/images/start.png")
    image5 = Image.open("tests/images/standing1.png")
    image6 = Image.open("tests/images/squatting1.png")
    assert qwop.test_for_game_over(image1) == True
    assert qwop.test_for_game_over(image2) == True
    assert qwop.test_for_game_over(image3) == True
    assert qwop.test_for_game_over(image4) == False
    assert qwop.test_for_game_over(image5) == False
    assert qwop.test_for_game_over(image6) == False

def test_restart(qwop):
    qwop.update_outputs(('3'))
    
    while(not qwop.test_for_game_over(qwop.get_frame())):
        time.sleep(1)
    qwop.update_outputs(('0'))
    qwop.restart()
    assert qwop.test_for_game_over(qwop.get_frame()) == False

