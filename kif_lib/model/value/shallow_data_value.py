# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ...typing import Any, cast, ClassVar, Location, override, Self
from .data_value import DataValue, DataValueTemplate, DataValueVariable

if TYPE_CHECKING:  # pragma: no cover
    from .string import VStringContent


class ShallowDataValueTemplate(DataValueTemplate):
    """Abstract base class for shallow data value templates."""

    object_class: ClassVar[type[ShallowDataValue]]  # pyright: ignore

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        from .string import StringVariable
        if i == 1:              # content
            return StringVariable.check(arg, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def content(self) -> VStringContent:
        """The content of shallow data value template."""
        return self.get_content()

    def get_content(self) -> VStringContent:
        """Gets the content of shallow data value.

        Returns:
           String content or string variable.
        """
        return self.args[0]


class ShallowDataValueVariable(DataValueVariable):
    """Shallow data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ShallowDataValue]]  # pyright: ignore


class ShallowDataValue(
        DataValue,
        template_class=ShallowDataValueTemplate,
        variable_class=ShallowDataValueVariable
):
    """Abstract base class for shallow data values."""

    template_class: ClassVar[type[ShallowDataValueTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ShallowDataValueVariable]]  # pyright: ignore

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        from .string import String
        if isinstance(arg, cls):
            return arg
        if cls is ShallowDataValue:
            if isinstance(arg, str):
                return cast(Self, String(arg))
        else:                   # concrete subclass?
            if isinstance(arg, String):
                return cls(arg.content)
            if isinstance(arg, str):
                return cls(str(arg))
        raise cls._check_error(arg, function, name, position)

    @property
    def content(self) -> str:
        """The content of shallow data value."""
        return self.get_content()

    def get_content(self) -> str:
        """Gets the content of shallow data value.

        Returns:
           String content.
        """
        return self.args[0]
