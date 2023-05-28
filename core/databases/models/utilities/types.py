from enum import StrEnum


class BudgetType(StrEnum):
    JOINT = 'joint'
    PERSONAL = 'personal'

class SummaryPeriodType(StrEnum):
    CURRENT_MONTH = 'Current Month'
    CURRENT_YEAR = 'Current Year'
    ALL_TIME = 'All Time'

class TransactionType(StrEnum):
    INCOME = 'Income'
    OUTCOME = 'Outcome'
    TRANSFER = 'Transfer'

class CategoryType(StrEnum):
    INCOME = 'Income'
    OUTCOME = 'Outcome'

class CurrencyType(StrEnum):
    RUB = 'RUB'
    USD = 'USD'
