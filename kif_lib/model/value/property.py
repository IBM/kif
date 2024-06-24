# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing_extensions import overload, TYPE_CHECKING

from ...itertools import chain
from ...typing import (
    Any,
    ClassVar,
    Iterable,
    Optional,
    override,
    TypeAlias,
    Union,
)
from ..template import Template
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable, VTEntity
from .iri import T_IRI, VT_IRI
from .value import Datatype, DatatypeVariable, VDatatype, VTDatatype, VTValue

if TYPE_CHECKING:               # pragma: no cover
    from ..snak import ValueSnak, ValueSnakTemplate
    from ..statement import Statement, StatementTemplate

PropertyClass: TypeAlias = type['Property']
PropertyDatatypeClass: TypeAlias = type['PropertyDatatype']
PropertyTemplateClass: TypeAlias = type['PropertyTemplate']
PropertyVariableClass: TypeAlias = type['PropertyVariable']

TProperty: TypeAlias = Union['Property', T_IRI]
VProperty: TypeAlias =\
    Union['PropertyTemplate', 'PropertyVariable', 'Property']
VTPropertyContent: TypeAlias = Union['PropertyTemplate', Variable, TProperty]


class PropertyTemplate(EntityTemplate):
    """Property template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
       range: Datatype or datatype variable.
    """

    object_class: ClassVar[PropertyClass]  # pyright: ignore

    def __init__(
            self,
            iri: VT_IRI,
            range: Optional[VTDatatype] = None
    ):
        super().__init__(iri, range)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            if isinstance(arg, (Template, Variable)):
                return super()._preprocess_arg(arg, i)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        elif i == 2:            # range
            if Variable.test(arg):
                return DatatypeVariable.check(arg, type(self), None, i)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> 'StatementTemplate':
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> 'ValueSnakTemplate':
        ...                     # pragma: no cover

    def __call__(self, v1, v2=None):
        if v2 is not None:
            return self._StatementTemplate(v1, self._ValueSnak(self, v2))
        else:
            return self._ValueSnakTemplate(self, v1)

    @property
    def range(self) -> Optional[VDatatype]:
        """The range of property template."""
        return self.get_range()

    def get_range(
            self,
            default: Optional[VDatatype] = None
    ) -> Optional[VDatatype]:
        """Gets the range of property template.

        If range is ``None``, returns `default`.

        Parameters:
           default: Default range.

        Returns:
           Datatype or datatype variable.
        """
        range = self.args[1]
        return range if range is not None else default


class PropertyVariable(EntityVariable):
    """Property variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[PropertyClass]  # pyright: ignore

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> 'StatementTemplate':
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> 'ValueSnakTemplate':
        ...                     # pragma: no cover

    def __call__(self, v1, v2=None):
        if v2 is not None:
            return self._StatementTemplate(v1, self._ValueSnak(self, v2))
        else:
            return self._ValueSnakTemplate(self, v1)


class PropertyDatatype(Datatype):
    """Property datatype."""

    value_class: ClassVar[PropertyClass]  # pyright: ignore


class Property(
        Entity,
        datatype_class=PropertyDatatype,
        template_class=PropertyTemplate,
        variable_class=PropertyVariable
):
    """Binary relationship.

    Parameters:
       iri: IRI.
       range: Datatype.
    """

    datatype_class: ClassVar[PropertyDatatypeClass]  # pyright: ignore
    datatype: ClassVar[PropertyDatatype]             # pyright: ignore
    template_class: ClassVar[PropertyTemplateClass]  # pyright: ignore
    variable_class: ClassVar[PropertyVariableClass]  # pyright: ignore

    def __init__(
            self,
            iri: VTPropertyContent,
            range: Optional[VTDatatype] = None
    ):
        super().__init__(iri, range)

    @staticmethod
    @override
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            return Entity._static_preprocess_arg(self_, arg, i)
        elif i == 2:            # range
            return Datatype.check_optional(arg, None, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> 'Statement':
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> 'ValueSnak':
        ...                     # pragma: no cover

    def __call__(self, v1, v2=None):
        if v2 is not None:
            return self._Statement(v1, self._ValueSnak(self, v2))
        else:
            return self._ValueSnak(self, v1)

    @property
    def range(self) -> Optional[Datatype]:
        """The range of property."""
        return self.get_range()

    def get_range(
            self,
            default: Optional[Datatype] = None
    ) -> Optional[Datatype]:
        """Gets the range of property.

        If range is ``None``, returns `default`.

        Parameters:
           default: Default range.

        Returns:
           Datatype.
        """
        range = self.args[1]
        return range if range is not None else default


def Properties(
        iri: VTPropertyContent,
        *iris: VTPropertyContent
) -> Iterable[Property]:
    """Constructs one or more properties.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting properties.
    """
    return map(Property, chain([iri], iris))
