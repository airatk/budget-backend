from enum import Enum, EnumMeta
from typing import Any, Iterable, cast


def persist_enumeration_values(enumeration: EnumMeta) -> list[Any]:
    return [ enumeration_type.value for enumeration_type in cast(Iterable[Enum], enumeration) ]
