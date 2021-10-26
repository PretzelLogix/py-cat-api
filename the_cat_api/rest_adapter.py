import requests
import logging
from typing import List, Dict
from json import JSONDecodeError
from the_cat_api.exceptions import TheCatApiException
from the_cat_api.models import Result


class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        """
        Constructor for RestAdapter
        :param hostname: Normally, api.the_cat_api.com
        :param api_key: (optional) string used for authentication when POSTing or DELETEing
        :param ver: always v1
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues, can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here.
        """
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}/{ver}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        Private method for GET, POST, DELETE, etc. methods
        :param http_method: Any str representing the HTTP Method ('GET', 'POST', etc.)
        :param endpoint: A str representing the endpoint after the base URL
        :param ep_params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}

        # Log HTTP params and perform an HTTP request; catching, logging, and re-raising any exceptions
        try:
            log_line = f"method={http_method}, url={full_url}, params={ep_params}"
            self._logger.debug(msg=log_line)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise TheCatApiException(str(e)) from e

        # Deserialize JSON output to Python object, or return failed Result on exception
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            log_line = f"success=False, status_code={response.status_code}, message={e}"
            self._logger.warning(msg=log_line)
            return Result(False, response.status_code, message=str(e))

        # If status_code in 200-299 range, return success Result with data, otherwise returned failed Result
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        return Result(is_success, response.status_code, message=response.reason, data=data_out)

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """
        GET method for TheCatApi
        :param endpoint: A str representing the endpoint after the base URL
        :param ep_params: A dict of Endpoint Parameters
        :return: Result object
        """
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        POST method for TheCatApi
        :param endpoint: A str representing the endpoint after the base URL
        :param ep_params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        """
        DELETE method for TheCatApi
        :param endpoint: A str representing the endpoint after the base URL
        :param ep_params: A dict of Endpoint Parameters
        :param data: A dict of data sent in the body
        :return: Result object
        """
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
