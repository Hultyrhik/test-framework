from pydantic import BaseModel, Field
from enum import Enum

class TestTypes(str, Enum):
    HTTP_REQUEST = "HTTP_REQUEST"
    SYSTEM_CPU = "SYSTEM_CPU"

class HTTP_Request(BaseModel):
    type: TestTypes
    url: str
    timedelta_in_seconds: float = Field(gt=0)

class SystemCpu(BaseModel):
    type: TestTypes
    duration_seconds: int = Field(ge=1)
    max_cpu_percents: int = Field(ge=1)