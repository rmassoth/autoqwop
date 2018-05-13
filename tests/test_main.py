from autoQWOP.auto_qwop import AUTOQWOP
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement

import pytest

from PIL import Image


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

def test_failed_state(qwop):
    assert qwop.test_for_game_over() == False
