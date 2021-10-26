from typing import List, Dict, Union


class Result:
    def __init__(self, success: bool, status_code: int, message: str = '', data: List[Dict] = None):
        """
        Result returned from low-level RestAdapter
        :param success: True if HTTP Request was successful, False if not
        :param status_code: Standard HTTP Status code
        :param message: Human readable result
        :param data: Python List of Dictionaries (or maybe just a single Dictionary on error)
        """
        self.success = bool(success)
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


class Fact:
    def __init__(self, id: str, text: str, language_code: str, breed_id: str):
        self.id = id
        self.text = text
        self.language_code = language_code
        self.breed_id = breed_id


class Weight:
    def __init__(self, imperial: str, metric: str):
        self.imperial = imperial
        self.metric = metric


class Category:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Breed:
    def __init__(self, weight: Union[Weight, dict], id: str, name: str, country_codes: str, country_code: str,
                 description: str, temperament: str = '', origin: str = '', life_span: str = '', alt_names: str = '',
                 wikipedia_url: str = '', **kwargs) -> None:
        self.weight = Weight(**weight) if isinstance(weight, dict) else weight
        self.id = id
        self.name = name
        self.origin = origin
        self.country_codes = country_codes
        self.country_code = country_code
        self.description = description
        self.temperament = temperament
        self.life_span = life_span
        self.alt_names = alt_names
        self.wikipedia_url = wikipedia_url
        self.__dict__.update(kwargs)


class ImageShort:
    def __init__(self, id: int, url: str, categories: List[Category] = None, breeds: List[Breed] = None, **kwargs):
        self.id = id
        self.url = url
        self.categories = [] if not categories else [Category(**c) for c in categories]
        self.breeds = [] if not breeds else [Breed(**b) for b in breeds]
        self.__dict__.update(kwargs)


class ImageFull(ImageShort):
    def __init__(self, id: int, url: str, sub_id: int = 0, created_at: str = '', original_filename: str = '',
                 categories: List[Category] = None, breeds: List[Breed] = None, **kwargs):
        super().__init__(id, url, categories, breeds, **kwargs)
        self.sub_id = sub_id
        self.created_at = created_at
        self.original_filename = original_filename
        self.__dict__.update(kwargs)
