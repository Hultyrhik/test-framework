import psutil
import time
from typing import Any
from pydantic import ValidationError
from .base_adapter import BaseTestAdapter
from .test_model import SystemCpu, Status

class SystemCPUAdapter(BaseTestAdapter):
    @staticmethod
    def run(test_data: dict[str, Any]) -> dict[str, Any]:
        try:
            system_cpu = SystemCpu.model_validate(test_data)
            duration = system_cpu.duration_seconds
            max_cpu_percent = system_cpu.max_cpu_percents
            
            start_time = time.time()
            max_observed = 0.0
            while (time.time() - start_time) < duration:
                cpu_percent = psutil.cpu_percent(interval=1.0)
                max_observed = max(max_observed, cpu_percent)
                if cpu_percent > max_cpu_percent:
                    return {
                        "status": Status.FAILED,
                        "message": f"Загрузка ЦП превысила {max_cpu_percent}%. Текущая: {cpu_percent}%."
                    }
            if max_observed <= max_cpu_percent:
                return {"status": Status.PASSED, "message": f"Загрузка ЦП стабильна. Максимум: {max_observed}% на протяжении {duration} секунд."}
            else:
                return {"status": Status.FAILED, "message": f"Максимальная загрузка ЦП: {max_observed}% на протяжении {duration} секунд."}
        except ValidationError as e:
            return {"status": Status.ERROR, "message": f"Ошибка парсинга модели: {e}", "error": str(e)}
        except Exception as e:
            return {"status": Status.ERROR, "message": f"Ошибка при мониторинге ЦП: {e}", "error": str(e)}