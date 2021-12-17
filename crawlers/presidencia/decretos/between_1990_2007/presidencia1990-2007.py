# -*- coding: utf-8 -*-

import sys
import logging
import requests
from selenium.webdriver.common.action_chains import ActionChains
from functions import get_driver
import os

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

ERROR_MESSAGE = "The resource you are looking for has been removed, had its name changed, or is temporarily unavailable."

mode = sys.argv[1]
initial_year = int(sys.argv[2])


def try_to_download():
    try:
        downloaded_pdf = requests.get(url).content

        with open(filename, "wb") as pdf_file:
            pdf_file.write(downloaded_pdf)

        logger.warning(f"Downloaded {filename}")

        return True

    except requests.exceptions.ConnectionError:
        logger.error(f"Timeout ao baixar {filename}")
    except Exception as e:
        logger.error(f"Erro desconhecido ao baixar {filename}", e)

    return False


if mode == "decretos":

    driver = get_driver()

    actions = ActionChains(driver)

    k = 0
    articles = []

    downloaded_files = os.listdir("data/pdfs/governo/decretos")

    for ano in range(initial_year, 2008):

        for mes_int, mes in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]):

            for dia in range(1, 32):

                base_url = f"http://historico.presidencia.gov.co/prensa_new/decretoslinea/{ano}/{mes}/{str(dia).zfill(2)}/conte.htm"
                driver.get(base_url)

                if driver.find_element_by_css_selector("body").text != ERROR_MESSAGE:
                    download_urls = [x.get_attribute("href") for x in driver.find_elements_by_css_selector("body > div > table > tbody tr td font font a") if x.text == 'pdf']

                    for url in download_urls:

                        logger.warning(f"Baixando {url}")

                        numero = url.split("/")[-1].strip('.pdf').strip('dec')[:-6].zfill(4)
                        data = f"{ano}{str(mes_int+1).zfill(2)}{str(dia).zfill(2)}"

                        filename = f"data/pdfs/governo/decretos/{data}_decreto_{numero}.pdf"

                        if not filename.split('/')[-1] in downloaded_files:
                            retry = 0
                            while retry < 3:
                                if try_to_download():
                                    break
                                retry += 1
