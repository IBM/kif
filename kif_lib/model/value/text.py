# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...rdflib import URIRef
from ...typing import (
    ClassVar,
    Final,
    NoReturn,
    Optional,
    override,
    TypeAlias,
    Union,
)
from ..kif_object import TCallable
from ..variable import Variable
from .shallow_data_value import (
    ShallowDataValue,
    ShallowDataValueTemplate,
    ShallowDataValueVariable,
)
from .string import (
    String,
    StringVariable,
    TString,
    VStringContent,
    VTStringContent,
)
from .value import Datatype

TextClass: TypeAlias = type['Text']
TextDatatypeClass: TypeAlias = type['TextDatatype']
TextTemplateClass: TypeAlias = type['TextTemplate']
TextVariableClass: TypeAlias = type['TextVariable']

TText: TypeAlias = Union['Text', TString]
VTTextContent: TypeAlias = Union[StringVariable, TText]
VText: TypeAlias = Union['TextTemplate', 'TextVariable', 'Text']


class TextTemplate(ShallowDataValueTemplate):
    """Text template.

    Parameters:
       content: Text content or string variable.
       language: Language tag or string variable.
    """

    object_class: ClassVar[TextClass]

    def __init__(
            self,
            content: VTTextContent,
            language: Optional[VTStringContent] = None
    ):
        super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(
                    arg, i, self.__class__)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        elif i == 2:            # language
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(
                    arg, i, self.__class__)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def language(self) -> VStringContent:
        """The language tag of text template."""
        return self.get_language()

    def get_language(self) -> VStringContent:
        """Gets the language tag of text template.

        Returns:
           Language tag or string variable.
        """
        return self.args[1]


class TextVariable(ShallowDataValueVariable):
    """Text variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[TextClass]


class TextDatatype(Datatype):
    """Text datatype."""

    value_class: ClassVar[TextClass]

    _uri: ClassVar[URIRef] = NS.WIKIBASE.Monolingualtext


class Text(
        ShallowDataValue,
        datatype_class=TextDatatype,
        template_class=TextTemplate,
        variable_class=TextVariable
):
    """Monolingual text.

    Parameters:
       content: Text content.
       language: Language tag.
    """

    datatype_class: ClassVar[TextDatatypeClass]
    datatype: ClassVar[TextDatatype]
    template_class: ClassVar[TextTemplateClass]
    variable_class: ClassVar[TextVariableClass]

    #: Default language tag.
    default_language: Final[str] = 'en'

    @classmethod
    def _check_arg_text(
            cls,
            arg: TText,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Text', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, str), function, name, position))

    def __init__(
            self,
            content: VTTextContent,
            language: Optional[VTStringContent] = None
    ):
        if isinstance(content, Text) and language is None:
            language = content.language
        super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_str(
                arg.args[0] if isinstance(arg, (String, Text)) else arg, i)
        elif i == 2:            # language
            return self._preprocess_optional_arg_str(
                arg.args[0] if isinstance(arg, String) else arg, i,
                Text.default_language)
        else:
            raise self._should_not_get_here()

    @property
    def language(self) -> str:
        """The language tag of text."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets the language tag of text.

        Returns:
           Language tag.
        """
        return self.args[1]
