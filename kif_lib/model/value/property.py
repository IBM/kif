# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import overload

from ...typing import (
    Any,
    ClassVar,
    Iterable,
    Mapping,
    override,
    Set,
    TypeAlias,
    TypedDict,
    Union,
)
from ..term import OpenTerm, Variable
from .datatype import Datatype, DatatypeVariable, VDatatype, VTDatatype
from .entity import Entity, EntityTemplate, EntityVariable, VTEntity
from .iri import IRI_Template, T_IRI, VT_IRI
from .string import TString
from .text import Text
from .value import VTValue

if TYPE_CHECKING:               # pragma: no cover
    from ..rank import VTRank
    from ..set import VTQualifierRecord, VTReferenceRecordSet
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
    def __call__(
            self,
            arg1: VTEntity,
            arg2: VTValue,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs statement template from property template.

        Parameters:
           arg1: Subject.
           arg2: Value.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def __call__(self, arg1: VTValue) -> ValueSnakTemplate:
        """Constructs value snak template from property template.

        Parameters:
           arg1: Value.

        Returns:
           Value snak template.
        """
        ...                     # pragma: no cover

    def __call__(
            self,
            arg1: VTEntity | VTValue,
            arg2: VTValue | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | ValueSnakTemplate:
        if arg2 is not None:
            from ..snak import ValueSnak
            from ..statement import StatementTemplate
            stmt = StatementTemplate(
                arg1, ValueSnak(self, arg2))  # type: ignore
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)
        else:
            from ..snak import ValueSnakTemplate
            return ValueSnakTemplate(self, arg1)

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

    @overload
    def no_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs no-value statement template from property template.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def no_value(self) -> NoValueSnakTemplate:
        """Constructs no-value snak template from property template.

        Returns:
           No-value snak template.
        """
        ...                     # pragma: no cover

    def no_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | NoValueSnakTemplate:
        from ..snak import NoValueSnakTemplate
        snak = NoValueSnakTemplate(self)
        if subject is None:
            return snak
        else:
            from ..statement import StatementTemplate
            stmt = StatementTemplate(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)

    @overload
    def some_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs some-value statement template from property template.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def some_value(self) -> SomeValueSnakTemplate:
        """Constructs some-value snak template from property template.

        Returns:
           Some-value snak template.
        """
        ...                     # pragma: no cover

    def some_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | SomeValueSnakTemplate:
        from ..snak import SomeValueSnakTemplate
        snak = SomeValueSnakTemplate(self)
        if subject is None:
            return snak
        else:
            from ..statement import StatementTemplate
            stmt = StatementTemplate(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)


class PropertyVariable(EntityVariable):
    """Property variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Property]]  # pyright: ignore

    @overload
    def __call__(
            self,
            arg1: VTEntity,
            arg2: VTValue,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs statement template from property variable.

        Parameters:
           arg1: Subject.
           arg2: Value.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def __call__(self, arg1: VTValue) -> ValueSnakTemplate:
        """Constructs value snak template from property variable.

        Parameters:
           arg1: Value.

        Returns:
           Value snak template.
        """
        ...                     # pragma: no cover

    def __call__(
            self,
            arg1: VTEntity | VTValue,
            arg2: VTValue | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | ValueSnakTemplate:
        if arg2 is not None:
            from ..snak import ValueSnak
            from ..statement import StatementTemplate
            stmt = StatementTemplate(
                arg1, ValueSnak(self, arg2))  # type: ignore
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)
        else:
            from ..snak import ValueSnakTemplate
            return ValueSnakTemplate(self, arg1)

    @overload
    def no_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs no-value statement template from property variable.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def no_value(self) -> NoValueSnakTemplate:
        """Constructs no-value snak template from property variable.

        Returns:
           No-value snak template.
        """
        ...                     # pragma: no cover

    def no_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | NoValueSnakTemplate:
        from ..snak import NoValueSnakTemplate
        snak = NoValueSnakTemplate(self)
        if subject is None:
            return snak
        else:
            from ..statement import StatementTemplate
            stmt = StatementTemplate(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)

    @overload
    def some_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate:
        """Constructs some-value statement template from property variable.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement template.
        """
        ...                     # pragma: no cover

    @overload
    def some_value(self) -> SomeValueSnakTemplate:
        """Constructs some-value snak template from property variable.

        Returns:
           Some-value snak template.
        """
        ...                     # pragma: no cover

    def some_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> StatementTemplate | SomeValueSnakTemplate:
        from ..snak import SomeValueSnakTemplate
        snak = SomeValueSnakTemplate(self)
        if subject is None:
            return snak
        else:
            from ..statement import StatementTemplate
            stmt = StatementTemplate(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)


class PropertyDatatype(Datatype):
    """Property datatype."""

    instance: ClassVar[PropertyDatatype]  # pyright: ignore
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

    class Descriptor(TypedDict, total=False):
        """Property descriptor."""

        #: Label indexed by language.
        labels: Mapping[str, Text]

        #: Aliases indexed by language.
        aliases: Mapping[str, Set[Text]]

        #: Description indexed by language.
        descriptions: Mapping[str, Text]

        #: Range datatype.
        range: Datatype

        #: Inverse property.
        inverse: Property

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
    def __call__(
            self,
            arg1: VTEntity,
            arg2: VTValue,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement:
        """Constructs statement from property.

        Parameters:
           arg1: Subject.
           arg2: Value.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement.
        """
        ...                     # pragma: no cover

    @overload
    def __call__(self, arg1: VTValue) -> ValueSnak:
        """Constructs value snak from property.

        Parameters:
           arg1: Value.

        Returns:
           Value snak.
        """
        ...                     # pragma: no cover

    def __call__(
            self,
            arg1: VTEntity | VTValue,
            arg2: VTValue | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement | ValueSnak:
        if arg2 is not None:
            from ..snak import ValueSnak
            from ..statement import Statement
            stmt = Statement(arg1, ValueSnak(self, arg2))  # type: ignore
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)
        else:
            from ..snak import ValueSnak
            return ValueSnak(self, arg1)

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

    @override
    def display(self, language: TString | None = None) -> str:
        label = self.context.entities.get_label(self, language, self.display)
        if label:
            return label.content
        else:
            return super().display(language)

    @property
    def label(self) -> Text | None:
        """The label of property in KIF context."""
        return self.get_label()

    def get_label(self, language: TString | None = None) -> Text | None:
        """Gets the label of property in KIF context.

        Parameters:
           language: Language.

        Returns:
           Label or ``None`` (no label for property in KIF context).
        """
        return self.context.entities.get_label(
            self, language, self.get_label)

    @overload
    def no_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement:
        """Constructs no-value statement from property.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement.
        """
        ...                     # pragma: no cover

    @overload
    def no_value(self) -> NoValueSnak:
        """Constructs no-value snak from property.

        Returns:
           No-value snak.
        """
        ...                     # pragma: no cover

    def no_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement | NoValueSnak:
        from ..snak import NoValueSnak
        snak = NoValueSnak(self)
        if subject is None:
            return snak
        else:
            from ..statement import Statement
            stmt = Statement(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)

    @overload
    def some_value(
            self,
            subject: VTEntity,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement:
        """Constructs some-value statement from property.

        Parameters:
           subject: Entity.
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.

        Returns:
           Statement.
        """
        ...                     # pragma: no cover

    @overload
    def some_value(self) -> SomeValueSnak:
        """Constructs some-value snak from property.

        Returns:
           Some-value snak.
        """
        ...                     # pragma: no cover

    def some_value(
            self,
            subject: VTEntity | None = None,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> Statement | SomeValueSnak:
        from ..snak import SomeValueSnak
        snak = SomeValueSnak(self)
        if subject is None:
            return snak
        else:
            from ..statement import Statement
            stmt = Statement(subject, snak)
            if qualifiers is None and references is None and rank is None:
                return stmt
            else:
                return stmt.annotate(qualifiers, references, rank)


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
