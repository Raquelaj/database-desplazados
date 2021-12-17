import time
from datetime import datetime
from decimal import Decimal

from crawlers.onic.base import driver, base_url
from model.post import Post
from persistence.dynamodb.dao import save_post

DIV_DATE_TIME = "div.item_info > dl > dd > time"
HEADER_H_A = "header > h4 > a"
ARTICLE = "#component > main > section > div > div > article"
DENY_BTN = "#pa-deny-btn"

driver.get(base_url)
time.sleep(5)

has_next_page = True

driver.find_element_by_css_selector(DENY_BTN).click()

count = 0

# TODO: has_next_page has to be evaluated based on the page navigation component

while has_next_page:

    count += 10

    posts = driver.find_elements_by_css_selector(ARTICLE)

    for p in posts:
        link = p.find_element_by_css_selector(HEADER_H_A)
        article_url = link.get_attribute("href")
        date_str = p \
            .find_element_by_css_selector(DIV_DATE_TIME) \
            .get_attribute("datetime").split(" ")[0]
        date = datetime.strptime(date_str, "%Y-%m-%d")

        print(article_url)

        post = Post(
            source="onic",
            title=article_url.split("/")[-1],
            url=article_url,
            date=Decimal(date.timestamp())
        )

        save_post(post)

    driver.get(base_url + f"?start={count}")
    time.sleep(5)
