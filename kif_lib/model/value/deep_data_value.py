# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import ClassVar
from .data_value import DataValue, DataValueTemplate, DataValueVariable


class DeepDataValueTemplate(DataValueTemplate):
    """Abstract base class for deep data value templates."""

    object_class: ClassVar[type[DeepDataValue]]  # pyright: ignore


class DeepDataValueVariable(DataValueVariable):
    """Deep data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[DeepDataValue]]  # pyright: ignore


class DeepDataValue(
        DataValue,
        template_class=DeepDataValueTemplate,
        variable_class=DeepDataValueVariable
):
    """Abstract base class for deep data values."""

    template_class: ClassVar[type[DeepDataValueTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[DeepDataValueVariable]]  # pyright: ignore
