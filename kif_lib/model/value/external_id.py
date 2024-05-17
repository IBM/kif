# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...rdflib import Literal, URIRef
from ...typing import (
    cast,
    Collection,
    NoReturn,
    Optional,
    override,
    TypeAlias,
    Union,
)
from ..kif_object import TCallable
from .string import (
    String,
    StringDatatype,
    StringTemplate,
    StringVariable,
    TString,
)
from .value import Value

ExternalIdClass: TypeAlias = type['ExternalId']
ExternalIdDatatypeClass: TypeAlias = type['ExternalIdDatatype']
ExternalIdTemplateClass: TypeAlias = type['ExternalIdTemplate']
ExternalIdVariableClass: TypeAlias = type['ExternalIdVariable']

TExternalId: TypeAlias = Union['ExternalId', TString]
VTExternalIdContent: TypeAlias = Union['StringVariable', TExternalId]
VExternalId: TypeAlias =\
    Union['ExternalIdTemplate', 'ExternalIdVariable', 'ExternalId']


class ExternalIdTemplate(StringTemplate):
    """External id template.

    Parameters:
       content: External id content or string variable.
    """

    object_class: ExternalIdClass

    def __init__(self, content: VTExternalIdContent):
        super().__init__(content)


class ExternalIdVariable(StringVariable):
    """External id variable.

    Parameters:
       name: Name.
    """

    object_class: ExternalIdClass


class ExternalIdDatatype(StringDatatype):
    """External id datatype."""

    value_class: ExternalIdClass

    _uri: URIRef = NS.WIKIBASE.ExternalId


class ExternalId(
        String,
        datatype_class=ExternalIdDatatype,
        template_class=ExternalIdTemplate,
        variable_class=ExternalIdVariable
):
    """External id.

    Parameters:
       content: External id content.
    """

    datatype_class: ExternalIdDatatypeClass
    datatype: ExternalIdDatatype
    template_class: ExternalIdTemplateClass
    variable_class: ExternalIdVariableClass

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

    def __init__(self, content: VTExternalIdContent):
        super().__init__(content)

    @override
    def _preprocess_arg(self, arg, i):
        if i == 1:              # content
            return self._preprocess_arg_str(
                arg.args[0] if isinstance(arg, (ExternalId, String))
                else arg, i)
        else:
            raise self._should_not_get_here()
