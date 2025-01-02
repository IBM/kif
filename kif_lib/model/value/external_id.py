# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import ClassVar, TypeAlias, Union
from .string import (
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    TString,
)

TExternalId: TypeAlias = Union['ExternalId', TString]
VExternalId: TypeAlias =\
    Union['ExternalIdTemplate', 'ExternalIdVariable', 'ExternalId']


class ExternalIdTemplate(StringTemplate):
    """External id template.

    Parameters:
       content: External id content or string variable.
    """

    object_class: ClassVar[type[ExternalId]]  # pyright: ignore


class ExternalIdVariable(StringVariable):
    """External id variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[ExternalId]]  # pyright: ignore


class ExternalIdDatatype(StringDatatype):
    """External id datatype."""

    instance: ClassVar[ExternalIdDatatype]  # pyright: ignore
    value_class: ClassVar[type[ExternalId]]  # pyright: ignore


class ExternalId(
        String,
        datatype_class=ExternalIdDatatype,
        template_class=ExternalIdTemplate,
        variable_class=ExternalIdVariable
):
    """External id.

    Parameters:
       content: External id content.
    """

    datatype_class: ClassVar[type[ExternalIdDatatype]]  # pyright: ignore
    datatype: ClassVar[ExternalIdDatatype]              # pyright: ignore
    template_class: ClassVar[type[ExternalIdTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[ExternalIdVariable]]  # pyright: ignore
