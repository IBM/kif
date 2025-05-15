# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ...context import Section
from ...typing import (
    Any,
    ClassVar,
    Iterable,
    Location,
    override,
    TypeAlias,
    Union,
)
from ..term import OpenTerm, Variable
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

TText: TypeAlias = Union['Text', TString]
VText: TypeAlias = Union['TextTemplate', 'TextVariable', 'Text']
VTTextContent: TypeAlias = Union[Variable, TText]

TTextSet: TypeAlias = Iterable[TText]

TTextLanguage: TypeAlias = TString
VTextLanguageContent: TypeAlias = VStringContent
VTTextLanguageContent: TypeAlias = VTStringContent


@dataclasses.dataclass
class TextOptions(Section, name='text'):
    """Text options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_language(kwargs)

    # -- language --

    #: The default value for the language option.
    DEFAULT_LANGUAGE: ClassVar[str] = 'en'

    _v_language: ClassVar[tuple[Iterable[str], str]] =\
        (('KIF_MODEL_VALUE_TEXT_LANGUAGE', 'KIF_LANGUAGE'),
         DEFAULT_LANGUAGE)

    _language: str

    def _init_language(self, kwargs: dict[str, Any]) -> None:
        self.language = kwargs.get(
            '_language', self.getenv_str(*self._v_language))

    @property
    def language(self) -> str:
        """The default language."""
        return self.get_language()

    @language.setter
    def language(self, language: TTextLanguage) -> None:
        self.set_language(language)

    def get_language(self) -> str:
        """Gets the default language.

        Returns:
           Language.
        """
        return self._language

    def set_language(
            self,
            language: TTextLanguage,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the default language.

        Parameters:
           language: Language.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._language = self._check_str(language, function, name, position)


class TextTemplate(ShallowDataValueTemplate):
    """Text template.

    Parameters:
       content: Text content or string variable.
       language: Language or string variable.
    """

    object_class: ClassVar[type[Text]]  # pyright: ignore

    def __init__(
            self,
            content: VTTextContent,
            language: VTTextLanguageContent | None = None
    ) -> None:
        super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, OpenTerm):
                return StringVariable.check(arg, type(self), None, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        elif i == 2:            # language
            if isinstance(arg, OpenTerm):
                return StringVariable.check(arg, type(self), None, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def language(self) -> VTextLanguageContent:
        """The language of text template."""
        return self.get_language()

    def get_language(self) -> VTextLanguageContent:
        """Gets the language of text template.

        Returns:
           Language or string variable.
        """
        return self.args[1]


class TextVariable(ShallowDataValueVariable):
    """Text variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Text]]  # pyright: ignore


class TextDatatype(Datatype):
    """Text datatype."""

    instance: ClassVar[TextDatatype]  # pyright: ignore
    value_class: ClassVar[type[Text]]  # pyright: ignore


class Text(
        ShallowDataValue,
        datatype_class=TextDatatype,
        template_class=TextTemplate,
        variable_class=TextVariable
):
    """Monolingual text.

    Parameters:
       content: Text content.
       language: Language.
    """

    datatype_class: ClassVar[type[TextDatatype]]  # pyright: ignore
    datatype: ClassVar[TextDatatype]              # pyright: ignore
    template_class: ClassVar[type[TextTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[TextVariable]]  # pyright: ignore

    def __init__(
            self,
            content: VTTextContent,
            language: VTTextContent | None = None
    ) -> None:
        if language is None and isinstance(content, Text):
            super().__init__(content.content, content.language)
        else:
            super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, Text):
                return arg.content
            else:
                return String.check(arg, type(self_), None, i).content
        elif i == 2:            # language
            if arg is None:
                return self_.context.options.language
            else:
                return String.check(arg, type(self_), None, i).content
        else:
            raise self_._should_not_get_here()

    @property
    def language(self) -> str:
        """The language of text."""
        return self.get_language()

    def get_language(self) -> str:
        """Gets the language of text.

        Returns:
           Language.
        """
        return self.args[1]
