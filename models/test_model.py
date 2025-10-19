from pydantic import BaseModel, Field
from enum import Enum

class Status(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    ERROR = "ERROR"


class TestTypes(str, Enum):
    HTTP_REQUEST = "HTTP_REQUEST"
    SYSTEM_CPU = "SYSTEM_CPU"

class CommonTest(BaseModel):
    test_name: str
    type: TestTypes

class HTTP_Request(CommonTest): 
    url: str
    timedelta_in_seconds: float = Field(gt=0)

class SystemCpu(CommonTest):
    duration_seconds: int = Field(ge=1)
    max_cpu_percents: int = Field(ge=1)

