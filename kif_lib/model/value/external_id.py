# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...typing import ClassVar, TypeAlias, Union
from .string import (
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    TString,
    VTStringContent,
)

ExternalIdClass: TypeAlias = type['ExternalId']
ExternalIdDatatypeClass: TypeAlias = type['ExternalIdDatatype']
ExternalIdTemplateClass: TypeAlias = type['ExternalIdTemplate']
ExternalIdVariableClass: TypeAlias = type['ExternalIdVariable']

TExternalId: TypeAlias = Union['ExternalId', TString]
VExternalId: TypeAlias =\
    Union['ExternalIdTemplate', 'ExternalIdVariable', 'ExternalId']


class ExternalIdTemplate(StringTemplate):
    """External id template.

    Parameters:
       content: External id content or string variable.
    """

    object_class: ClassVar[ExternalIdClass]  # pyright: ignore

    def __init__(self, content: VTStringContent):
        super().__init__(content)


class ExternalIdVariable(StringVariable):
    """External id variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[ExternalIdClass]  # pyright: ignore


class ExternalIdDatatype(StringDatatype):
    """External id datatype."""

    value_class: ClassVar[ExternalIdClass]  # pyright: ignore


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

    datatype_class: ClassVar[ExternalIdDatatypeClass]  # pyright: ignore
    datatype: ClassVar[ExternalIdDatatype]             # pyright: ignore
    template_class: ClassVar[ExternalIdTemplateClass]  # pyright: ignore
    variable_class: ClassVar[ExternalIdVariableClass]  # pyright: ignore

    def __init__(self, content: VTStringContent):
        super().__init__(content)
