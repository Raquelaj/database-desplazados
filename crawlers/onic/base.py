import hashlib
import re
from os import rename, listdir

from crawlers.base import get_driver
from model.post import Post

base_url = "https://www.onic.org.co/noticias"

driver = get_driver()


def move_and_rename_file(url):
    hash_url = hashlib.md5(url.encode()).hexdigest()
    pdf_files = [x for x in listdir("data") if re.search("\.pdf", x)]
    rename(f"data/{pdf_files[0]}", f"data/pdfs/onic-{hash_url}.pdf")


def download_iframe_pdf(post: Post):
    driver.switch_to.frame(driver.find_element_by_css_selector(
        "#component > main > article > div.item_fulltext > div:nth-child(2) > iframe"))
    driver.find_element_by_css_selector("#download").click()
    move_and_rename_file(post.url)
