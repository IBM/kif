# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...itertools import chain
from ...rdflib import URIRef
from ...typing import (
    cast,
    ClassVar,
    Iterable,
    NoReturn,
    Optional,
    TypeAlias,
    Union,
)
from ..kif_object import TCallable
from ..variable import Variable
from .entity import Entity, EntityTemplate, EntityVariable
from .iri import IRI, IRI_Template, IRI_Variable, T_IRI
from .string import String
from .value import Datatype

LexemeClass: TypeAlias = type['Lexeme']
LexemeDatatypeClass: TypeAlias = type['LexemeDatatype']
LexemeTemplateClass: TypeAlias = type['LexemeTemplate']
LexemeVariableClass: TypeAlias = type['LexemeVariable']

TLexeme: TypeAlias = Union['Lexeme', T_IRI]
VTLexemeContent: TypeAlias = Union[IRI_Template, IRI_Variable, 'TLexeme']
VLexeme: TypeAlias = Union['LexemeTemplate', 'LexemeVariable', 'Lexeme']


class LexemeTemplate(EntityTemplate):
    """Lexeme template.

    Parameters:
       iri: IRI, IRI template, or IRI variable.
    """

    object_class: ClassVar[LexemeClass]

    def __init__(self, iri: VTLexemeContent):
        super().__init__(iri)


class LexemeVariable(EntityVariable):
    """Lexeme variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[LexemeClass]

    @classmethod
    def _preprocess_arg_lexeme_variable(
            cls,
            arg: Variable,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['LexemeVariable', NoReturn]:
        return cast(LexemeVariable, cls._preprocess_arg_variable(
            arg, i, function or cls))


class LexemeDatatype(Datatype):
    """Lexeme datatype."""

    value_class: ClassVar[LexemeClass]

    _uri: ClassVar[URIRef] = NS.WIKIBASE.WikibaseLexeme


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

    datatype_class: ClassVar[LexemeDatatypeClass]
    datatype: ClassVar[LexemeDatatype]
    template_class: ClassVar[LexemeTemplateClass]
    variable_class: ClassVar[LexemeVariableClass]

    @classmethod
    def _check_arg_lexeme(
            cls,
            arg: TLexeme,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Lexeme', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, IRI, URIRef, String, str), function, name, position))

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
