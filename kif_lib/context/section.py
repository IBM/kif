# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import os

from ..typing import Any, ClassVar, Iterator, Self


@dataclasses.dataclass
class Section:
    """Section in KIF options."""

    #: Name of this section.
    name: ClassVar[str]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        cls.name = kwargs.get('name', cls.__qualname__)

    @classmethod
    def getenv(cls, name: str, default: Any | None = None) -> Any:
        """Alias for :func:`os.getenv`."""
        return os.getenv(name, default)

    @classmethod
    def from_ast(cls, ast: dict[str, Any]) -> Self:
        """Converts abstract syntax tree to section.

        Parameters:
           ast: Abstract syntax tree.

        Returns:
           Section.
        """
        def it() -> Iterator[tuple[str, Any]]:
            for field in dataclasses.fields(cls):
                if field.name not in ast:
                    continue
                if (isinstance(field.default_factory, type)
                        and issubclass(field.default_factory, Section)):
                    yield (field.name,
                           field.default_factory.from_ast(ast[field.name]))
                else:
                    yield (field.name, ast[field.name])
        return cls(**dict(it()))

    def to_ast(self) -> dict[str, Any]:
        """Converts section to abstract syntax tree.

        Returns:
           Dictionary.
        """
        return dataclasses.asdict(self)

    def __str__(self) -> str:
        return self.to_str()

    def to_str(self) -> str:
        """Converts section to string.

        Returns:
           String.
        """
        return '\n'.join(self._to_str(self.name))

    def _to_str(self, prefix: str) -> Iterator[str]:
        for field in sorted(dataclasses.fields(self), key=lambda f: f.name):
            name = prefix + '.' + field.name
            value = getattr(self, field.name)
            if isinstance(value, Section):
                yield from value._to_str(name)
            else:
                if isinstance(field.type, type):
                    type_name = field.type.__qualname__
                else:
                    type_name = str(field.type)
                yield f'{name}: {type_name} = {value}'
