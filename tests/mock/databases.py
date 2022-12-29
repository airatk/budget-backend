from itertools import chain
from json import load as load_from_json
from typing import Type, TypeAlias

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from core.databases.models import (
    Account,
    Budget,
    Category,
    Family,
    Transaction,
    User,
)
from core.databases.models.utilities.base import BaseModel

from .settings import test_settings


test_postgres_engine: Engine = create_engine(url=test_settings.POSTGRES_URL)  # type: ignore [arg-type]

TestPostgresSession: sessionmaker = sessionmaker(
    bind=test_postgres_engine,
    autocommit=False,
    autoflush=False,
)


DatabaseMapping: TypeAlias = tuple[Type[BaseModel], str, str]

def fill_up_test_database():  # noqa: WPS210
    generic_json_file_path: str = "tests/mock/data/{0}.json"
    data_mapping: tuple[DatabaseMapping, ...] = (
        (User, "users", "user_id_seq"),
        (Family, "families", "family_id_seq"),
        (Account, "accounts", "account_id_seq"),
        (Category, "categories", "category_id_seq"),
        (Budget, "budgets", "budget_id_seq"),
        (Transaction, "transactions", "transaction_id_seq"),
    )

    tables: list[list[BaseModel]] = []
    sequence_data: dict[str, int] = {}

    for (model, data_type, sequence_id) in data_mapping:
        with open(file=generic_json_file_path.format(data_type), mode="r") as json_file:
            tables.append([
                model(**json_list_item_data) for json_list_item_data in load_from_json(json_file)
            ])

        sequence_data[sequence_id] = len(tables[-1]) + 1

    with TestPostgresSession() as test_postgres_session:
        test_postgres_session.add_all(chain(*tables))

        for (sequence_id, next_sequence_value) in sequence_data.items():  # noqa: WPS440
            test_postgres_session.execute(
                "ALTER SEQUENCE {0} RESTART WITH {1}".format(sequence_id, next_sequence_value),
            )

        test_postgres_session.commit()
