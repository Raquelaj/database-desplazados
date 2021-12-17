# -*- coding: utf-8 -*-

import sys
import logging
import time

import dateparser
import re
from selenium.webdriver.common.action_chains import ActionChains
import json
from datetime import datetime
from functions import get_driver
import os

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

mode = sys.argv[1]


def fixed_file_list(download_directory):
    return [x.replace('  ', ' ') for x in os.listdir(download_directory)]


def get_fixed_filename(filename, download_directory):

    for name in os.listdir(download_directory):
        if filename == name.replace('  ', ' '):
            return name

    return None


if mode == "leis":

    download_directory = "data/pdfs/governo/leis"
    driver = get_driver(download_directory)

    actions = ActionChains(driver)

    k = 0
    articles = []

    for ano in range(2010, 2017):

        base_url = f"http://wp.presidencia.gov.co/sitios/normativa/leyes/Paginas/leyes-{ano}.aspx"

        driver.get(base_url)

        pdfs = driver.find_elements_by_css_selector("body > form > div > article > div > div > p > a")

        for lei in pdfs:

            k += 1
            logger.warning(f"{k} {lei.text}")
            article_url = lei.get_attribute("href")

            date = re.search(r"(?:DEL|DE|EL)\s(\d{1,2})\s?(?:DE\s)?([A-Z]{1,})\s?(?:DE)?\s?(\d{4})?", lei.text, re.IGNORECASE)

            if date.group(3):
                preparsed_date = f"{date.group(1)} DE {date.group(2).upper()} DE {date.group(3)}"
                last_year = date.group(3)
                date = dateparser.parse(preparsed_date, languages=["es"])
            else:
                preparsed_date = f"{date.group(1)} DE {date.group(2).upper()} DE {last_year}"
                date = dateparser.parse(preparsed_date, languages=["es"])

            logger.warning(date)

            articles.append(
                {
                    "title": lei.text,
                    "url": article_url,
                    "date": date.strftime("%Y-%m-%d"),
                }
            )

    with open(f"data/governo_leis_{datetime.now().date()}.json", "w") as json_file:
        json_file.write(json.dumps(articles, indent=4, ensure_ascii=False))

elif mode == "download":

    download_directory = "data/pdfs/governo/leis"
    driver = get_driver(download_directory)

    actions = ActionChains(driver)

    k = 0
    articles = []

    base_url = "https://dapre.presidencia.gov.co/normativa/leyes"

    driver.get(base_url)

    with open(f"data/governo_leis_{datetime.now().date()}.json", "r") as json_file:
        leis = json.loads(json_file.read())

    for lei in leis:

        try:
            date = re.search(r"LEY\s(?:No\.\s)?(\d{1,})\s(?:DEL|DE|EL)\s(\d{1,2})\s?(?:DE\s)?([A-Z]{1,})\s?(?:D?E?)?\s?(\d{4})?", lei["title"],
                             re.IGNORECASE)

            logger.warning(f"Downloading {lei['title']}")

            num_decreto = date.group(1)
            preparsed_date = f"{date.group(2)} DE {date.group(3)} DE {date.group(4)}"
            date = dateparser.parse(preparsed_date, languages=["es"])
            filename = f"data/pdfs/governo/leis/lei_{num_decreto}_{date.strftime('%Y%m%d')}.pdf"

            if not filename.split('/')[-1] in os.listdir(download_directory):

                logger.warning(f"Downloading {filename}")

                driver.get(lei["url"])
                while f"{lei['title']}.pdf" not in fixed_file_list(download_directory) \
                        and f"{lei['url'].split('/')[-1]}" not in fixed_file_list(download_directory) \
                        and f"{lei['title'].replace('  ', ' ')}.pdf" not in fixed_file_list(download_directory):
                    time.sleep(1)

                fixed_filename = get_fixed_filename(f"{lei['title']}.pdf", download_directory)

                if fixed_filename in os.listdir(download_directory):
                    os.rename(f"{download_directory}/{fixed_filename}", filename)
                if f"{lei['url'].split('/')[-1]}" in os.listdir(download_directory):
                    os.rename(f"{download_directory}/{lei['url'].split('/')[-1]}", filename)

                logger.warning(f"Downloaded {filename}")



            lei["file"] = filename

        except:
            logger.error(f"Falha ao baixar {lei['title']}")


    with open(f"data/governo_leis_{datetime.now().date()}-2.json", "w") as json_file:
        json_file.write(
            json.dumps(
                leis,
                indent=4,
                ensure_ascii=False
            )
            )