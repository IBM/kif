from ..typing import Optional, TypeAlias, Union
from .kif_object import KIF_Object
from .value import IRI, Item, String, T_IRI, TString, Text, TText
from .variable import IRI_Variable, StringVariable, TextVariable, Variable

T_IRI_Content: TypeAlias = Union[StringVariable, T_IRI]
TEntityContent: TypeAlias = Union['IRI_Template', IRI_Variable, T_IRI]
TStringContent: TypeAlias = Union[StringVariable, TString]
TTextContent: TypeAlias = Union[StringVariable, TText]

TItemContent: TypeAlias = TEntityContent
TLexemeContent: TypeAlias = TEntityContent
TPropertyContent: TypeAlias = TEntityContent


class Template(KIF_Object):
    pass


# == Entity ================================================================

class EntityTemplate(Template):
    """Base class for entity templates."""

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, Template):
                return self._preprocess_arg_iri_template(arg, i)
            elif isinstance(arg, Variable):
                return self._preprocess_arg_iri_variable(arg, i)
            else:
                return Item._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class ItemTemplate(EntityTemplate):
    def __init__(self, iri: TItemContent):
        super().__init__(iri)


class PropertyTemplate(EntityTemplate):
    def __init__(self, iri: TPropertyContent):
        super().__init__(iri)


# == ShallowDataValue ======================================================

class IRI_Template(Template):

    def __init__(self, content: T_IRI_Content):
        super().__init__(content)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, Variable):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return IRI._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class TextTemplate(Template):

    def __init__(
            self,
            content: TTextContent,
            language: Optional[TStringContent] = None
    ):
        super().__init__(content, language)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, Variable):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        elif i == 2:
            if isinstance(arg, StringVariable):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class StringTemplate(Template):

    def __init__(self, content: TStringContent):
        super().__init__(content)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            if isinstance(arg, Variable):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return String._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()
