from ninja import Schema
from pydantic import Field


class ProgressIn(Schema):
    current_time: float = Field(ge=0)
    duration: float = Field(ge=0)


class ProgressOut(Schema):
    current_time: float
    duration: float
    percentage: float
