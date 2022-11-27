from enum import Enum


class BudgetType(str, Enum):
    JOINT: str = "joint"
    PERSONAL: str = "personal"

    def __repr__(self) -> str:
        return self.value

class SummaryPeriodType(str, Enum):
    CURRENT_MONTH: str = "Current Month"
    CURRENT_YEAR: str = "Current Year"
    ALL_TIME: str = "All Time"

    def __repr__(self):
        return self.value

class TransactionType(str, Enum):
    INCOME: str = "Income"
    OUTCOME: str = "Outcome"
    TRANSFER: str = "Transfer"

    def __repr__(self) -> str:
        return self.value

class CategoryType(str, Enum):
    INCOME: str = "Income"
    OUTCOME: str = "Outcome"

    def __repr__(self) -> str:
        return self.value

class CurrencyType(str, Enum):
    RUB: str = "RUB"
    USD: str = "USD"

    def __repr__(self) -> str:
        return self.value
