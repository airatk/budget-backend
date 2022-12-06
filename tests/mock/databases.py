from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from models import Account, Budget, Category, Family, Transaction, User
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
            User(username="test-user", password="test-password"),  # noqa: S106
            User(username="family-member", password="test-password")  # noqa: S106
        ]
        families: list[Family] = [
            Family(access_code="password", members=users)
        ]
        accounts: list[Account] = [
            Account(user=users[0], name="Account 1", currency=CurrencyType.RUB, openning_balance=0.00),
            Account(user=users[0], name="Account 2", currency=CurrencyType.RUB, openning_balance=0.00),
            Account(user=users[0], name="Account 3", currency=CurrencyType.RUB, openning_balance=0.00),

            Account(user=users[1], name="Account 1", currency=CurrencyType.RUB, openning_balance=0.00)
        ]
        categories: list[Category] = [
            Category(user=users[0], name="Category 1", type=CategoryType.INCOME),
            Category(user=users[0], name="Category 2", type=CategoryType.INCOME),
            Category(user=users[0], name="Category 3", type=CategoryType.OUTCOME),
            Category(user=users[0], name="Category 4", type=CategoryType.OUTCOME),

            Category(user=users[1], name="Category 1", type=CategoryType.INCOME),
            Category(user=users[1], name="Category 2", type=CategoryType.OUTCOME)
        ]
        budgets: list[Budget] = [
            Budget(family=families[0], categories=categories, name="Budget 1", planned_outcomes=100000.00),
            Budget(user=users[0], categories=categories, name="Budget 2", planned_outcomes=20000.00)
        ]
        transactions: list[Transaction] = [
            Transaction(account=accounts[0], category=categories[0], type=TransactionType.INCOME, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
            Transaction(account=accounts[0], category=categories[0], type=TransactionType.OUTCOME, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
            Transaction(account=accounts[0], category=categories[0], type=TransactionType.TRANSFER, due_date="2022-12-12", due_time="10:40", amount=100.00, note="Note"),
        ]

        test_postgres_session.add_all([ *users, *families, *accounts, *categories, *budgets, *transactions ])
        test_postgres_session.commit()
