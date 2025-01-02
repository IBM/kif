# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum

from ..typing import Any, Location, Self
from .kif_object import KIF_Object


class Flags(enum.Flag):
    """Base class for flags."""

    @classmethod
    def auto(cls) -> Any:
        """Alias of :func:`enum.auto`."""
        return enum.auto()

    @classmethod
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        """Coerces `arg` into an instance of this class.

        If `arg` cannot be coerced, raises an error.

        Parameters:
           arg: Value.
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           Flags.
        """
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, int):
            try:
                return cls(arg)
            except ValueError as err:
                raise KIF_Object._check_error(
                    arg, function or cls.check, name, position,
                    ValueError, to_=cls.__qualname__) from err
        else:
            raise KIF_Object._check_error(
                arg, function or cls.check, name, position,
                to_=cls.__qualname__)

    @classmethod
    def check_optional(
            cls,
            arg: Any | None,
            default: Any | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self | None:
        """Coerces optional `arg` into an instance of this class.

        If `arg` cannot be coerced, raises an error.

        If `arg` is ``None``, returns `default`.

        Parameters:
           arg: Value.
           default: Default value.
           function: Function or function name.
           name: Argument name.
           position: Argument position.

        Returns:
           Flags or `default`.
        """
        if arg is None:
            arg = default
        if arg is None:
            return arg
        else:
            return cls.check(arg, function, name, position)
