from pydantic import BaseModel
from enum import Enum

class TestTypes(str, Enum):
    HTTP_REQUES = "HTTP_REQUEST"

class HTTP_Request(BaseModel):
    type: TestTypes
    url: str
    timedelta_in_seconds: float