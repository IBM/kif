# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from abc import abstractmethod
from enum import auto, Enum, Flag
from functools import cache

from .. import namespace as NS
from ..itertools import chain
from ..rdflib import Literal, URIRef
from ..typing import (
    cast,
    Collection,
    Final,
    Iterable,
    NoReturn,
    Optional,
    override,
    TypeAlias,
    Union,
)
from .kif_object import (
    Datetime,
    Decimal,
    KIF_Object,
    TCallable,
    TDatetime,
    TDecimal,
)
from .pattern import Template, Variable

# -- Value --

TValue: TypeAlias = Union['Value', NS.T_URI, TDatetime, TDecimal, str]

VValue: TypeAlias = Union['ValueTemplate', 'ValueVariable', TValue]

# -- Entity --

VEntity: TypeAlias = Union['EntityTemplate', 'EntityVariable', 'Entity']

# -- Item --

TItem: TypeAlias = Union['Item', 'T_IRI']

VItemContent: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'TItem']

VItem: TypeAlias = Union['ItemTemplate', 'ItemVariable', 'Item']

# -- Property --

TProperty: TypeAlias = Union['Property', 'T_IRI']

VPropertyContent: TypeAlias =\
    Union['IRI_Template', 'IRI_Variable', 'TProperty']

VProperty: TypeAlias =\
    Union['PropertyTemplate', 'PropertyVariable', TProperty]

# -- Lexeme --

TLexeme: TypeAlias = Union['Lexeme', 'T_IRI']

VLexemeContent: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'TLexeme']

VLexeme: TypeAlias = Union['LexemeTemplate', 'LexemeVariable', 'Lexeme']

# -- IRI --

T_IRI: TypeAlias = Union['IRI', 'String', NS.T_URI]

V_IRI_Content: TypeAlias = Union['StringVariable', T_IRI]

V_IRI: TypeAlias = Union['IRI_Template', 'IRI_Variable', 'IRI']

# -- Text --

TText: TypeAlias = Union['Text', 'TString']

VTextContent: TypeAlias = Union['StringVariable', TText]

VText: TypeAlias = Union['TextTemplate', 'TextVariable', TText]

# -- String --

TString: TypeAlias = Union['String', str]

VStringContent: TypeAlias = Union['StringVariable', TString]

VString: TypeAlias = Union['StringTemplate', 'StringVariable', TString]

# -- External id --

TExternalId: TypeAlias = Union['ExternalId', TString]

VExternalIdContent: TypeAlias = Union['StringVariable', TExternalId]

VExternalId: TypeAlias =\
    Union['ExternalIdTemplate', 'ExternalIdVariable', TExternalId]

# -- Quantity --

TQuantity: TypeAlias = Union['Quantity', TDecimal]

VQuantityContent: TypeAlias = Union['QuantityVariable', TQuantity]

VQuantity: TypeAlias =\
    Union['QuantityTemplate', 'QuantityVariable', TQuantity]

# -- Time --

TTime: TypeAlias = Union['Time', TDatetime]

VTimeContent: TypeAlias = Union['TimeVariable', TTime]

VTime: TypeAlias = Union['TimeTemplate', 'TimeVariable', TTime]

TTimePrecision: TypeAlias = Union['Time.Precision', TQuantity]

VTimePrecisionContent: TypeAlias = Union['QuantityVariable', TTimePrecision]

TTimeTimezone: TypeAlias = TQuantity

VTimeTimezoneContent: TypeAlias = VQuantityContent

# -- Datatype --

TDatatype = Union['Datatype', T_IRI]


# == Value =================================================================

class ValueTemplate(Template):
    """Abstract base class for value templates."""


class ValueVariable(Variable):
    """Value variable.

    Parameters:
       name: String.
    """


class Value(KIF_Object):
    """Abstract base class for values."""

    #: Concrete template class associated with this value class (if any).
    template_class: type[Template]

    #: Variable class associated with this value class.
    variable_class: type[Variable] = ValueVariable

    class Mask(Flag):
        """Mask for concrete value classes."""

        #: Mask for :class:`Item`.
        ITEM = auto()

        #: Mask for :class:`Property`.
        PROPERTY = auto()

        #: Mask for :class:`Lexeme`.
        LEXEME = auto()

        #: Mask for :class:`IRI`.
        IRI = auto()

        #: Mask for :class:`Text`.
        TEXT = auto()

        #: Mask for :class:`String`.
        STRING = auto()

        #: Mask for :class:`ExternalId`.
        EXTERNAL_ID = auto()

        #: Mask for :class:`Quantity`.
        QUANTITY = auto()

        #: Mask for :class:`Time`.
        TIME = auto()

        #: Mask for :class:`Entity`.
        ENTITY = ITEM | PROPERTY | LEXEME

        #: Mask for :class:`ShallowDataValue`.
        SHALLOW_DATA_VALUE = IRI | TEXT | STRING | EXTERNAL_ID

        #: Mask for :class:`DeepDataValue`.
        DEEP_DATA_VALUE = TIME | QUANTITY

        #: Mask for :class:`DataValue`.
        DATA_VALUE = SHALLOW_DATA_VALUE | DEEP_DATA_VALUE

        #: Mask for all value classes.
        ALL = ENTITY | SHALLOW_DATA_VALUE | DEEP_DATA_VALUE

    #: Mask for :class:`Item`.
    ITEM: Final[Mask] = Mask.ITEM

    #: Mask for :class:`Property`.
    PROPERTY: Final[Mask] = Mask.PROPERTY

    #: Mask for :class:`Lexeme`.
    LEXEME: Final[Mask] = Mask.LEXEME

    #: Mask for :class:`IRI`.
    IRI: Final[Mask] = Mask.IRI

    #: Mask for :class:`Text`.
    TEXT: Final[Mask] = Mask.TEXT

    #: Mask for :class:`String`.
    STRING: Final[Mask] = Mask.STRING

    #: Mask for :class:`ExternalId`.
    EXTERNAL_ID: Final[Mask] = Mask.EXTERNAL_ID

    #: Mask for :class:`Quantity`.
    QUANTITY: Final[Mask] = Mask.QUANTITY

    #: Mask for :class:`Time`.
    TIME: Final[Mask] = Mask.TIME

    #: Mask for :class:`Entity`.
    ENTITY: Final[Mask] = Mask.ENTITY

    #: Mask for :class:`ShallowDataValue`.
    SHALLOW_DATA_VALUE: Final[Mask] = Mask.SHALLOW_DATA_VALUE

    #: Mask for :class:`DeepDataValue`.
    DEEP_DATA_VALUE: Final[Mask] = Mask.DEEP_DATA_VALUE

    #: Mask for :class:`DataValue`.
    DATA_VALUE: Final[Mask] = Mask.DATA_VALUE

    #: Mask for all value classes.
    ALL: Final[Mask] = Mask.ALL

    TMask = Union[Mask, int]

    @classmethod
    def _check_arg_value_mask(
            cls,
            arg: TMask,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Mask, NoReturn]:
        return cls.Mask(cls._check_arg_isinstance(
            arg, (cls.Mask, int), function, name, position))

    @classmethod
    def _check_optional_arg_value_mask(
            cls,
            arg: Optional[TMask],
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_value_mask(arg, function, name, position)

    @classmethod
    def _preprocess_arg_value_mask(
            cls,
            arg: TMask,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Mask, NoReturn]:
        return cls._check_arg_value_mask(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_value_mask(
            cls,
            arg,
            i: int,
            default: Optional[Mask] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[Mask], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._preprocess_arg_value_mask(arg, i, function)

    #: Mask of this value class.
    mask: Mask = Mask.ALL

    @classmethod
    def get_mask(cls) -> Mask:
        """Gets the mask of this value class.

        Returns:
           Mask.
        """
        return cls.mask

    @classmethod
    def _check_arg_value(
            cls,
            arg: TValue,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Value', NoReturn]:
        arg = cls._check_arg_isinstance(
            arg, (cls, URIRef, Datetime, float, int, str),
            function, name, position)
        if isinstance(arg, URIRef):
            return IRI(arg)
        elif isinstance(arg, Datetime):
            return Time(arg)
        elif isinstance(arg, (float, int)):
            return Quantity(arg)
        elif isinstance(arg, str):
            return String(arg)
        else:
            assert isinstance(arg, Value)
            return arg

    @property
    def value(self) -> str:
        """The simple value of value."""
        return self.get_value()

    @abstractmethod
    def get_value(self) -> str:
        """Gets the simple value of value.

        Returns:
           Simple value.
        """
        raise self._must_be_implemented_in_subclass()

    def n3(self) -> str:
        """Gets the simple value of value in N3 format.

        Returns:
           Simple value in N3 format.
        """
        node = self._to_rdflib()
        if isinstance(node, Literal):
            return cast(Literal, node).n3()
        elif isinstance(node, URIRef):
            return cast(URIRef, node).n3()
        else:
            raise self._should_not_get_here()

    @classmethod
    def _from_rdflib(
            cls,
            node: Union[Literal, URIRef],
            item_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_item_prefixes,
            property_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_property_prefixes,
            lexeme_prefixes: Collection[
                NS.T_NS] = NS.Wikidata.default_lexeme_prefixes
    ) -> 'Value':
        from ..rdflib import _NUMERIC_LITERAL_TYPES
        cls._check_arg_isinstance(
            node, (Literal, URIRef), cls._from_rdflib, 'node', 1)
        res: Value
        if isinstance(node, URIRef):
            uri = cast(URIRef, node)
            if NS.Wikidata.is_wd_item(uri, item_prefixes):
                if item_prefixes == NS.Wikidata.default_item_prefixes:
                    res = Item(uri)
                else:
                    res = Item(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_property(uri, property_prefixes):
                if property_prefixes == NS.Wikidata.default_property_prefixes:
                    res = Property(uri)
                else:
                    res = Property(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            elif NS.Wikidata.is_wd_lexeme(uri, lexeme_prefixes):
                if lexeme_prefixes == NS.Wikidata.default_lexeme_prefixes:
                    res = Lexeme(uri)
                else:
                    res = Lexeme(NS.WD[NS.Wikidata.get_wikidata_name(uri)])
            else:
                res = IRI(uri)
        elif isinstance(node, Literal):
            literal = cast(Literal, node)
            if literal.datatype in _NUMERIC_LITERAL_TYPES:
                res = Quantity(str(literal))
            elif (literal.datatype == NS.XSD.dateTime
                  or literal.datatype == NS.XSD.date):
                res = Time(str(literal))
            elif literal.datatype is None and literal.language:
                res = Text(str(literal), literal.language)
            else:
                res = String(str(literal))
        else:
            raise cls._should_not_get_here()
        return cast(Value, cls.check(res))

    def _to_rdflib(self) -> Union[Literal, URIRef]:
        if self.is_entity() or self.is_iri():
            return URIRef(self.value)
        elif self.is_quantity():
            return Literal(self.value, datatype=NS.XSD.decimal)
        elif self.is_time():
            return Literal(self.value, datatype=NS.XSD.dateTime)
        elif self.is_text():
            return Literal(self.value, cast(Text, self).language)
        elif self.is_string():
            return Literal(self.value)
        else:
            raise self._should_not_get_here()


# == Entity ================================================================

class EntityTemplate(ValueTemplate):
    """Abstract base class for entity templates."""

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # iri
            if Template.test(arg):
                return self._preprocess_arg_iri_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_iri_variable(arg, i)
            else:
                return Entity._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def iri(self) -> V_IRI:
        return self.get_iri()

    def get_iri(self) -> V_IRI:
        return self.args[0]


class EntityVariable(ValueVariable):
    """Entity variable.

    Parameters:
       name: String.
    """


class Entity(Value):
    """Abstract base class for entities."""

    variable_class: type[Variable] = EntityVariable

    mask: Value.Mask = Value.ENTITY

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # iri
            return self._preprocess_arg_iri(
                arg.args[0] if isinstance(arg, Entity) else arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return self.args[0].value

    @property
    def iri(self) -> 'IRI':
        """The iri of entity."""
        return self.get_iri()

    def get_iri(self) -> 'IRI':
        """Gets the iri of entity.

        Returns:
           IRI.
        """
        return self.args[0]


# -- Item ------------------------------------------------------------------

class ItemTemplate(EntityTemplate):
    """Item template.

    Parameters:
        iri: IRI.
    """

    def __init__(self, iri: VItemContent):
        super().__init__(iri)


class ItemVariable(EntityVariable):
    """Item variable.

    Parameters:
        name: String.
    """


class Item(Entity):
    """Person or thing.

    Parameters:
       iri: IRI.
    """

    template_class: type[Template] = ItemTemplate

    variable_class: type[Variable] = ItemVariable

    mask: Value.Mask = Value.ITEM

    @classmethod
    def _check_arg_item(
            cls,
            arg: TItem,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Item', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, IRI, URIRef, String, str), function, name, position))

    def __init__(self, iri: VItemContent):
        super().__init__(iri)


def Items(iri: VItemContent, *iris: VItemContent) -> Iterable[Item]:
    """Constructs one or more items.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting items.
    """
    return map(Item, chain([iri], iris))


# -- Property --------------------------------------------------------------

class PropertyTemplate(EntityTemplate):
    """Property template.

    Parameters:
       iri: IRI.
    """

    def __init__(self, iri: VPropertyContent):
        super().__init__(iri)


class PropertyVariable(EntityVariable):
    """Property variable.

    Parameters:
        name: String.
    """


class Property(Entity):
    """Binary relationship.

    Parameters:
       iri: IRI.
    """

    template_class: type[Template] = PropertyTemplate

    variable_class: type[Variable] = PropertyVariable

    mask: Value.Mask = Value.PROPERTY

    @classmethod
    def _check_arg_property(
            cls,
            arg: TProperty,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Property', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, IRI, URIRef, String, str), function, name, position))

    def __init__(self, iri: VPropertyContent):
        super().__init__(iri)

    def __call__(self, value1, value2=None):
        if value2 is not None:
            return self._Statement(value1, self._ValueSnak(self, value2))
        else:
            return self._ValueSnak(self, value1)


def Properties(
        iri: VPropertyContent,
        *iris: VPropertyContent
) -> Iterable[Property]:
    """Constructs one or more properties.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting properties.
    """
    return map(Property, chain([iri], iris))


# -- Lexeme ----------------------------------------------------------------

class LexemeTemplate(EntityTemplate):
    """Lexeme template.

    Parameters:
       iri: IRI.
    """

    def __init__(self, iri: VLexemeContent):
        super().__init__(iri)


class LexemeVariable(EntityVariable):
    """Lexeme variable.

    Parameters:
        name: String.
    """


class Lexeme(Entity):
    """Word or phrase.

    Parameters:
       iri: IRI.
    """

    template_class: type[Template] = LexemeTemplate

    variable_class: type[Variable] = LexemeVariable

    mask: Value.Mask = Value.LEXEME

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

    def __init__(self, iri: VLexemeContent):
        super().__init__(iri)


def Lexemes(iri: VLexemeContent, *iris: VLexemeContent) -> Iterable[Lexeme]:
    """Constructs one or more lexemes.

    Parameters:
       iri: IRI.
       iris: Remaining IRIs.

    Returns:
       The resulting lexemes.
    """
    return map(Lexeme, chain([iri], iris))


# == Data value ============================================================

class DataValueTemplate(ValueTemplate):
    """Abstract base class for data value templates."""


class DataValueVariable(ValueVariable):
    """Data value variable.

    Parameters:
       name: String.
    """


class DataValue(Value):
    """Abstract base class for data values."""

    variable_class: type[Variable] = DataValueVariable

    mask: Value.Mask = Value.DATA_VALUE


# == Shallow data value ====================================================

class ShallowDataValueTemplate(DataValueTemplate):
    """Abstract base class for shallow data value templates."""

    @property
    def content(self) -> str:
        return self.get_content()

    def get_content(self) -> str:
        return self.args[0]


class ShallowDataValueVariable(DataValueVariable):
    """Shallow data value variable.

    Parameters:
       name: String.
    """


class ShallowDataValue(DataValue):
    """Abstract base class for shallow data values."""

    variable_class: type[Variable] = ShallowDataValueVariable

    mask: Value.Mask = Value.SHALLOW_DATA_VALUE

    def get_value(self) -> str:
        return self.args[0]

    @property
    def content(self) -> str:
        """The content of shallow data value."""
        return self.get_content()

    def get_content(self) -> str:
        """Gets the content of shallow data value.

        Returns:
           Content.
        """
        return self.args[0]


# -- IRI -------------------------------------------------------------------

class IRI_Template(ShallowDataValueTemplate):
    """IRI template.

    Parameters:
       content: IRI content.
    """

    def __init__(self, content: V_IRI_Content):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return IRI._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class IRI_Variable(ShallowDataValueVariable):
    """IRI variable.

    Parameters:
        name: String.
    """


class IRI(ShallowDataValue):
    """IRI.

    Parameters:
       content: IRI content.
    """

    template_class: type[Template] = IRI_Template

    variable_class: type[Variable] = IRI_Variable

    mask: Value.Mask = Value.IRI

    @classmethod
    def _check_arg_iri(
            cls,
            arg: T_IRI,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['IRI', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, URIRef, String, str), function, name, position))

    def __init__(self, content: V_IRI_Content):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # content
            if isinstance(arg, (IRI, String)):
                arg = arg.args[0]
            elif isinstance(arg, URIRef):
                arg = str(arg)
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


# -- Text ------------------------------------------------------------------

class TextTemplate(ShallowDataValueTemplate):
    """Text template.

    Parameters:
       content: Text content.
       language: Language tag.
    """

    def __init__(
            self,
            content: VTextContent,
            language: Optional[VStringContent] = None
    ):
        super().__init__(content, language)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        elif i == 2:            # language
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return Text._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class TextVariable(ShallowDataValueVariable):
    """Text variable.

    Parameters:
        name: String.
    """


class Text(ShallowDataValue):
    """Monolingual text.

    Parameters:
       content: Text content.
       language: Language tag.
    """

    template_class: type[Template] = TextTemplate

    variable_class: type[Variable] = TextVariable

    mask: Value.Mask = Value.TEXT

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
            content: VTextContent,
            language: Optional[VStringContent] = None
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


# -- String ----------------------------------------------------------------

class StringTemplate(ShallowDataValueTemplate):
    """Base class for string templates.

    Parameters:
       content: String content.
    """

    def __init__(self, content: VStringContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return String._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class StringVariable(ShallowDataValueVariable):
    """String variable.

    Parameters:
        name: String.
    """


class String(ShallowDataValue):
    """String.

    Parameters:
       content: String content.
    """

    template_class: type[Template] = StringTemplate

    variable_class: type[Variable] = StringVariable

    mask: Value.Mask = Value.STRING

    @classmethod
    def _check_arg_string(
            cls,
            arg: TString,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['String', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, str), function, name, position))

    def __init__(self, content: VStringContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_str(
                arg.args[0] if isinstance(arg, String) else arg, i)
        else:
            raise self._should_not_get_here()


# -- External id -----------------------------------------------------------

class ExternalIdTemplate(StringTemplate):
    """External id template.

    Parameters:
       content: External id content.
    """

    def __init__(self, content: VExternalIdContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            if Variable.test(arg):
                return self._preprocess_arg_string_variable(arg, i)
            else:
                return ExternalId._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class ExternalIdVariable(StringVariable):
    """External id variable.

    Parameters:
        name: String.
    """


class ExternalId(String):
    """External id.

    Parameters:
       content: External id content.
    """

    template_class: type[Template] = ExternalIdTemplate

    variable_class: type[Variable] = ExternalIdVariable

    mask: Value.Mask = Value.EXTERNAL_ID

    @classmethod
    def _check_arg_external_id(
            cls,
            arg: TExternalId,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['ExternalId', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, String, str), function, name, position))

    @classmethod
    @override
    def _from_rdflib(
            cls,
            node: Union[Literal, URIRef],
            item_prefixes: Collection[NS.T_NS]
            = NS.Wikidata.default_item_prefixes,
            property_prefixes: Collection[NS.T_NS]
            = NS.Wikidata.default_property_prefixes,
            lexeme_prefixes: Collection[NS.T_NS]
            = NS.Wikidata.default_lexeme_prefixes
    ) -> 'Value':
        res = Value._from_rdflib(
            node, item_prefixes, property_prefixes, lexeme_prefixes)
        if res.is_string():
            return cls(cast(String, res))
        else:
            return cast(Value, cls.check(res))

    def __init__(self, content: VExternalIdContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_str(
                arg.args[0] if isinstance(arg, (ExternalId, String))
                else arg, i)
        else:
            raise self._should_not_get_here()


# == Deep data value =======================================================

class DeepDataValueTemplate(DataValueTemplate):
    """Abstract base class for deep data value templates."""


class DeepDataValueVariable(DataValueVariable):
    """Deep data value variable.

    Parameters:
       name: String.
    """


class DeepDataValue(DataValue):
    """Abstract base class for deep data values."""

    variable_class: type[Variable] = DeepDataValueVariable

    mask: Value.Mask = Value.DEEP_DATA_VALUE


# -- Quantity --------------------------------------------------------------

class QuantityTemplate(DeepDataValueTemplate):
    """Quantity template.

    Parameters:
       amount: Amount.
       unit: Unit.
       lower_bound: Lower bound.
       upper_bound: Upper bound.
    """

    def __init__(
            self,
            amount: VQuantityContent,
            unit: Optional[VItem] = None,
            lower_bound: Optional[VQuantityContent] = None,
            upper_bound: Optional[VQuantityContent] = None):
        super().__init__(amount, unit, lower_bound, upper_bound)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # amount
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(arg, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 2:            # unit
            if Template.test(arg):
                return self._preprocess_arg_item_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_item_variable(arg, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 3:            # lower-bound
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(arg, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        elif i == 4:            # upper-bound
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(arg, i)
            else:
                return Quantity._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class QuantityVariable(DeepDataValueVariable):
    """Quantity variable.

    Parameters:
       name: String.
    """


class Quantity(DeepDataValue):
    """Quantity.

    Parameters:
       amount: Amount.
       unit: Unit.
       lower_bound: Lower bound.
       upper_bound: Upper bound.
    """

    template_class: type[Template] = QuantityTemplate

    variable_class: type[Variable] = QuantityVariable

    mask: Value.Mask = Value.QUANTITY

    @classmethod
    def _check_arg_quantity(
            cls,
            arg: TQuantity,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Quantity', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, Decimal, float, int, str), function, name, position))

    def __init__(
            self,
            amount: VQuantityContent,
            unit: Optional[VItem] = None,
            lower_bound: Optional[VQuantityContent] = None,
            upper_bound: Optional[VQuantityContent] = None):
        super().__init__(amount, unit, lower_bound, upper_bound)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # amount
            return self._preprocess_arg_decimal(
                arg.args[0] if isinstance(arg, Quantity) else arg, i)
        elif i == 2:            # unit
            return self._preprocess_optional_arg_item(arg, i)
        elif i == 3:            # lower-bound
            return self._preprocess_optional_arg_decimal(
                arg.args[0] if isinstance(arg, Quantity) else arg, i)
        elif i == 4:            # upper-bound
            return self._preprocess_optional_arg_decimal(
                arg.args[0] if isinstance(arg, Quantity) else arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return str(self.args[0])

    @property
    def amount(self) -> Decimal:
        """The amount of quantity."""
        return self.get_amount()

    def get_amount(self) -> Decimal:
        """Gets the amount of quantity.

        Returns:
           Amount.
        """
        return self.args[0]

    @property
    def unit(self) -> Optional[Item]:
        """The unit of quantity."""
        return self.get_unit()

    def get_unit(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets the unit of quantity.

        If the unit is ``None``, returns `default`.

        Parameters:
           default: Default unit.

        Returns:
           Unit.
        """
        unit = self.args[1]
        return unit if unit is not None else default

    @property
    def lower_bound(self) -> Optional[Decimal]:
        """The lower bound of quantity."""
        return self.get_lower_bound()

    def get_lower_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the lower bound of quantity.

        If the lower bound is ``None``, returns `default`.

        Parameters:
           default: Default lower bound.

        Returns:
           Lower bound.
        """
        lb = self.args[2]
        return lb if lb is not None else default

    @property
    def upper_bound(self) -> Optional[Decimal]:
        """The upper bound of quantity."""
        return self.get_upper_bound()

    def get_upper_bound(
            self,
            default: Optional[Decimal] = None
    ) -> Optional[Decimal]:
        """Gets the upper bound of quantity.

        If the upper bound is ``None``, returns `default`.

        Parameters:
           default: Default upper bound.

        Returns:
           Upper bound.
        """
        ub = self.args[3]
        return ub if ub is not None else default


# -- Time ------------------------------------------------------------------

class TimeTemplate(DeepDataValueTemplate):
    """Time template.

    Parameters:
       time: Time.
       precision: Precision.
       timezone: Time zone.
       calendar: Calendar model.
    """

    def __init__(
            self,
            time: VTimeContent,
            precision: Optional[VTimePrecisionContent] = None,
            timezone: Optional[VTimeTimezoneContent] = None,
            calendar: Optional[VItem] = None):
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # time
            if Variable.test(arg):
                return self._preprocess_arg_time_variable(arg, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 2:            # precision
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(arg, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 3:            # timezone
            if Variable.test(arg):
                return self._preprocess_arg_quantity_variable(arg, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        elif i == 4:            # calendar
            if Template.test(arg):
                return self._preprocess_arg_item_template(arg, i)
            elif Variable.test(arg):
                return self._preprocess_arg_item_variable(arg, i)
            else:
                return Time._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()


class TimeVariable(DeepDataValueVariable):
    """Time variable.

    Parameters:
       name: String.
    """


class Time(DeepDataValue):
    """Time.

    Parameters:
       time: Time.
       precision: Precision.
       timezone: Time zone.
       calendar: Calendar model.
    """

    template_class: type[Template] = TimeTemplate

    variable_class: type[Variable] = TimeVariable

    mask: Value.Mask = Value.TIME

    # See:
    # <https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Time>.
    # <https://www.mediawiki.org/wiki/Wikibase/DataModel#Dates_and_times>.

    class Precision(Enum):
        """Time precision."""

        #: Billion years.
        BILLION_YEARS = 0

        #: Hundred million years.
        HUNDRED_MILLION_YEARS = 1

        #: Ten million years.
        TEN_MILLION_YEARS = 2

        #: Million years.
        MILLION_YEARS = 3

        #: Hundred thousand years.
        HUNDRED_THOUSAND_YEARS = 4

        #: Ten thousand years.
        TEN_THOUSAND_YEARS = 5

        #: Millennia.
        MILLENNIA = 6

        #: Century.
        CENTURY = 7

        #: Decade.
        DECADE = 8

        #: Year.
        YEAR = 9

        #: Month.
        MONTH = 10

        #: Day.
        DAY = 11

        #: Hour.
        HOUR = 12

        #: Minute.
        MINUTE = 13

        #: Second.
        SECOND = 14

    #: Billion years.
    BILLION_YEARS = Precision.BILLION_YEARS

    #: Hundred million years.
    HUNDRED_MILLION_YEARS = Precision.HUNDRED_MILLION_YEARS

    #: Ten million years.
    TEN_MILLION_YEARS = Precision.TEN_MILLION_YEARS

    #: Million years.
    MILLION_YEARS = Precision.MILLION_YEARS

    #: Hundred thousand years.
    HUNDRED_THOUSAND_YEARS = Precision.HUNDRED_THOUSAND_YEARS

    #: Ten thousand years.
    TEN_THOUSAND_YEARS = Precision.TEN_THOUSAND_YEARS

    #: Millennia.
    MILLENNIA = Precision.MILLENNIA

    #: Century.
    CENTURY = Precision.CENTURY

    #: Decade.
    DECADE = Precision.DECADE

    #: Year
    YEAR = Precision.YEAR

    #: Month.
    MONTH = Precision.MONTH

    #: Day.
    DAY = Precision.DAY

    #: Hour.
    HOUR = Precision.HOUR

    #: Minute.
    MINUTE = Precision.MINUTE

    #: Second.
    SECOND = Precision.SECOND

    @classmethod
    def _check_arg_precision(
            cls,
            arg: TTimePrecision,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Time.Precision', NoReturn]:
        arg = cls._check_arg_isinstance(
            arg, (cls.Precision, Quantity, Decimal, float, int, str),
            function, name, position)
        try:
            if isinstance(arg, Quantity):
                arg = int(arg.args[0])
            if not isinstance(arg, (int, cls.Precision)):
                arg = int(arg)
            return cls.Precision(arg)
        except ValueError:
            raise cls._arg_error(
                f'expected {cls.Precision.__qualname__}',
                function, name, position, ValueError)

    @classmethod
    def _check_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            default: Optional['Time.Precision'] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional['Time.Precision'], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_precision(arg, function, name, position)

    @classmethod
    def _preprocess_arg_precision(
            cls,
            arg: TTimePrecision,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Time.Precision', NoReturn]:
        return cls._check_arg_precision(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_precision(
            cls,
            arg: Optional[TTimePrecision],
            i: int,
            default: Optional['Time.Precision'] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional['Time.Precision'], NoReturn]:
        return cls._check_optional_arg_precision(
            arg, default, function or cls, None, i)

    @classmethod
    def _check_arg_timezone(
            cls,
            arg: TTimeTimezone,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[int, NoReturn]:
        arg = cls._check_arg_isinstance(
            arg, (Quantity, Decimal, float, int, str),
            function, name, position)
        try:
            if isinstance(arg, Quantity):
                return int(arg.args[0])
            else:
                return int(arg)
        except ValueError:
            raise cls._arg_error(
                'expected timezone', function, name, position, ValueError)

    @classmethod
    def _check_optional_arg_timezone(
            cls,
            arg: Optional[TTimeTimezone],
            default: Optional[int] = None,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[Optional[int], NoReturn]:
        if arg is None:
            return default
        else:
            return cls._check_arg_timezone(arg, function, name, position)

    @classmethod
    def _preprocess_arg_timezone(
            cls,
            arg: TTimeTimezone,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[int, NoReturn]:
        return cls._check_arg_timezone(arg, function or cls, None, i)

    @classmethod
    def _preprocess_optional_arg_timezone(
            cls,
            arg: Optional[TTimeTimezone],
            i: int,
            default: Optional[int] = None,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union[Optional[int], NoReturn]:
        return cls._check_optional_arg_timezone(
            arg, default, function or cls, None, i)

    @classmethod
    def _check_arg_time(
            cls,
            arg: TTime,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union['Time', NoReturn]:
        return cls(cls._check_arg_isinstance(
            arg, (cls, Datetime, str), function, name, position))

    def __init__(
            self,
            time: VTimeContent,
            precision: Optional[VTimePrecisionContent] = None,
            timezone: Optional[VTimeTimezoneContent] = None,
            calendar: Optional[VItem] = None):
        super().__init__(time, precision, timezone, calendar)

    @override
    def _preprocess_arg(self, arg, i):
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self, arg, i):
        if i == 1:              # time
            return self._preprocess_arg_datetime(
                arg.args[0] if isinstance(arg, Time) else arg, i)
        elif i == 2:            # precision
            return Time._preprocess_optional_arg_precision(arg, i)
        elif i == 3:            # timezone
            return Time._preprocess_optional_arg_timezone(arg, i)
        elif i == 4:            # calendar
            return self._preprocess_optional_arg_item(arg, i)
        else:
            raise self._should_not_get_here()

    def get_value(self) -> str:
        return str(self.args[0].isoformat())

    @property
    def time(self) -> Datetime:
        """The date-time of time."""
        return self.get_time()

    def get_time(self) -> Datetime:
        """Gets the date-time of time.

        Returns:
           Datetime.
        """
        return self.args[0]

    @property
    def precision(self) -> Optional[Precision]:
        """The precision of time."""
        return self.get_precision()

    def get_precision(
            self,
            default: Optional['Time.Precision'] = None
    ) -> Optional[Precision]:
        """Gets the precision of time.

        If the precision is ``None``, returns `default`.

        Parameters:
           default: Default precision.

        Returns:
           Precision.
        """
        prec = self.args[1]
        return prec if prec is not None else default

    @property
    def timezone(self) -> Optional[int]:
        """The timezone of time."""
        return self.get_timezone()

    def get_timezone(
            self,
            default: Optional[int] = None
    ) -> Optional[int]:
        """Gets the timezone of time.

        If the timezone is ``None``, returns `default`.

        Parameters:
           default: Default timezone.

        Returns:
           Timezone.
        """
        tz = self.args[2]
        return tz if tz is not None else default

    @property
    def calendar(self) -> Optional[Item]:
        """The calendar model of time."""
        return self.get_calendar()

    def get_calendar(
            self,
            default: Optional[Item] = None
    ) -> Optional[Item]:
        """Gets calendar model of time.

        If the calendar model is ``None``, returns `default`.

        Parameters:
           default: Default calendar model.

        Returns:
           Calendar model.
        """
        cal = self.args[3]
        return cal if cal is not None else default


# == Datatype ==============================================================

class Datatype(KIF_Object):
    """Abstract base class for datatypes."""

    #: The datatype of :class:`Item`.
    item: 'ItemDatatype'

    #: The datatype of :class:`Property`.
    property: 'PropertyDatatype'

    #: The datatype of :class:`Lexeme`.
    lexeme: 'LexemeDatatype'

    #: The datatype of :class:`IRI`.
    iri: 'IRI_Datatype'

    #: The datatype of :class:`Text`.
    text: 'TextDatatype'

    #: The datatype of :class:`String`.
    string: 'StringDatatype'

    #: The datatype of :class:`ExternalId`.
    external_id: 'ExternalIdDatatype'

    #: The datatype of :class:`Quantity`.
    quantity: 'QuantityDatatype'

    #: The datatype of :class:`Time`.
    time: 'TimeDatatype'

    @classmethod
    def _preprocess_arg_datatype(
            cls,
            arg: TDatatype,
            i: int,
            function: Optional[Union[TCallable, str]] = None
    ) -> Union['Datatype', NoReturn]:
        if isinstance(arg, (IRI, URIRef, str)):
            if isinstance(arg, IRI):
                uri: URIRef = URIRef(arg.value)
            elif isinstance(arg, URIRef):
                uri = arg
            elif isinstance(arg, str):
                uri = URIRef(arg)
            else:
                raise cls._should_not_get_here()
            try:
                return cls._from_rdflib(uri)
            except ValueError as err:
                return cast(Datatype, cls._check_arg(
                    arg, False, str(err), function or cls,
                    None, i, ValueError))
        else:
            return cast(Datatype, Datatype.check(
                arg, function or cls, None, i))

    _uri: URIRef

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == cls.item._uri:
            return cls.item
        elif uri == cls.property._uri:
            return cls.property
        elif uri == cls.lexeme._uri:
            return cls.lexeme
        elif uri == cls.iri._uri:
            return cls.iri
        elif uri == cls.text._uri:
            return cls.text
        elif uri == cls.string._uri:
            return cls.string
        elif uri == cls.external_id._uri:
            return cls.external_id
        elif uri == cls.quantity._uri:
            return cls.quantity
        elif uri == cls.time._uri:
            return cls.time
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        return cls._uri

    @classmethod
    @cache
    def from_value_class(cls, value_class: type[Value]) -> 'Datatype':
        """Gets the datatype of `value_class`.

        Parameters:
           value_class: Value class.

        Returns:
           Datatype.
        """
        if value_class is Item:
            return cls.item
        elif value_class is Property:
            return cls.property
        elif value_class is Lexeme:
            return cls.lexeme
        elif value_class is IRI:
            return cls.iri
        elif value_class is Text:
            return cls.text
        elif value_class is String:
            return cls.string
        elif value_class is ExternalId:
            return cls.external_id
        elif value_class is Quantity:
            return cls.quantity
        elif value_class is Time:
            return cls.time
        else:
            cls._check_arg_issubclass(
                value_class, Value, cls.from_value_class, 'value_class', 2)
            raise cls._arg_error(
                f'no datatype for {value_class.__qualname__}',
                cls.from_value_class, 'value_class', 2)

    @classmethod
    @abstractmethod
    def to_value_class(cls) -> type[Value]:
        """Gets the value class of datatype.

        Returns:
           Value class.
        """
        raise cls._must_be_implemented_in_subclass()

    def __init__(self):
        return super().__init__()


class ItemDatatype(Datatype):
    """Datatype of :class:`Item`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseItem

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Item


class PropertyDatatype(Datatype):
    """Datatype of :class:`Property`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseProperty

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Property


class LexemeDatatype(Datatype):
    """Datatype of :class:`Lexeme`."""

    _uri: URIRef = NS.WIKIBASE.WikibaseLexeme

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Lexeme


class IRI_Datatype(Datatype):
    """Datatype of :class:`IRI`."""

    _uri: URIRef = NS.WIKIBASE.Url

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return IRI


class TextDatatype(Datatype):
    """Datatype of :class:`Text`."""

    _uri: URIRef = NS.WIKIBASE.Monolingualtext

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Text


class StringDatatype(Datatype):
    """Datatype of :class:`String`."""

    _uri: URIRef = NS.WIKIBASE.String

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return String


class ExternalIdDatatype(StringDatatype):
    """Datatype of :class:`ExternalId`."""

    _uri: URIRef = NS.WIKIBASE.ExternalId

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return ExternalId


class QuantityDatatype(Datatype):
    """Datatype of :class:`Quantity`."""

    _uri: URIRef = NS.WIKIBASE.Quantity

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Quantity


class TimeDatatype(Datatype):
    """Datatype of :class:`Time`."""

    _uri: URIRef = NS.WIKIBASE.Time

    @classmethod
    @override
    def to_value_class(cls) -> type[Value]:
        return Time


Datatype.item = ItemDatatype()
Datatype.property = PropertyDatatype()
Datatype.lexeme = LexemeDatatype()
Datatype.iri = IRI_Datatype()
Datatype.text = TextDatatype()
Datatype.string = StringDatatype()
Datatype.external_id = ExternalIdDatatype()
Datatype.quantity = QuantityDatatype()
Datatype.time = TimeDatatype()
