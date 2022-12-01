from enum import Enum


class BaseType(str, Enum):
    def __repr__(self) -> str:
        return self.value


class BudgetType(BaseType):
    JOINT = "joint"
    PERSONAL = "personal"

class SummaryPeriodType(BaseType):
    CURRENT_MONTH = "Current Month"
    CURRENT_YEAR = "Current Year"
    ALL_TIME = "All Time"

class TransactionType(BaseType):
    INCOME = "Income"
    OUTCOME = "Outcome"
    TRANSFER = "Transfer"

class CategoryType(BaseType):
    INCOME = "Income"
    OUTCOME = "Outcome"

class CurrencyType(BaseType):
    RUB = "RUB"
    USD = "USD"
