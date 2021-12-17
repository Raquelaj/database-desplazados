from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from functions import get_driver
import time
import json

base_url = "http://www.afrodescolombia.org/category/noticias-afrodes/"

driver = get_driver()

driver.get(base_url)
time.sleep(5)

articles = []

next_page_btn = driver.find_element_by_css_selector("#content > div > a.next.page-numbers")


def get_post_title():
    try:
        return p.find_element_by_css_selector("div.entry h3").text
    except NoSuchElementException:
        try:
            return p.find_element_by_css_selector("div.entry h2").text
        except NoSuchElementException:
            return p.find_element_by_css_selector("h2.post-title").text



while next_page_btn:

    posts = driver.find_elements_by_css_selector("section.primary > article")

    for p in posts:

        link = p.find_element_by_css_selector("div.entry a.more-link")
        article_url = link.get_attribute("href")
        date = p.find_element_by_css_selector("div.entry-meta > span.meta-date > a > time").get_attribute("datetime").split("T")[0]
        title = get_post_title()

        print(title)

        articles.append(
            {
                "title": title,
                "url": article_url,
                "date": date,
            }
        )

    with open(f"afrodes_{datetime.now().date()}.json", "w") as json_file:
        json_file.write(json.dumps(articles, indent=4, ensure_ascii=False))

    next_page_btn.click()
    time.sleep(5)
    next_page_btn = driver.find_element_by_css_selector("#content > div > a.next.page-numbers")

