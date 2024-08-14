# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses

from ...context import Section
from ...typing import Any, ClassVar, Optional, override, TypeAlias, Union
from ..template import Template
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

TText: TypeAlias = Union['Text', TString]
VText: TypeAlias = Union['TextTemplate', 'TextVariable', 'Text']
VTTextContent: TypeAlias = Union[Variable, TText]


@dataclasses.dataclass
class TextOptions(Section, name='text'):
    """Text options."""

    _default_language: str

    def __init__(self, **kwargs):
        self.default_language = kwargs.get(
            '_default_language',
            self.getenv('KIF_MODEL_VALUE_TEXT_DEFAULT_LANGUAGE', 'en'))

    @property
    def default_language(self) -> str:
        """The default language tag."""
        return self._default_language

    @default_language.setter
    def default_language(self, language: TString):
        self._default_language = String.check(
            language, 'default_language', 'language', 1).content


class TextTemplate(ShallowDataValueTemplate):
    """Text template.

    Parameters:
       content: Text content or string variable.
       language: Language tag or string variable.
    """

    object_class: ClassVar[type['Text']]  # pyright: ignore

    def __init__(
            self,
            content: VTTextContent,
            language: Optional[VTStringContent] = None
    ):
        super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # content
            if isinstance(arg, (Template, Variable)):
                return StringVariable.check(arg, type(self), None, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        elif i == 2:            # language
            if isinstance(arg, (Template, Variable)):
                return StringVariable.check(arg, type(self), None, i)
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

    object_class: ClassVar[type['Text']]  # pyright: ignore


class TextDatatype(Datatype):
    """Text datatype."""

    value_class: ClassVar[type['Text']]  # pyright: ignore


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

    datatype_class: ClassVar[type[TextDatatype]]  # pyright: ignore
    datatype: ClassVar[TextDatatype]              # pyright: ignore
    template_class: ClassVar[type[TextTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[TextVariable]]  # pyright: ignore

    def __init__(
            self,
            content: VTTextContent,
            language: Optional[VTStringContent] = None
    ):
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
                return self_.context.options.default_language
            else:
                return String.check(arg, type(self_), None, i).content
        else:
            raise self_._should_not_get_here()

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
