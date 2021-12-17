import re
from datetime import datetime

import dateparser

from crawlers.base import logger, driver, month_list
from crawlers.presidencia.decretos.between_2016_today.base import base_url

k = 0


for ano in range(2016, 2022):

    for mes_int, mes in enumerate(month_list):

        logger.warning(f"Crawling {ano}/{mes}")

        if ano == datetime.now().year and mes_int + 1 > datetime.now().month:
            break

        driver.get(base_url.format(ano=ano, mes=mes))

        pdfs = driver.find_elements_by_css_selector("div > div > div > ul > li > div > a")

        for decreto in pdfs:
            k += 1
            logger.warning(f"{k} {decreto.text}")
            article_url = decreto.get_attribute("href")

            date = re.search(r"(?:DEL|DE|EL)\s(\d{1,2})\s?(?:DE\s)?([A-Z]{1,})\s?(?:DE)?\s?(\d{4})?", decreto.text,
                             re.IGNORECASE)
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