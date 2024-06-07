# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, TypeAlias
from .data_value import DataValue, DataValueTemplate, DataValueVariable

DeepDataValueClass: TypeAlias = type['DeepDataValue']
DeepDataValueTemplateClass: TypeAlias = type['DeepDataValueTemplate']
DeepDataValueVariableClass: TypeAlias = type['DeepDataValueVariable']


class DeepDataValueTemplate(DataValueTemplate):
    """Abstract base class for deep data value templates."""

    object_class: ClassVar[DeepDataValueClass]


class DeepDataValueVariable(DataValueVariable):
    """Deep data value variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[DeepDataValueClass]


class DeepDataValue(
        DataValue,
        template_class=DeepDataValueTemplate,
        variable_class=DeepDataValueVariable
):
    """Abstract base class for deep data values."""

    template_class: ClassVar[DeepDataValueTemplateClass]
    variable_class: ClassVar[DeepDataValueVariableClass]
