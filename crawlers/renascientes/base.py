# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
import re
from selenium.webdriver.common.action_chains import ActionChains

from unidecode import unidecode
from ..base import get_driver

driver = get_driver()

actions = ActionChains(driver)

base_url = "http://renacientes.net/"


def get_region(text):
    t = unidecode(text.lower())
    if "pacifico" in t:
        return "Pacífico"
    elif "caribe" in t:
        return "Caribe"
    elif re.search("andin(a|o)", t):
        return "Andino"
    else:
        return None


def get_author():
    try:
        a = driver.find_element_by_css_selector(
            "div.article-content.clearfix > div.below-entry-meta > span.byline > span > a")
        return a.text
    except NoSuchElementException:
        return None


def get_text():

    try:
        text_element = driver.find_element_by_css_selector("#content")
    except NoSuchElementException:
        text_element = driver.find_element_by_css_selector(
            "div.article-content.clearfix > div.entry-content.clearfix > p")

    return text_element.text