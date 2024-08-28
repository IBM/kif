# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import ClassVar, Iterable, TypeAlias, Union
from ..term import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .value import Datatype

TLexeme: TypeAlias = Union['Lexeme', T_IRI]
VLexeme: TypeAlias = Union['LexemeTemplate', 'LexemeVariable', 'Lexeme']
VTLexeme: TypeAlias = Union[Variable, VLexeme, TLexeme]
VTLexemeContent: TypeAlias = Union[Variable, IRI_Template, TLexeme]


class LexemeTemplate(EntityTemplate):
    """Lexeme template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[type[Lexeme]]  # pyright: ignore

    def __init__(self, iri: VTLexemeContent) -> None:
        super().__init__(iri)


class LexemeVariable(EntityVariable):
    """Lexeme variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Lexeme]]  # pyright: ignore


class LexemeDatatype(Datatype):
    """Lexeme datatype."""

    value_class: ClassVar[type[Lexeme]]  # pyright: ignore


class Lexeme(
        Entity,
        datatype_class=LexemeDatatype,
        template_class=LexemeTemplate,
        variable_class=LexemeVariable
):
    """Word or phrase.

    Parameters:
       iri: IRI.
    """

    datatype_class: ClassVar[type[LexemeDatatype]]  # pyright: ignore
    datatype: ClassVar[LexemeDatatype]              # pyright: ignore
    template_class: ClassVar[type[LexemeTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[LexemeVariable]]  # pyright: ignore

    def __init__(self, iri: VTLexemeContent) -> None:
        super().__init__(iri)


def Lexemes(iri: VTLexemeContent, *iris: VTLexemeContent) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting lexemes.
    """
    from ... import itertools
    return map(Lexeme, itertools.chain([iri], iris))
