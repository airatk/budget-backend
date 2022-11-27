from typing import Any
from typing import cast
from typing import Iterable

from enum import EnumMeta
from enum import Enum


def persist_enumeration_values(enumeration: EnumMeta) -> list[Any]:
    return [ enumeration_type.value for enumeration_type in cast(Iterable[Enum], enumeration) ]
