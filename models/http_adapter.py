import requests
from datetime import datetime
from .base_adapter import BaseTestAdapter
from typing import Any
from .test_model import HTTP_Request, Status

class HttpAdapter(BaseTestAdapter):
    def run(self, test_data: dict[str, Any]) -> dict[str, Any]:
        try:
            http_request = HTTP_Request.model_validate(test_data)
            url = http_request.url

            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            server_time_str = response.text
            server_time = datetime.strptime(server_time_str, "%d/%m/%Y %H:%M:%S")
            local_time = datetime.now()
            
            time_difference = abs((local_time - server_time).total_seconds())
            max_allowed_difference = http_request.timedelta_in_seconds
            
            if time_difference <= max_allowed_difference:
                return {"status": Status.PASSED, "message": f"Время синхронизировано. Расхождение: {time_difference:.2f}с."}
            else:
                return {"status": Status.FAILED, "message": f"Расхождение времени слишком велико: {time_difference:.2f}с."}
                
        except requests.exceptions.RequestException as e:
            return {"status": Status.ERROR, "message": f"Ошибка сети: {e}", "error": str(e)}
        except ValueError as e:
            return {"status": Status.ERROR, "message": f"Ошибка парсинга времени: {e}", "error": str(e)}