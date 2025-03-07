# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from ...typing import Any, ClassVar, override, TypeAlias, TypedDict, Union
from ..term import Variable
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .string import String, TString
from .value import Datatype

if TYPE_CHECKING:               # pragma: no cover
    from ...store import Store

T_IRI: TypeAlias = Union['IRI', TString]
V_IRI: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'IRI']
VT_IRI: TypeAlias = Union[Variable, V_IRI, T_IRI]
VT_IRI_Content: TypeAlias = Union[Variable, T_IRI]


class IRI_Template(ShallowDataValueTemplate):
    """IRI template.

    Parameters:
       content: IRI content or string variable.
    """

    object_class: ClassVar[type[IRI]]  # pyright: ignore

    def __init__(self, content: VT_IRI_Content) -> None:
        super().__init__(content)


class IRI_Variable(ShallowDataValueVariable):
    """IRI variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[IRI]]  # pyright: ignore


class IRI_Datatype(Datatype):
    """IRI datatype."""

    instance: ClassVar[IRI_Datatype]  # pyright: ignore
    value_class: ClassVar[type[IRI]]  # pyright: ignore


class IRI(
        ShallowDataValue,
        datatype_class=IRI_Datatype,
        template_class=IRI_Template,
        variable_class=IRI_Variable
):
    """IRI.

    Parameters:
       content: IRI content.
    """

    datatype_class: ClassVar[type[IRI_Datatype]]  # pyright: ignore
    datatype: ClassVar[IRI_Datatype]              # pyright: ignore
    template_class: ClassVar[type[IRI_Template]]  # pyright: ignore
    variable_class: ClassVar[type[IRI_Variable]]  # pyright: ignore

    class Descriptor(TypedDict, total=False):
        """IRI descriptor."""

        #: Prefix.
        prefix: str

        #: Entity resolver.
        resolver: Store

    def __init__(self, content: VT_IRI_Content) -> None:
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_: IRI, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, IRI):
                return arg.content
            else:
                return String.check(arg, type(self_), None, i).content
        else:
            raise self_._should_not_get_here()

    def describe(self) -> IRI.Descriptor | None:
        """Gets the descriptor of IRI in KIF context.

        Returns:
           IRI descriptor or ``None``.
        """
        return self.context.describe(self, function=self.describe)

    def register(
            self,
            prefix: TString | None = None,
            resolver: Store | None = None,
    ) -> IRI:
        """Adds or updates IRI data in KIF context.

        Parameters:
           prefix: Prefix.
           resolver: Resolver store.

        Returns:
           IRI.
        """
        return self.context.iris.register(
            self, prefix=prefix, resolver=resolver, function=self.register)

    def unregister(
            self,
            prefix: bool = False,
            resolver: bool = False,
            all: bool = False,
    ) -> bool:
        """Remove IRI data from KIF context.

        If called with no arguments, removes all IRI data.

        Parameters:
           prefix: Whether to remove prefix.
           resolver: Whether to remove resolver.
           all: Whether to remove all data.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        if prefix is False and resolver is False:
            return self.context.iris.unregister(
                self, all=True, function=self.unregister)
        else:
            return self.context.iris.unregister(
                self, prefix=prefix, resolver=resolver,
                function=self.unregister)
