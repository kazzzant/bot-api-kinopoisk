import requests
from logs.log import logger
from loader import site_api_key


headers = {"X-API-KEY": site_api_key}
url = "https://api.kinopoisk.dev/"


@logger.catch
def api_request(query: dict, url_address: str = '') -> (bool, list):
    """
    отправляет запрос на сайт, получает ответ и проверяет статус ответа
    в случае успешного ответа возвращает список данных в формате json
    """
    try:
        response = requests.get(url+url_address, params=query, headers=headers, timeout=15)

        if response.status_code == 200:
            return True, response.json()
        else:
            return False, []
    except requests.Timeout as error_timeout:
        logger.error(error_timeout)
        return False, []
    except requests.ConnectionError as error_connection:
        logger.error(error_connection)
        return False, []
    except requests.RequestException as error_exception:
        logger.error(error_exception)
        return False, []
