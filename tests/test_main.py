from autoQWOP import auto_qwop
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webelement import FirefoxWebElement
import pytest


@pytest.fixture(scope="module")
def driver():
    driver = auto_qwop.load_game()
    yield driver
    print("teardown webdriver")
    driver.quit()


def test_loadgame(driver):
    assert type(driver) == WebDriver
    assert driver.title == "QWOP"


def test_setup(driver):
    game = auto_qwop.setup(driver)
    assert type(game) == FirefoxWebElement


def test_get_image(driver):
    """

    Tests that the image is the correct format and size
    """
    game = auto_qwop.setup(driver)
    image = auto_qwop.get_frame(game)
    assert image.format == "PNG"
    assert image.height == 400
    assert image.width == 640