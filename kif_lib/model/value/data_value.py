# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import TypeAlias
from .value import Value, ValueTemplate, ValueVariable

DataValueClass: TypeAlias = type['DataValue']
DataValueTemplateClass: TypeAlias = type['DataValueTemplate']
DataValueVariableClass: TypeAlias = type['DataValueVariable']


class DataValueTemplate(ValueTemplate):
    """Abstract base class for data value templates."""

    object_class: DataValueClass


class DataValueVariable(ValueVariable):
    """Data value variable.

    Parameters:
       name: Name.
    """

    object_class: DataValueClass


class DataValue(
        Value,
        template_class=DataValueTemplate,
        variable_class=DataValueVariable
):
    """Abstract base class for data values."""

    template_class: DataValueTemplateClass
    variable_class: DataValueVariableClass
