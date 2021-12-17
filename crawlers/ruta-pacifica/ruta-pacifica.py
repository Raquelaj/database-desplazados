import sys
import logging as lg
import time
from functions import get_driver
from selenium.webdriver.common.action_chains import ActionChains

lg.info("Iniciando crawler de ruta pacifica")

driver = get_driver()
actions = ActionChains(driver)

base_url = "https://rutapacifica.org.co/wp/category/publicaciones/"

driver.get(base_url)
time.sleep(5)

step = int(sys.argv[1])

if step == 1:
    articles = []
    lg.info("Buscando links e datas...")

    # posts = driver.find_elements_by_css_selector("article > div > div > div > div.post_more > a")
    posts = driver.find_elements_by_css_selector("article")

    for post in posts:
        link = post.find_element_by_css_selector("div > div > div > div.post_more > a")
        article_url = link.get_attribute("href")
        date_element = post.find_element("div > div.post_text > div > h2 > span")
        mes = ""
        dia = ""
        date = f"2020-{mes}-{dia}"

        articles.append(
            {
                "title": link.text,
                "url": article_url,
                "date": date.strftime("%Y-%m-%d"),
            }
        )

post_urls = []
for post in posts:
    post_urls.append(post.get_attribute("href"))

while post_urls:
    url = post_urls.pop(0)
    driver.get(url)
    download_button = driver.find_element_by_css_selector("div.post_content_holder > div > div > div.vc_row.wpb_row.section.vc_row-fluid.vc_custom_1600696814592.grid_section > div > div > div:nth-child(2) > div > div > a")
    download_url = download_button.get_attribute("href")

