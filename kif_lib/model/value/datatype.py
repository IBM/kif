# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from functools import cache

from ...rdflib import URIRef
from ...typing import NoReturn, Optional, TypeAlias, Union
from ..kif_object import KIF_Object, KIF_ObjectClass, TCallable

DatatypeClass: TypeAlias = type['Datatype']
TDatatypeClass: TypeAlias = Union[DatatypeClass, KIF_ObjectClass]


class Datatype(KIF_Object):
    """Abstract base class for datatypes.

    Parameters:
       datatype_class: Datatype class.
    """

    #: Value class associated with this datatype class.
    value_class: KIF_ObjectClass

    def __new__(
            cls,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        datatype_cls = cls._check_optional_arg_datatype_class(
            datatype_class, cls, cls, 'datatype_class', 1)
        assert datatype_cls is not None
        return super().__new__(datatype_cls)

    @classmethod
    def _check_arg_datatype_class(
            cls,
            arg: TDatatypeClass,
            function: Optional[Union[TCallable, str]] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> Union[DatatypeClass, NoReturn]:
        if isinstance(arg, type) and issubclass(arg, cls):
            return arg
        else:
            arg = cls._check_arg_kif_object_class(
                arg, function, name, position)
            return getattr(cls._check_arg(
                arg, hasattr(arg, 'datatype_class'),
                f'no datatype class for {arg.__qualname__}',
                function, name, position), 'datatype_class')

    _uri: URIRef

    @classmethod
    @cache
    def _from_rdflib(cls, uri: URIRef) -> 'Datatype':
        if uri == cls._ItemDatatype._uri:
            return cls._ItemDatatype()
        elif uri == cls._PropertyDatatype._uri:
            return cls._PropertyDatatype()
        elif uri == cls._LexemeDatatype._uri:
            return cls._LexemeDatatype()
        elif uri == cls._IRI_Datatype._uri:
            return cls._IRI_Datatype()
        elif uri == cls._TextDatatype._uri:
            return cls._TextDatatype()
        elif uri == cls._StringDatatype._uri:
            return cls._StringDatatype()
        elif uri == cls._ExternalIdDatatype._uri:
            return cls._ExternalIdDatatype()
        elif uri == cls._QuantityDatatype._uri:
            return cls._QuantityDatatype()
        elif uri == cls._TimeDatatype._uri:
            return cls._TimeDatatype()
        else:
            raise ValueError(f'bad Wikibase datatype: {uri}')

    @classmethod
    def _to_rdflib(cls) -> URIRef:
        return cls._uri

    def __init__(
            self,
            datatype_class: Optional[TDatatypeClass] = None
    ):
        if self.__class__ == Datatype:
            self._check_arg_not_none(
                datatype_class, self.__class__, 'datatype_class', 1)
            assert datatype_class is not None
            self._check_arg(
                datatype_class, datatype_class is not Datatype,
                f'expected proper subclass of {self.__class__.__qualname__}',
                self.__class__, 'datatype_class', 1)
        super().__init__()
