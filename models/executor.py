import logging
from typing import Any
from .base_adapter import BaseTestAdapter
from .test_model import Status, TestTypes
from .http_adapter import HttpAdapter
from .system_cpu_adapter import SystemCPUAdapter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TestExecutor:
    def __init__(self):
        self.adapters: dict[str, BaseTestAdapter] = {}
        
    def _load_adapter(self, adapter_name: str) -> BaseTestAdapter:
       
        if adapter_name not in self.adapters:
            try:
                if adapter_name == TestTypes.HTTP_REQUEST:
                    self.adapters[adapter_name] = HttpAdapter
                elif adapter_name == TestTypes.SYSTEM_CPU:
                    self.adapters[adapter_name] = SystemCPUAdapter
            except (ImportError, AttributeError) as e:
                raise ValueError(f"Не удалось загрузить адаптер '{adapter_name}': {e}")
        return self.adapters[adapter_name]
    
    def run_tests(self, test_suites: list[dict[str, Any]]):
        results : list[dict[str, Any]] = []
        for test_config in test_suites:
            test_name = test_config["test_name"]
            adapter_type = test_config["type"]
            
            logger.info(f"Запуск теста: {test_name}")
            
            try:
                adapter = self._load_adapter(adapter_type)
                result = adapter.run(test_config)
                result["test_name"] = test_name
                results.append(result)
                
                if result["status"] == Status.PASSED:
                    logger.info(f"ТЕСТ ПРОЙДЕН: {test_name} - {result['message']}")
                elif result["status"] == Status.FAILED:
                    logger.warning(f"ТЕСТ ПРОВАЛЕН: {test_name} - {result['message']}")
                else:
                    logger.error(f"ОШИБКА В ТЕСТЕ: {test_name} - {result['message']}")
                    
            except Exception as e:
                error_result = {
                    "test_name": test_name,
                    "status": "error",
                    "message": f"Критическая ошибка при выполнении теста: {e}",
                    "error": str(e)
                }
                results.append(error_result)
                logger.error(f"КРИТИЧЕСКАЯ ОШИБКА: {test_name} - {e}")
        
        self._print_summary(results)
        return results
    
    def _print_summary(self, results: list[dict[str, Any]]):
        stats = {"passed": 0, "failed": 0, "errors": 0}
        for result in results:
            if result["status"] == Status.PASSED:
                stats["passed"] += 1
            elif result["status"] == Status.FAILED:
                stats["failed"] += 1
            else:
                stats["errors"] += 1
        logger.info("="*50)
        logger.info("ОБЩИЙ ОТЧЁТ:")
        logger.info(f"Всего тестов: {len(results)}")
        logger.info(f"Пройдено: {stats["passed"]}")
        logger.info(f"Провалено: {stats["failed"]}")
        logger.info(f"Ошибок: {stats["errors"]}")
        logger.info("="*50)