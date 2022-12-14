from itertools import chain

from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from models import Account, Budget, Category, Family, Transaction, User
from models.utilities.base import BaseModel
from models.utilities.types import CategoryType, CurrencyType, TransactionType

from .settings import test_settings


test_postgres_engine: Engine = create_engine(url=test_settings.POSTGRES_URL)

TestPostgresSession: sessionmaker = sessionmaker(
    bind=test_postgres_engine,
    autocommit=False,
    autoflush=False
)


def fill_up_test_database():
    with TestPostgresSession() as test_postgres_session:
        users: list[User] = [
            User(id=1, username="test-user", password="test-password"),  # noqa: S106
            User(id=2, username="family-member", password="test-password")  # noqa: S106
        ]
        families: list[Family] = [
            Family(id=1, access_code="password", members=users)
        ]
        accounts: list[Account] = [
            Account(id=1, user=users[0], name="Account 1", currency=CurrencyType.RUB, openning_balance=0.00),
            Account(id=2, user=users[0], name="Account 2", currency=CurrencyType.RUB, openning_balance=0.00),
            Account(id=3, user=users[0], name="Account 3", currency=CurrencyType.RUB, openning_balance=0.00),

            Account(id=4, user=users[1], name="Account 1", currency=CurrencyType.RUB, openning_balance=0.00)
        ]
        categories: list[Category] = [
            Category(id=1, user=users[0], name="Category 1", type=CategoryType.INCOME),
            Category(id=2, user=users[0], name="Category 2", type=CategoryType.INCOME),
            Category(id=3, user=users[0], name="Category 3", type=CategoryType.OUTCOME),
            Category(id=4, user=users[0], name="Category 4", type=CategoryType.OUTCOME),

            Category(id=5, user=users[1], name="Category 1", type=CategoryType.INCOME),
            Category(id=6, user=users[1], name="Category 2", type=CategoryType.OUTCOME)
        ]
        budgets: list[Budget] = [
            Budget(id=1, family=families[0], categories=categories, name="Budget 1", planned_outcomes=100000.00),
            Budget(id=2, user=users[0], categories=categories, name="Budget 2", planned_outcomes=20000.00)
        ]
        transactions: list[Transaction] = [
            Transaction(id=1, account=accounts[0], category=categories[0], type=TransactionType.INCOME, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
            Transaction(id=2, account=accounts[0], category=categories[0], type=TransactionType.OUTCOME, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
            Transaction(id=3, account=accounts[0], category=categories[0], type=TransactionType.TRANSFER, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
        ]

        tables: tuple[list[BaseModel]] = (
            users,
            families,
            accounts,
            categories,
            budgets,
            transactions
        )
        sequence_next_values: tuple[int] = tuple(
            len(table) + 1 for table in tables
        )
        sequence_ids: tuple[str] = (
            "user_id_seq",
            "family_id_seq",
            "account_id_seq",
            "category_id_seq",
            "budget_id_seq",
            "transaction_id_seq"
        )

        test_postgres_session.add_all(chain(*tables))

        for (sequence_id, next_sequence_value) in zip(sequence_ids, sequence_next_values):
            test_postgres_session.execute(
                "ALTER SEQUENCE {0} RESTART WITH {1}".format(sequence_id, next_sequence_value)
            )

        test_postgres_session.commit()
