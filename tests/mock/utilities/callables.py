from datetime import datetime
from json import load as load_from_json
from typing import Any

from .constants import GENERIC_JSON_FILE_PATH


def get_records_data_from_json(file_name: str) -> list[dict[str, Any]]:
    record_data_list: list[dict[str, Any]] = []

    with open(
        file=GENERIC_JSON_FILE_PATH.format(file_name),
        mode='r',
    ) as json_file:
        for record_data in load_from_json(json_file):
            due_date: str | None = record_data.get('due_date')
            due_time: str | None = record_data.get('due_time')

            if due_date is not None:
                record_data['due_date'] = datetime.strptime(due_date, '%Y-%m-%d').date()
            if due_time is not None:
                record_data['due_time'] = datetime.strptime(due_time, '%H:%M').time()

            record_data_list.append(record_data)

    return record_data_list
