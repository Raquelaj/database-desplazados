# -*- coding: utf-8 -*-

import sys
import logging
import dateparser
import re
import requests as r
from selenium.webdriver.common.action_chains import ActionChains
import json
from datetime import datetime
import os

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

mode = sys.argv[1]

if mode == "decretos":

    driver = get_driver()

    actions = ActionChains(driver)

    k = 0
    articles = []

    for ano in range(2016, 2022):
        for mes_int, mes in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]):

            logger.warning(f"Crawling {ano}/{mes}")

            if ano == datetime.now().year and mes_int+1 > datetime.now().month:
                break

            base_url = f"https://dapre.presidencia.gov.co/normativa/decretos-{ano}/decretos-{mes}-{ano}"

            driver.get(base_url)

            pdfs = driver.find_elements_by_css_selector("div > div > div > ul > li > div > a")

            for decreto in pdfs:

                k += 1
                logger.warning(f"{k} {decreto.text}")
                article_url = decreto.get_attribute("href")

                date = re.search(r"(?:DEL|DE|EL)\s(\d{1,2})\s?(?:DE\s)?([A-Z]{1,})\s?(?:DE)?\s?(\d{4})?", decreto.text, re.IGNORECASE)
                preparsed_date = f"{date.group(1)} DE {mes.upper()} DE {ano}"
                date = dateparser.parse(preparsed_date, languages=["es"])

                logger.warning(date)

                articles.append(
                    {
                        "title": decreto.text,
                        "url": article_url,
                        "date": date.strftime("%Y-%m-%d"),
                    }
                )

    with open(f"data/governo_decretos_{datetime.now().date()}.json", "w") as json_file:
        json_file.write(json.dumps(articles, indent=4, ensure_ascii=False))

elif mode == "download":

    with open(f"data/governo_decretos_{datetime.now().date()}.json", "r") as json_file:
        decretos = json.loads(json_file.read())

    # for decreto in decretos[len(decretos)//2:]:
    for decreto in decretos:

        try:
            date = re.search(r"DECRETO\s(?:No\.\s)?(\d{1,})\s(?:DEL|DE|EL)\s(\d{1,2})\s?(?:DE\s)?([A-Z]{1,})\s?(?:D?E?)?\s?(\d{4})?", decreto["title"],
                             re.IGNORECASE)

            logger.warning(f"Downloading {decreto['title']}")

            num_decreto = date.group(1)
            preparsed_date = f"{date.group(2)} DE {date.group(3)} DE {date.group(4)}"
            date = dateparser.parse(preparsed_date, languages=["es"])
            filename = f"data/pdfs/governo/decretos/decreto_{num_decreto}_{date.strftime('%Y%m%d')}.pdf"

            if not filename.split('/')[-1] in os.listdir("data/pdfs/governo/decretos"):

                downloaded_pdf = r.get(decreto["url"]).content

                with open(filename, "wb") as pdf_file:
                    pdf_file.write(downloaded_pdf)

                logger.warning(f"Downloaded {filename}")

            decreto["file"] = filename

        except:
            logger.error(f"Falha ao baixar {decreto['title']}")


    with open(f"data/governo_decretos_{datetime.now().date()}-2.json", "w") as json_file:
        json_file.write(
            json.dumps(
                decretos,
                indent=4,
                ensure_ascii=False
            )
            )




