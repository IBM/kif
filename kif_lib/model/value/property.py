# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
from typing import TYPE_CHECKING

from typing_extensions import overload

from ...typing import (
    Any,
    cast,
    ClassVar,
    Iterable,
    Location,
    Mapping,
    override,
    Self,
    Set,
    TypeAlias,
    TypedDict,
    Union,
)
from ..term import OpenTerm, Variable
from .datatype import (
    Datatype,
    DatatypeVariable,
    TDatatype,
    VDatatype,
    VTDatatype,
)
from .entity import Entity, EntityTemplate, EntityVariable, VTEntity
from .iri import IRI, IRI_Template, T_IRI, VT_IRI
from .string import TString
from .text import Text, TText, TTextLanguage, TTextSet
from .value import VTValue

if TYPE_CHECKING:               # pragma: no cover
    from ...store import Store
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

    class Schema(TypedDict):
        """Property schema."""

        p: IRI
        pq: IRI
        pqv: IRI
        pr: IRI
        prv: IRI
        ps: IRI
        psv: IRI
        wdno: IRI
        wdt: IRI

    class _TSchema(TypedDict):
        """Property schema (coercion type)."""

        p: T_IRI
        pq: T_IRI
        pqv: T_IRI
        pr: T_IRI
        prv: T_IRI
        ps: T_IRI
        psv: T_IRI
        wdno: T_IRI
        wdt: T_IRI

    TSchema: TypeAlias = Union[Schema, _TSchema]

    @classmethod
    def _check_schema(
            cls,
            schema: Property.TSchema,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Property.Schema:
        schema = cls._check_arg_isinstance(
            schema, Mapping, function, name, position)
        f = functools.partial(
            IRI.check, function=function, name=name, position=position)
        try:
            return {
                'p': f(schema['p']),
                'pq': f(schema['pq']),
                'pqv': f(schema['pqv']),
                'pr': f(schema['pr']),
                'prv': f(schema['prv']),
                'ps': f(schema['ps']),
                'psv': f(schema['psv']),
                'wdno': f(schema['wdno']),
                'wdt': f(schema['wdt']),
            }
        except KeyError as err:
            raise cls._arg_error(
                f'property schema misses key {err}',
                function, name, position) from err

    @classmethod
    def _check_optional_schema(
            cls,
            schema: Property.TSchema | None,
            default: Property.Schema | None = None,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Property.Schema | None:
        if schema is None:
            schema = default
        if schema is None:
            return schema
        else:
            return cls._check_schema(schema, function, name, position)

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

    @classmethod
    def descriptor_to_snaks(
            cls,
            descriptor: Descriptor,
    ) -> Iterable[ValueSnak]:
        """Converts property descriptor to (value) snaks.

        Parameters:
           descriptor: Property descriptor.

        Returns:
           (Value) snaks.
        """
        if 'labels' in descriptor:
            from .pseudo_property import LabelProperty
            for label in descriptor['labels'].values():
                yield LabelProperty()(label)
        if 'aliases' in descriptor:
            from .pseudo_property import AliasProperty
            for aliases in descriptor['aliases'].values():
                yield from map(AliasProperty(), aliases)
        if 'description' in descriptor:
            from .pseudo_property import DescriptionProperty
            for description in descriptor['descriptions'].values():
                yield DescriptionProperty()(description)

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

    @override
    def display(self, language: TString | None = None) -> str:
        label = self.get_label(language)
        if label:
            return label.content
        else:
            return super().display(language)  # fallback

    def describe(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Property.Descriptor | None:
        """Gets the descriptor of property in KIF context.

        If `language` is given, resolves only text in `language`.
        Otherwise, resolves text in all languages.

        If `resolve` is ``True``, resolves property data.

        If `resolver` is given, uses it to resolve property data.
        Otherwise, uses the resolver registered in context (if any).

        If `force` is given, forces resolution.

        Parameters:
           language: Language.
           resolve: Whether to resolve descriptor.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Property descriptor or ``None``.
        """
        return self.context.describe(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.describe)

    @property
    def label(self) -> Text | None:
        """The label of property in KIF context."""
        return self.get_label()

    def get_label(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Text | None:
        """Gets the label of property in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve label.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Label or ``None``.
        """
        return self.context.get_label(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_label)

    @property
    def aliases(self) -> Set[Text] | None:
        """The aliases of property in KIF context."""
        return self.get_aliases()

    def get_aliases(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Set[Text] | None:
        """Gets the aliases of property in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve aliases.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Aliases or ``None``.
        """
        return self.context.get_aliases(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_aliases)

    @property
    def description(self) -> Text | None:
        """The description of property in KIF context."""
        return self.get_description()

    def get_description(
            self,
            language: TTextLanguage | None = None,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Text | None:
        """Gets the description of property in KIF context.

        Parameters:
           language: Language.
           resolve: Whether to resolve description.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Description or ``None``.
        """
        return self.context.get_description(
            self, language=language, resolve=resolve, resolver=resolver,
            force=force, function=self.get_description)

    @property
    def registered_range(self) -> Datatype | None:
        """The range of property in KIF context."""
        return self.get_registered_range()

    def get_registered_range(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Datatype | None:
        """Gets the range of property in KIF context.

        Parameters:
           resolve: Whether to resolve range.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Range or ``None``.
        """
        return self.context.get_range(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.get_range)

    @property
    def inverse(self) -> Property | None:
        """The inverse of property in KIF context."""
        return self.get_inverse()

    def get_inverse(
            self,
            resolve: bool | None = None,
            resolver: Store | None = None,
            force: bool | None = None
    ) -> Property | None:
        """Gets the inverse of property in KIF context.

        Parameters:
           resolve: Whether to resolve inverse.
           resolver: Resolver store.
           force: Whether to force resolution.

        Returns:
           Property or ``None``.
        """
        return self.context.get_inverse(
            self, resolve=resolve, resolver=resolver,
            force=force, function=self.get_inverse)

    @property
    def schema(self) -> Property.Schema | None:
        """The schema of property in KIF context."""
        return self.get_schema()

    def get_schema(self) -> Property.Schema | None:
        """Gets the schema of property in KIF context.

        Returns:
           Property schema or ``None``.
        """
        return self.context.get_schema(self, function=self.get_schema)

    def register(
            self,
            label: TText | None = None,
            labels: TTextSet | None = None,
            alias: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None,
            descriptions: TTextSet | None = None,
            range: TDatatype | None = None,
            inverse: TProperty | None = None
    ) -> Self:
        """Adds or updates property data in KIF context.

        Parameters:
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           range: Range.
           inverse: Inverse property.

        Returns:
           Property.
        """
        return cast(Self, self.context.entities.register(
            self, label=label, labels=labels, alias=alias, aliases=aliases,
            description=description, descriptions=descriptions,
            range=range, inverse=inverse, function=self.register))

    def unregister(
            self,
            label: TText | None = None,
            labels: TTextSet | None = None,
            alias: TText | None = None,
            aliases: TTextSet | None = None,
            description: TText | None = None,
            descriptions: TTextSet | None = None,
            label_language: TTextLanguage | None = None,
            alias_language: TTextLanguage | None = None,
            description_language: TTextLanguage | None = None,
            all_labels: bool = False,
            all_aliases: bool = False,
            all_descriptions: bool = False,
            range: bool = False,
            inverse: bool = False
    ) -> bool:
        """Removes property data from KIF context.

        If called with no arguments, removes all property data.

        Parameters:
           label: Label.
           labels: Labels.
           alias: Alias.
           aliases: Aliases.
           description: Description.
           descriptions: Descriptions.
           label_language: Language.
           alias_language: Language.
           description_language: Language.
           all_labels: Whether to remove all labels.
           all_aliases: Whether to remove all aliases.
           all_descriptions: Whether to remove all descriptions.
           range: Whether to remove range.
           inverse: Whether to remove inverse.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        if (label is None and labels is None
                and alias is None and aliases is None
                and description is None and descriptions is None
                and label_language is None
                and alias_language is None
                and description_language is None
                and all_labels is False
                and all_aliases is False
                and all_descriptions is False
                and range is False
                and inverse is False):
            return self.context.entities.unregister(
                self, all=True, function=self.unregister)
        else:
            return self.context.entities.unregister(
                self, label=label, labels=labels,
                alias=alias, aliases=aliases,
                description=description, descriptions=descriptions,
                label_language=label_language, alias_language=alias_language,
                description_language=description_language,
                all_labels=all_labels, all_aliases=all_aliases,
                all_descriptions=all_descriptions,
                range=range, inverse=inverse, function=self.unregister)


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
