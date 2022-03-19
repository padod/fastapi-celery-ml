from datetime import datetime
from typing import (List, Optional, Literal)

from pydantic import BaseModel, Field, validator

CeleryStatus = Literal['PENDING', 'STARTED', 'RETRY', 'FAILURE', 'SUCCESS']


class WorkerPostResponse(BaseModel):
    id: str
    status: CeleryStatus


class Point(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)


class OrderedPoint(BaseModel):
    longitude: float = Field(..., ge=-180, le=180)
    latitude: float = Field(..., ge=-90, le=90)
    order: int = Field(..., ge=0)


class OptimizerResponse(BaseModel):
    coordinates: List[OrderedPoint]


class WorkerGetResponse(BaseModel):
    id: str
    status: CeleryStatus
    result: OptimizerResponse
    create_dtm: Optional[datetime] = None

    @validator("create_dtm", always=True)
    def set_create_dtm(cls, value: datetime) -> datetime:
        return value or datetime.now()


class Points(BaseModel):
    coordinates: List[Point]

    @classmethod
    def unpack(cls, payload):
        return [(p.longitude, p.latitude) for p in payload.coordinates]


class Payload(BaseModel):
    payload: Points

    @classmethod
    def unpack(cls, payload):
        return [(p.longitude, p.latitude) for p in payload.payload.coordinates]
