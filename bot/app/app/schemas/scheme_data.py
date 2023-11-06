from pydantic import BaseModel
from datetime import datetime
from app.schemas.constraint import GroupTo


class DataRequest(BaseModel):
    """Db request data scheme
    """
    dt_from: datetime
    dt_upto: datetime
    group_type: GroupTo

    class Config:

        json_schema_extra = {
            "example": {
                "dt_from": "2022-09-01T00:00:00",
                "dt_upto": "2022-12-31T23:59:00",
                "group_type": "month"
                    }
                }


class DataResponse(BaseModel):
    """Db response data scheme
    """
    dataset: list[int]
    labels: list[datetime]

    class Config:

        json_schema_extra = {
            "example": {
                "dataset": [5906586, 5515874, 5889803, 6092634],
                "labels": [
                    "2022-09-01T00:00:00", "2022-10-01T00:00:00",
                    "2022-11-01T00:00:00", "2022-12-01T00:00:00"
                        ]
                        }
                    }
