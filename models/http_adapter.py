import requests
from datetime import datetime
from .base_adapter import BaseTestAdapter
from typing import Any
from .test_model import HTTP_Request, Status
from pydantic import ValidationError
from datetime import timezone

class HttpAdapter(BaseTestAdapter):
    @staticmethod
    def run(test_data: dict[str, Any]) -> dict[str, Any]:
        try:
            http_request = HTTP_Request.model_validate(test_data)
            url = http_request.url

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            server_time_json = response.json()
            server_timezone = server_time_json["timezone"]
            timestamp = server_time_json["timestamp"]
            server_time = int(timestamp) /1000
            client_time = datetime.now(timezone.utc).timestamp()
            
            time_difference = abs((server_time - client_time))
            max_allowed_difference = http_request.timedelta_in_seconds
            
            if time_difference <= max_allowed_difference:
                return {"status": Status.PASSED, "message": f"Время синхронизировано. Расхождение: {time_difference:.2f}с. Максимум - {max_allowed_difference}c. Пришло - {server_time}. На клиенте - {client_time}"}
            else:
                return {"status": Status.FAILED, "message": f"Расхождение времени слишком большое: {time_difference:.2f}с. Максимум - {max_allowed_difference}c. Пришло - {server_time}. На клиенте - {client_time}"}
                
        except requests.exceptions.RequestException as e:
            return {"status": Status.ERROR, "message": f"Ошибка сети: {e}", "error": str(e)}
        except ValidationError as e:
            error_obj = {}
            for error in e.errors():
                print(f"Location: {error['loc']}")
                print(f"Message: {error['msg']}")
                print(f"Type: {error['type']}")
                error_obj["Location": f"Location: {error['loc']}"]
                error_obj["Message": f"Message: {error['msg']}"]
                error_obj["Type": f"Type: {error['type']}"]
            return {"status": Status.ERROR, "message": f"Ошибка парсинга модели: {e}", "error": str(error_obj)}
        except ValueError as e:
            return {"status": Status.ERROR, "message": f"Ошибка парсинга времени: {e}", "error": str(e)}