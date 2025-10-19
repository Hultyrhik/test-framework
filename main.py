import json
import sys
from models.executor import TestExecutor
from models.test_model import Status

def main():
    relative_test_file_path = 'tests/test_cases.json'
    try:
        with open(relative_test_file_path, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
        executor = TestExecutor()
        all_results = executor.run_tests(test_cases)
        
        if any(r["status"] in (Status.FAILED, Status.ERROR) for r in all_results):
            sys.exit(1)
        else:
            sys.exit(0)
    except FileNotFoundError:
        print(f"Ошибка: Файл с тестами {relative_test_file_path} не найден.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: Невалидный JSON в файле конфигурации: {e}")
        sys.exit(1)
    


if __name__ == "__main__":
    main()