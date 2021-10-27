import logging
from typing import Iterator, Callable
from the_cat_api.rest_adapter import RestAdapter
from the_cat_api.exceptions import TheCatApiException
from the_cat_api.models import *


class TheCatApi:
    def __init__(self, hostname: str = 'api.thecatapi.com', api_key: str = '', ver: str = 'v1', ssl_verify: bool = True,
                 logger: logging.Logger = None, page_size: int = 5):
        self._rest_adapter = RestAdapter(hostname, api_key, ver, ssl_verify, logger)
        self._page_size = page_size

    def get_kitty(self) -> ImageShort:
        return self.get_clowder_of_kitties(1)[0]

    def get_clowder_of_kitties(self, amt: int = 1) -> List[ImageShort]:
        result = self._rest_adapter.get(endpoint=f'/images/search?limit={amt}')
        kitty_img_list = [ImageShort(datum) for datum in result.data]
        return kitty_img_list

    def fetch_image_data(self, image: ImageShort):
        image.data = self._rest_adapter.fetch_data(url=image.url)

    def _page(self, endpoint: str, model: Callable[..., Model], max_amt: int = 100) -> Iterator[Model]:
        amt_yielded = 0
        curr_page = last_page = 1
        ep_params = {'limit': self._page_size, 'order': 'Desc'}
        while curr_page <= last_page:
            ep_params['page'] = curr_page
            result = self._rest_adapter.get(endpoint=endpoint, ep_params=ep_params)
            last_page = int(result.headers.get('pagination-count', 1))
            curr_page = int(result.headers.get('pagination-page')) + 1
            for datum in result.data:
                yield from model(datum)
                amt_yielded += 1
                if amt_yielded >= max_amt:
                    last_page = 0
                    break

    def get_kitties_paged(self, max_amt: int = 100) -> Iterator[ImageShort]:
        return self._page(endpoint='/images/search', model=ImageShort, max_amt=max_amt)
