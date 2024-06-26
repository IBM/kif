# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...itertools import chain
from ...typing import ClassVar, Iterable, TypeAlias, Union
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI_Template, T_IRI
from .value import Datatype

LexemeClass: TypeAlias = type['Lexeme']
LexemeDatatypeClass: TypeAlias = type['LexemeDatatype']
LexemeTemplateClass: TypeAlias = type['LexemeTemplate']
LexemeVariableClass: TypeAlias = type['LexemeVariable']

TLexeme: TypeAlias = Union['Lexeme', T_IRI]
VLexeme: TypeAlias = Union['LexemeTemplate', 'LexemeVariable', 'Lexeme']
VTLexeme: TypeAlias = Union[Variable, VLexeme, TLexeme]
VTLexemeContent: TypeAlias = Union[IRI_Template, Variable, TLexeme]


class LexemeTemplate(EntityTemplate):
    """Lexeme template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[LexemeClass]  # pyright: ignore

    def __init__(self, iri: VTLexemeContent):
        super().__init__(iri)


class LexemeVariable(EntityVariable):
    """Lexeme variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[LexemeClass]  # pyright: ignore


class LexemeDatatype(Datatype):
    """Lexeme datatype."""

    value_class: ClassVar[LexemeClass]  # pyright: ignore


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

    datatype_class: ClassVar[LexemeDatatypeClass]  # pyright: ignore
    datatype: ClassVar[LexemeDatatype]             # pyright: ignore
    template_class: ClassVar[LexemeTemplateClass]  # pyright: ignore
    variable_class: ClassVar[LexemeVariableClass]  # pyright: ignore

    def __init__(self, iri: VTLexemeContent):
        super().__init__(iri)


def Lexemes(iri: VTLexemeContent, *iris: VTLexemeContent) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       iri: IRI.
       iris: IRIs.

    Returns:
       The resulting lexemes.
    """
    return map(Lexeme, chain([iri], iris))
