# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import ClassVar
from .value import Value, ValueTemplate, ValueVariable


class DataValueTemplate(ValueTemplate):
    """Abstract base class for data value templates."""

    object_class: ClassVar[type[DataValue]]  # pyright: ignore


class DataValueVariable(ValueVariable):
    """Data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[DataValue]]  # pyright: ignore


class DataValue(
        Value,
        template_class=DataValueTemplate,
        variable_class=DataValueVariable
):
    """Abstract base class for data values."""

    template_class: ClassVar[type[DataValueTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[DataValueVariable]]  # pyright: ignore
