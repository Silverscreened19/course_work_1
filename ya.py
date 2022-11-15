import requests
import json
import urllib.parse
from pprint import pprint
import logging
import time
from tqdm import tqdm


logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.INFO)

handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
handler2.setFormatter(formatter2)
logger2.addHandler(handler2)
logger2.info(f"Testing the custom logger for module {__name__}...")


class YaDisk:
    host = 'https://cloud-api.yandex.net'
    with open('/Users/silverscreened19/Documents/ya_disk_token.txt', 'r') as file:
        token_ya = file.readline()

    def __init__(self, token_ya):
        self.token = token_ya

    def headers(self):
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
                   'Authorization': f'OAuth {self.token}'}
        return headers

    def upload(self):
        with open('sorted_items.json') as file:
            info_list = json.load(file)
            dir = f'{self.create_folder()}'
            id = 0
            for id, el in enumerate(tqdm(info_list)):
                if id <= 4:
                    time.sleep(1)
                    name = el['file_name']
                    url_max = el['url_max']
                    path = f'{dir}/{name}'
                    query = urllib.parse.quote(url_max)
                    url = f'{self.host}/v1/disk/resources/upload?path={path}&url={query}&disable_redirects=false'
                    response = requests.post(url, headers=self.headers())
                    if response.status_code == 202:
                        print("Success")
                        logger2.info(
                            f'File {name} uploaded to the directory {dir}')
                        id += 1
                    else:
                        print('done')

    def create_folder(self):
        folder_name = input('Введите имя папки: ')
        path = f'{folder_name}'
        url = f'{self.host}/v1/disk/resources?path={path}'
        response = requests.put(url, headers=self.headers())
        if response.status_code == 201:
            link = response.json()['href']
            logger2.info(f'Folder {folder_name} is created')
            return link.split('=')[1]
        else:
            logger2.error(f'Folder {folder_name} already exists')
            print(response.json())
