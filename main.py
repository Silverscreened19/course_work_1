import datetime
import requests
import json
import logging
from pprint import pprint
from ya import YaDisk
import logging


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)
py_handler = logging.FileHandler(f"{__name__}.log", mode='w')
py_formatter = logging.Formatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s")
py_handler.setFormatter(py_formatter)
py_logger.addHandler(py_handler)
py_logger.info(f"Testing the custom logger for module {__name__}...")

with open('/Users/silverscreened19/Documents/vk_token.txt', 'r') as file:
    token_vk = file.readline()

with open('/Users/silverscreened19/Documents/ya_disk_token.txt', 'r') as file:
    token_ya = file.readline()


class VK:

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def photos_get(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id, 'extended': '1',
                  'photo_sizes': '1', 'album_id': 'profile'}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


    def photos_filter(self):
        with open('photos_info.json') as file:
            items = json.load(file)
            sorted_items = [item for item in items if item['type'] != '']
            with open('sorted_items.json', 'w') as f:
                json.dump(sorted_items, f, ensure_ascii=False, indent=4)

    def photos_info(self):
        items = self.photos_get()['response']['items']
        all_photos = {}
        likes_list = []
        json_list = []
        for item in items:
            height = 0
            width = 0
            url_max = ''
            type = ''
            file_name = str(item['likes']['count'])
            timestamp = item['date']
            value = datetime.datetime.fromtimestamp(
                timestamp).strftime('%Y-%m-%d')
            for size in item['sizes']:
                if height < size['height'] and width < size['width']:
                    height = size['height']
                    width = size['width']
                    type = size['type']
                    url_max = size['url']
            if item['likes']['count'] not in likes_list:
                likes_list.append(item['likes']['count'])
                all_photos = dict(
                    file_name=f'{file_name}.jpg', type=type, url_max=url_max)
            else:
                all_photos = dict(
                    file_name=f'{file_name} {value}.jpg', type=type, url_max=url_max)
            json_list.append(all_photos)
        py_logger.info(f'Photos info collected')
        return json_list

    def json_file(self):
        with open('photos_info.json', 'w') as f:
            info = vk.photos_info()
            json.dump(info, f, ensure_ascii=False, indent=4)
            py_logger.info(f'photos_info.json done')


def logging_():
    logging.basicConfig(
        level=logging.INFO,
        filename='py_log.log',
        filemode='w',
        format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s")
    logging.debug('A DEBUG Message')
    logging.info('An INFO')
    logging.warning('A WARNING')
    logging.error('An ERROR')
    logging.critical('A message of CRITICAL severity')


if __name__ == '__main__':
    logging_()
    owner_id = int(input('Введите id вконтакте: '))
    vk = VK(token_vk)
    vk.photos_get()
    vk.json_file()
    vk.photos_filter()
    ya = YaDisk(token_ya)
    ya.upload()
