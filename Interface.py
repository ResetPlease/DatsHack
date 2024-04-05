from requests import get, post
from requests.models import Response
from requests.exceptions import RequestException, Timeout, HTTPError
from typing import Union
import config

class Interface:
    TOKEN : str
    headers = {"X-Auth-Token" : config.TOKEN}
    timeout = 10
    def __init__(self, token):
        self.TOKEN = token
        self.headers['Authorization'] = f"Basic {self.TOKEN}"
    
    @staticmethod
    def Data(response : Response):
        """
            Статический метод `Data` возвращает результат запроса в виде `json` или просто `text`
        """
        try:
            return response.json()
        except Exception as e:
            print(f"Ошибка получения json-ответа: {e}")
            return response.text

    def __get(self, url : str) -> Union[None, str, dict]:
        try:
            result = get(url, headers=self.headers, timeout=self.timeout)
            return Interface.Data(result)
        except Timeout:
            print("Время ожидания ответа от сервера истекло")
        except HTTPError as http_err:
            print(f"Ошибка HTTP( ответ 4xx и 5xx):\n{http_err}")
        except RequestException as request_exc:
            print(f"Какой-то хайп RequestException:\n{request_exc}")
        except Exception as e:
            print(f"Какой-то левак:\n{e}")
        return None

    def __post(self, url : str, data : dict) -> Union[None, str, dict]:
        try:
            result = post(url, headers=self.headers, data=data, timeout=self.timeout)
            return Interface.Data(result)
        except Timeout:
            print("Время ожидания ответа от сервера истекло")
        except HTTPError as http_err:
            print(f"Ошибка HTTP( ответ 4xx и 5xx):\n{http_err}")
        except RequestException as request_exc:
            print(f"Какой-то хайп RequestException:\n{request_exc}")
        except Exception as e:
            print(f"Какой-то левак:\n{e}")
        return None
        
    
    def Register(self, name : str, url : str, method : str) -> None:
        """
            Метод Register регистрирует в классе Interface новый метод 
            c именем `name` с указанным эндпоинтом API и типом запроса.
            
            
            Грубо:
                * Получить некоторые данные - `GET` -> `Register("name", URL, "GET")`

                * Отправить даные - `POST` -> `Register("name", URL, "POST")`
            
            Возвращаемое значение обязательно чекать на `None` для избежания исключений вне класса.
        """
        name = name.strip()
        if method.lower() == "post":
            setattr( Interface, name, lambda self, data : self.__post(url, data) )
        elif method.lower() == "get":
            setattr( Interface, name, lambda self, : self.__get(url) )


if __name__ == "__main__":

    # инициализация объекта типа класса API
    manager = Interface("TOKEN") 
    
    # Регистрируем новые методы
    manager.Register("EchoGet", "https://echo.free.beeceptor.com", "GET")
    manager.Register("EchoPost", "https://echo.free.beeceptor.com", "POST")
    manager.Register("Bebra", "Словим exception из-за неправильного URL", "GET")
    
    # чекаем результаты
    print( manager.EchoGet() )
    print( manager.EchoPost( {"hello" : True} ) )
    
    print( manager.Bebra() )

    """ OUTPUT:
    
    GET:
        {'method': 'GET', 'protocol': 'https', 'host': 'echo.free.beeceptor.com', 
        'path': '/', 'ip': '83.221.30.155', 'headers': {'Host': 'echo.free.beeceptor.com', 
                                    'User-Agent': 'python-requests/2.28.1', 'Accept': '*/*', 
            'Accept-Encoding': 'gzip, deflate, br', 'Authorize': 'Basic TOKEN'}, 'parsedQueryParams': {}}

    =========================================================================================================
    
    POST:
        {'method': 'POST', 'protocol': 'https', 'host': 'echo.free.beeceptor.com', 
        'path': '/', 'ip': '83.221.30.155', 'headers': {'Host': 'echo.free.beeceptor.com', 
                        'User-Agent': 'python-requests/2.28.1', 'Content-Length': '10', 'Accept': '*/*',
                        'Accept-Encoding': 'gzip, deflate, br', 'Authorize': 'Basic TOKEN', 
                        'Content-Type': 'application/x-www-form-urlencoded'}, 

        'parsedQueryParams': {}, 'parsedBody': {'hello': 'True'}} <-- JSON

    =========================================================================================================

    Bebra GET:
        Какой-то хайп RequestException:
        Failed to parse: Словим exception из-за неправильного URL
        None

    """