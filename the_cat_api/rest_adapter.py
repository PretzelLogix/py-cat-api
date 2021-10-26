import requests
import logging
from typing import List, Dict
from json import JSONDecodeError
from the_cat_api.exceptions import TheCatApiException
from the_cat_api.models import Result


class RestAdapter:
    def __init__(self, hostname: str, api_key: str = '', ver: str = 'v1', ssl_verify: bool = True, logger: logging.Logger = None):
        self._logger = logger or logging.getLogger(__name__)
        self.url = f"https://{hostname}/{ver}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        if not ssl_verify:
            # noinspection PyUnresolvedReferences
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        full_url = self.url + endpoint
        headers = {'x-api-key': self._api_key}
        try:
            log_line = f"method={http_method}, url={full_url}, params={ep_params}"
            self._logger.debug(msg=log_line)
            response = requests.request(method=http_method, url=full_url, verify=self._ssl_verify, headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise TheCatApiException(str(e)) from e
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            log_line = f"success=False, status_code={response.status_code}, message={e}"
            self._logger.warning(msg=log_line)
            return Result(False, response.status_code, message=str(e))
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        self._logger.debug(msg=log_line)
        return Result(is_success, response.status_code, message=response.reason, data=data_out)

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)
