from typing import Type

from fastapi import status

from core.databases.models.utilities.base import BaseModel

from .response import BaseApiException


class CouldNotFindRecord(BaseApiException):
    def __init__(self, record_id: int, record_type: Type[BaseModel] | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message='Could not find the record of the {record_type} with given ID of {record_id}'.format(
                record_id=record_id,
                record_type=record_type.__class__.__name__ if record_type else 'Model',
            ),
            error_data={
                'id': record_id,
            },
        )

class CouldNotAccessRecord(BaseApiException):
    def __init__(self, record_id: int, record_type: Type[BaseModel] | None = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message='Could not access the record of the {record_type} with given ID of {record_id}'.format(
                record_id=record_id,
                record_type=record_type.__class__.__name__ if record_type else 'Model',
            ),
            error_data={
                'id': record_id,
            },
        )

class CouldNotAccessRecords(BaseApiException):
    def __init__(self, record_ids: list[int], record_type: Type[BaseModel] | None = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message='Could not access the records of the {record_type} with given IDs'.format(
                record_type=record_type.__class__.__name__ if record_type else 'Model',
            ),
            error_data={
                'ids': record_ids,
            },
        )
