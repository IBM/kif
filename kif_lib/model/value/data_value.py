# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, TypeAlias
from .value import Value, ValueTemplate, ValueVariable

DataValueClass: TypeAlias = type['DataValue']
DataValueTemplateClass: TypeAlias = type['DataValueTemplate']
DataValueVariableClass: TypeAlias = type['DataValueVariable']


class DataValueTemplate(ValueTemplate):
    """Abstract base class for data value templates."""

    object_class: ClassVar[DataValueClass]  # pyright: ignore


class DataValueVariable(ValueVariable):
    """Data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[DataValueClass]  # pyright: ignore


class DataValue(
        Value,
        template_class=DataValueTemplate,
        variable_class=DataValueVariable
):
    """Abstract base class for data values."""

    template_class: ClassVar[DataValueTemplateClass]  # pyright: ignore
    variable_class: ClassVar[DataValueVariableClass]  # pyright: ignore
