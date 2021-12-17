import logging
import os
import requests
from selenium import webdriver
import re
import zipfile
import xmltodict
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
from selenium.webdriver.chrome.options import Options


def fix_driver(path):
    try:
        os.remove(f"{path}/drivers/chromedriver")
    except:
        pass
    stream = os.popen("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version")
    output = stream.read()
    version = re.search("Google Chrome ([\d\.]+)", output).group(1).split(".")[0]
    link = f"https://chromedriver.storage.googleapis.com/"
    r = requests.get(link)
    contents = [x for x in xmltodict.parse(r.content.decode())['ListBucketResult']['Contents']]
    mac64_download_keys = [x for x in contents if 'mac64' in x['Key']]
    matching_version_key = [x for x in mac64_download_keys if f"{version}." in x["Key"]][0]["Key"]
    download_link = link + matching_version_key
    r = requests.get(download_link)
    open(f'{path}/drivers/chromedriver.zip', 'wb').write(r.content)
    with zipfile.ZipFile(f"{path}/drivers/chromedriver.zip", 'r') as zip_ref:
        zip_ref.extractall(f"{path}/drivers/")
    os.chmod(f'{path}/drivers/chromedriver', 0o755)
    os.remove(f"{path}/drivers/chromedriver.zip")


def get_driver(download_directory=""):
    path = os.path.sep.join(os.path.dirname(os.path.realpath(__file__)).split(os.path.sep)[:-1])

    options = Options()

    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("--window-size=2500x1080")

    options.add_experimental_option("prefs", {
        "download.default_directory": f"{path}/{download_directory}",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True
    })

    try:
        driver = webdriver.Chrome(
            options=options,
            executable_path=os.path.sep.join([path, "drivers", "chromedriver"])
        )
    except SessionNotCreatedException as e:
        fix_driver(path)
    except WebDriverException as e:
        fix_driver(path)
    # finally:
    #     driver = webdriver.Chrome(
    #         options=options,
    #         executable_path=os.path.sep.join([path, "drivers", "chromedriver"])
    #     )

    return driver


driver = get_driver()

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)

month_list = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]
