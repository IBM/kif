# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from ...namespace import DCT, RDFS, SCHEMA, SKOS, WIKIBASE
from ...typing import Any, cast, ClassVar, Location, override, Self, TypeAlias
from .datatype import Datatype, VTDatatype
from .iri import IRI
from .item import ItemDatatype
from .property import Property, VTPropertyContent
from .string import String
from .text import TextDatatype

VTPseudoPropertyContent: TypeAlias = VTPropertyContent


class PseudoProperty(Property):
    """Base class for pseudo-properties."""

    #: The expected IRI for the pseudo-property.
    expected_iri: ClassVar[IRI]

    #: The expected range for the pseudo-property.
    expected_range: ClassVar[Datatype]

    @classmethod
    def _check_arg_iri_details(cls, arg: IRI) -> str:
        return f'expected {cls.expected_iri}, got {arg}'

    @classmethod
    def _check_arg_range_details(cls, arg: IRI) -> str:
        return f'expected {cls.expected_range}, got {arg}'

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if cls is PseudoProperty:
            if isinstance(arg, cls):
                return cast(Self, arg)
            elif isinstance(arg, (IRI, String, str)):
                iri = IRI.check(arg, function, name, position)
                for sub in cls._get_proper_subclasses():
                    if sub.expected_iri == iri:
                        return cast(Self, sub(
                            sub.expected_iri, sub.expected_range))
            raise cls._check_error(arg, function, name, position)
        else:
            try:
                return super().check(arg)
            except (TypeError, ValueError) as err:
                raise cls._check_error(arg, function, name, position) from err

    @abc.abstractmethod
    def __init__(
            self,
            iri: VTPseudoPropertyContent | None,
            range: VTDatatype | None
    ):
        super().__init__(
            iri or self.expected_iri,
            range or self.expected_range)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        arg = super()._preprocess_arg(arg, i)
        if i == 1:
            return self._check_optional_arg(
                arg, None, arg == self.expected_iri,
                self._check_arg_iri_details,
                type(self), None, 1)
        elif i == 2:
            return self._check_optional_arg(
                arg, None, arg == self.expected_range,
                self._check_arg_range_details,
                type(self), None, 2)
        else:
            raise self._should_not_get_here()


class LabelProperty(PseudoProperty):
    """The "label" pseudo-property."""

    expected_iri = IRI(RDFS.label)
    expected_range = TextDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)


class AliasProperty(PseudoProperty):
    """The "alias" pseudo-property."""

    expected_iri = IRI(SKOS.altLabel)
    expected_range = TextDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)


class DescriptionProperty(PseudoProperty):
    """The "description" pseudo-property."""

    expected_iri = IRI(SCHEMA.description)
    expected_range = TextDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)


class LemmaProperty(PseudoProperty):
    """The "lemma" pseudo-property."""

    expected_iri = IRI(WIKIBASE.lemma)
    expected_range = TextDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)


class LexicalCategoryProperty(PseudoProperty):
    """The "lexical category" pseudo-property."""

    expected_iri = IRI(WIKIBASE.lexicalCategory)
    expected_range = ItemDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)


class LanguageProperty(PseudoProperty):
    """The "language" pseudo-property."""

    expected_iri = IRI(DCT.language)
    expected_range = ItemDatatype()

    def __init__(
            self,
            iri: VTPseudoPropertyContent | None = None,
            range: VTDatatype | None = None
    ) -> None:
        super().__init__(iri, range)
