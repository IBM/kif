# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses
import os

from ..typing import Any, ClassVar, Iterator, Optional, Self


@dataclasses.dataclass
class Section:
    """Section in KIF options."""

    #: Name of this section.
    name: ClassVar[str]

    def __init_subclass__(cls, **kwargs):
        cls.name = kwargs.get('name', cls.__qualname__)

    @classmethod
    def getenv(cls, name: str, default: Optional[Any] = None) -> Any:
        return os.getenv(name, default)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        def it():
            for field in dataclasses.fields(cls):
                if field.name not in data:
                    continue
                if (isinstance(field.default_factory, type)
                        and issubclass(field.default_factory, Section)):
                    yield (field.name,
                           field.default_factory.from_dict(data[field.name]))
                else:
                    yield (field.name, data[field.name])
        return cls(**dict(it()))

    def __str__(self) -> str:
        return self.to_str()

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    def to_str(self) -> str:
        return '\n'.join(self._to_str(self.name))

    def _to_str(self, prefix: str) -> Iterator[str]:
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if field.name[0] == '_':
                name = prefix + '.' + field.name[1:]
            else:
                name = prefix + '.' + field.name
            if isinstance(value, Section):
                yield from value._to_str(name)
            else:
                yield f'{name}: {field.type.__qualname__} = {value}'
