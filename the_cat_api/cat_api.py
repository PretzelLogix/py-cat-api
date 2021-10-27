import logging
from the_cat_api.rest_adapter import RestAdapter
from the_cat_api.exceptions import TheCatApiException
from the_cat_api.models import *


class TheCatApi:
    def __init__(self, hostname: str = 'api.thecatapi.com', api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)

    def get_kitty(self) -> ImageShort:
        return self.get_clowder_of_kitties(1)[0]

    def get_clowder_of_kitties(self, amt: int = 1) -> List[ImageShort]:
        result = self._rest_adapter.get(endpoint=f'/images/search?limit={amt}')
        kitty_img_list = [ImageShort(datum) for datum in result.data]
        return kitty_img_list

    def fetch_image_data(self, image: ImageShort):
        image.data = self._rest_adapter.fetch_data(url=image.url)
