from typing import TypeVar, Generic, Type, Any
from pydantic import BaseModel
from pymongo.client_session import ClientSession
from app.schemas.scheme_data import DataRequest, DataResponse
from app.schemas.constraint import Collections, GroupTo
from app.config import settings


SchemaDbType = TypeVar("SchemaDbType", bound=BaseModel)
SchemaReturnType = TypeVar("SchemaReturnType", bound=BaseModel)


class CRUDBase(Generic[SchemaDbType]):
    def __init__(
        self,
        schema: Type[SchemaReturnType],
        col_name: str,
        db_name: str = settings.DB_NAME
            ):
        """
        CRUD object with default methods to Create,
        Read, Update, Delete (CRUD).
        """
        self.schema = schema
        self.col_name = col_name
        self.db_name = db_name


class CRUDData(CRUDBase[DataRequest]):
    """Data crud
    """

    @staticmethod
    def make_date(group_type: GroupTo) -> dict[str, Any]:
        """Make date pattern
        """
        match group_type:
            case GroupTo.MONTH:
                f = "%Y-%m-01T00:00:00"
            case GroupTo.DAY:
                f = "%Y-%m-%dT00:00:00"
            case GroupTo.HOUR:
                f = "%Y-%m-%dT%H:00:00"
        return {"$dateToString": {
            "date": "$dt",
            "format": f,
                }}

    @staticmethod
    def make_aggr(group_type: GroupTo, dt: dict[str, Any]) -> dict[str, Any]:
        """Make aggregation pattern
        """
        aggr = {"_id": {
                    "hour": {"$hour": "$dt"},
                    "day": {"$dayOfMonth": "$dt"},
                    "month": {"$month": "$dt"},
                    "year": {"$year": "$dt"},
                        },
                "v_sum": {"$sum": '$value'},
                "v_date": {"$first": dt}
                }
        match group_type:
            case GroupTo.MONTH:
                del aggr['_id']["day"]
                del aggr['_id']["hour"]
            case GroupTo.DAY:
                del aggr['_id']["hour"]

        return aggr

    async def get_grouped(
        self,
        session: ClientSession,
        q: DataRequest,
            ) -> DataResponse:
        """Get single document

        Args:
            session (ClientSession): session
            q: (DataRequest): query filter data

        Returns:
            DataResponse: search result
        """
        dt = self.make_date(q.group_type)
        aggr = self.make_aggr(q.group_type, dt)

        pipeline = [
            {"$match": {"dt": {"$gte": q.dt_from, "$lt": q.dt_upto}}},
            {"$group": aggr},
            {"$sort": {"v_date": 1}}
                ]

        collect = {'dataset': [], 'labels': []}
        async for row in session.client[self.db_name][self.col_name].aggregate(pipeline):
            collect['dataset'].append(row['v_sum'])
            collect['labels'].append(row['v_date'])
        return DataResponse(**collect)


data = CRUDData(
    schema=DataResponse,
    col_name=Collections.SAMPLE_COLLECTION.value,
    db_name=settings.DB_NAME,
        )
