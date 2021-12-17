# -*- coding: utf-8 -*-

import re
import time

from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

from crawlers.base import get_driver

from crawlers.renascientes.base import base_url
from model.post import build_post_obj
from persistence.dynamodb.dao import save_post

driver = get_driver()

actions = ActionChains(driver)

driver.get(base_url)
time.sleep(5)
k = 0

articles = []

page = 132


for page in range(page, 255):

    print("current page:", page)

    driver.get(base_url + f"page/{page}/")

    links = driver.find_elements_by_css_selector(".post .entry-header h2 a")

    for link in links:
        k += 1
        print(k, link.text)
        article_url = link.get_attribute("href")
        article__title = link.text
        date = re.search(r"blog/(\d{4}/\d{2}/\d{2})/", article_url).group(1)
        date = datetime.strptime(date, "%Y/%m/%d")

        save_post(build_post_obj("renascientes", link.text, article_url, date))

    time.sleep(10)
