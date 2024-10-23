# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import overload

from ...typing import Any, ClassVar, Iterable, override, TypeAlias, Union
from ..term import OpenTerm, Variable
from .datatype import Datatype, DatatypeVariable, VDatatype, VTDatatype
from .entity import Entity, EntityTemplate, EntityVariable, VTEntity
from .iri import IRI_Template, T_IRI, VT_IRI
from .item import ItemDatatype
from .text import TextDatatype
from .value import VTValue

if TYPE_CHECKING:               # pragma: no cover
    from ..snak import (
        NoValueSnak,
        NoValueSnakTemplate,
        SomeValueSnak,
        SomeValueSnakTemplate,
        ValueSnak,
        ValueSnakTemplate,
    )
    from ..statement import Statement, StatementTemplate

TProperty: TypeAlias = Union['Property', T_IRI]
VProperty: TypeAlias =\
    Union['PropertyTemplate', 'PropertyVariable', 'Property']
VTProperty: TypeAlias = Union[Variable, VProperty, TProperty]
VTPropertyContent: TypeAlias = Union[Variable, IRI_Template, TProperty]


class PropertyTemplate(EntityTemplate):
    """Property template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
       range: Datatype or datatype variable.
    """

    object_class: ClassVar[type[Property]]  # pyright: ignore

    def __init__(self, iri: VT_IRI, range: VTDatatype | None = None) -> None:
        super().__init__(iri, range)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # iri
            if isinstance(arg, OpenTerm):
                return super()._preprocess_arg(arg, i)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        elif i == 2:            # range
            if isinstance(arg, Variable):
                return DatatypeVariable.check(arg, type(self), None, i)
            else:
                return Property._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> StatementTemplate:
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> ValueSnakTemplate:
        ...                     # pragma: no cover

    def __call__(
            self,
            v1: VTEntity | VTValue,
            v2: VTValue | None = None
    ) -> StatementTemplate | ValueSnakTemplate:
        if v2 is not None:
            from ..snak import ValueSnak
            from ..statement import StatementTemplate
            return StatementTemplate(v1, ValueSnak(self, v2))  # type: ignore
        else:
            from ..snak import ValueSnakTemplate
            return ValueSnakTemplate(self, v1)

    @property
    def range(self) -> VDatatype | None:
        """The range of property template."""
        return self.get_range()

    def get_range(self, default: VDatatype | None = None) -> VDatatype | None:
        """Gets the range of property template.

        If range is ``None``, returns `default`.

        Parameters:
           default: Default range.

        Returns:
           Datatype or datatype variable.
        """
        return self.get(1, default)

    def no_value(self) -> NoValueSnakTemplate:
        """Constructs a no-value snak template from property template.

        Returns:
           No-value snak template.
        """
        from ..snak import NoValueSnakTemplate
        return NoValueSnakTemplate(self)

    def some_value(self) -> SomeValueSnakTemplate:
        """Constructs a some-value snak template from property template.

        Returns:
           Some-value snak template.
        """
        from ..snak import SomeValueSnakTemplate
        return SomeValueSnakTemplate(self)


class PropertyVariable(EntityVariable):
    """Property variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Property]]  # pyright: ignore

    @overload
    def __call__(self, v1: VTEntity, v2: VTValue) -> StatementTemplate:
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> ValueSnakTemplate:
        ...                     # pragma: no cover

    def __call__(
            self,
            v1: VTEntity | VTValue,
            v2: VTValue | None = None
    ) -> StatementTemplate | ValueSnakTemplate:
        if v2 is not None:
            from ..snak import ValueSnak
            from ..statement import StatementTemplate
            return StatementTemplate(v1, ValueSnak(self, v2))  # type: ignore
        else:
            from ..snak import ValueSnakTemplate
            return ValueSnakTemplate(self, v1)

    def no_value(self) -> NoValueSnakTemplate:
        """Constructs a no-value snak template from property variable.

        Returns:
           No-value snak template.
        """
        from ..snak import NoValueSnakTemplate
        return NoValueSnakTemplate(self)

    def some_value(self) -> SomeValueSnakTemplate:
        """Constructs a some-value snak template from property variable.

        Returns:
           Some-value snak template.
        """
        from ..snak import SomeValueSnakTemplate
        return SomeValueSnakTemplate(self)


class PropertyDatatype(Datatype):
    """Property datatype."""

    value_class: ClassVar[type[Property]]  # pyright: ignore


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

    datatype_class: ClassVar[type[PropertyDatatype]]  # pyright: ignore
    datatype: ClassVar[PropertyDatatype]              # pyright: ignore
    template_class: ClassVar[type[PropertyTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[PropertyVariable]]  # pyright: ignore

    def __init__(
            self,
            iri: VTPropertyContent,
            range: VTDatatype | None = None
    ) -> None:
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
    def __call__(self, v1: VTEntity, v2: VTValue) -> Statement:
        ...                     # pragma: no cover

    @overload
    def __call__(self, v1: VTValue) -> ValueSnak:
        ...                     # pragma: no cover

    def __call__(
            self,
            v1: VTEntity | VTValue,
            v2: VTValue | None = None
    ) -> Statement | ValueSnak:
        if v2 is not None:
            from ..snak import ValueSnak
            from ..statement import Statement
            return Statement(v1, ValueSnak(self, v2))  # type: ignore
        else:
            from ..snak import ValueSnak
            return ValueSnak(self, v1)

    @property
    def range(self) -> Datatype | None:
        """The range of property."""
        return self.get_range()

    def get_range(self, default: Datatype | None = None) -> Datatype | None:
        """Gets the range of property.

        If range is ``None``, returns `default`.

        Parameters:
           default: Default range.

        Returns:
           Datatype.
        """
        return self.get(1, default)

    def no_value(self) -> NoValueSnak:
        """Constructs a no-value snak from property.

        Returns:
           No-value snak.
        """
        from ..snak import NoValueSnak
        return NoValueSnak(self)

    def some_value(self) -> SomeValueSnak:
        """Constructs a some-value snak from property.

        Returns:
           Some-value snak.
        """
        from ..snak import SomeValueSnak
        return SomeValueSnak(self)


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
    from ... import itertools
    return map(Property, itertools.chain((iri,), iris))


class PseudoPropertyVariable(PropertyVariable):
    """Base class for pseudo-property variables."""

    object_class: ClassVar[type[PseudoProperty]]  # pyright: ignore


class PseudoProperty(
        Property,
        variable_class=PseudoPropertyVariable,
):
    """Base class for pseudo-properties."""


class LabelProperty(PseudoProperty):
    """The "label" pseudo-property."""

    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import RDFS
        super().__init__(RDFS.label, TextDatatype())


class AliasProperty(PseudoProperty):
    """The "alias" pseudo-property."""

    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import SKOS
        super().__init__(SKOS.altLabel, TextDatatype())


class DescriptionProperty(PseudoProperty):
    """The "description" pseudo-property."""

    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import SCHEMA
        super().__init__(SCHEMA.description, TextDatatype())


class LemmaProperty(PseudoProperty):
    """The "lemma" pseudo-property."""

    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import WIKIBASE
        super().__init__(WIKIBASE.lemma, TextDatatype())


class LexicalCategoryProperty(PseudoProperty):
    """The "lexical category" pseudo-property."""

    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import WIKIBASE
        super().__init__(WIKIBASE.lexicalCategory, ItemDatatype())


class LanguageProperty(PseudoProperty):
    """The "language" pseudo-property."""
    def __init__(
            self,
            iri: VTPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        from ...namespace import DCT
        super().__init__(DCT.language, ItemDatatype())
