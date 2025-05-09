# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import functools
import re

from ... import itertools, rdflib
from ...compiler.sparql import SPARQL_Mapping
from ...model import Filter, IRI, T_IRI, TGraph
from ...typing import (
    Any,
    BinaryIO,
    ClassVar,
    Iterable,
    Iterator,
    Location,
    override,
    TextIO,
    TypeAlias,
    Union,
)
from ..abc import Store
from ..mixer import MixerStore
from .rdf import RDF_Store
from .sparql_core import _SPARQL_Store


class SPARQL_Store(
        MixerStore,
        store_name='sparql',
        store_description='SPARQL store'
):
    """SPARQL store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       format: Input source format (file extension or media type).
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       rdflib_graph: RDFLib graph to be used as input source.
       skolemize: Whether to skolemize the resulting graph.
       mapping: SPARQL mapping.
       kwargs: Other keyword arguments.
    """

    @dataclasses.dataclass
    class _Options(MixerStore.Options):

        _v_best_ranked: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_SPARQL_STORE_BEST_RANKED',), None)

        _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_SPARQL_STORE_DISTINCT',), None)

        _v_distinct: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_SPARQL_STORE_DISTINCT',), None)

        _v_max_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_SPARQL_STORE_MAX_LIMIT',), None)

        _v_limit: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_SPARQL_STORE_LIMIT',), None)

        _v_lookahead: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_SPARQL_STORE_LOOKAHEAD',), None)

        _v_max_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_SPARQL_STORE_MAX_PAGE_SIZE',), None)

        _v_page_size: ClassVar[tuple[Iterable[str], int | None]] =\
            (('KIF_SPARQL_STORE_PAGE_SIZE',), None)

        _v_max_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_SPARQL_STORE_MAX_TIMEOUT',), None)

        _v_timeout: ClassVar[tuple[Iterable[str], float | None]] =\
            (('KIF_SPARQL_STORE_TIMEOUT',), None)

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            self._init_skolemize(kwargs)

        # -- skolemize --

        #: Default value for the skolemize option.
        DEFAULT_SKOLEMIZE: ClassVar[bool] = True

        _v_skolemize: ClassVar[tuple[Iterable[str], bool | None]] =\
            (('KIF_SPARQL_STORE_SKOLEMIZE',), DEFAULT_SKOLEMIZE)

        _skolemize: bool | None

        def _init_skolemize(self, kwargs: dict[str, Any]) -> None:
            self.skolemize = kwargs.get(
                '_skolemize', self.getenv_optional_bool(*self._v_skolemize))

        @property
        def skolemize(self) -> bool:
            """The skolemize flag."""
            return self.get_skolemize()

        @skolemize.setter
        def skolemize(self, skolemize: bool) -> None:
            self.set_skolemize(skolemize)

        def get_skolemize(self) -> bool:
            """Gets the skolemize flag.

            Returns:
               Skolemize flag.
            """
            assert self._skolemize is not None
            return self._skolemize

        def set_skolemize(
                self,
                skolemize: bool,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            """Sets the skolemize flag.

            Parameters:
               skolemize: Skolemize flag.
               function: Function or function name.
               name: Argument name.
               position: Argument position.
            """
            self._skolemize = bool(skolemize)

    @dataclasses.dataclass
    class Options(_Options, name='sparql'):
        """SPARQL store options."""

        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)

        @override
        def _get_parent_callback(self) -> MixerStore.Options:
            return self.get_context().options.store.mixer

        @override
        def _init_sync_flags(self, kwargs: dict[str, Any]) -> None:
            self.set_sync_flags(kwargs.get('_sync_flags'))

        @override
        def get_skolemize(self) -> bool:
            return self._do_get('_skolemize', super().get_skolemize)

        @override
        def set_skolemize(
                self,
                skolemize: bool | None,
                function: Location | None = None,
                name: str | None = None,
                position: int | None = None
        ) -> None:
            self._do_set(skolemize, '_skolemize', functools.partial(
                super().set_skolemize,
                function=function, name=name, position=position))

    #: Type alias for SPARQL Store arguments.
    Args: TypeAlias = Union[T_IRI, RDF_Store.Args]

    @classmethod
    def _is_http_or_https_iri(
            cls,
            arg: Args,
            _re: re.Pattern = re.compile(r'^http[s]?://')
    ) -> bool:
        content: str
        if isinstance(arg, IRI):
            content = arg.content
        elif isinstance(arg, rdflib.URIRef):
            content = str(arg)
        elif isinstance(arg, str):
            content = arg
        else:
            return False
        return bool(_re.match(content))

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        other, iris = map(list, itertools.partition(
            self._is_http_or_https_iri, args))

        def it() -> Iterator[Store]:
            for iri in iris:
                yield Store('sparql-httpx', iri, mapping=mapping, **kwargs)
            if (other
                    or location is not None
                    or file is not None
                    or data is not None
                    or graph is not None
                    or rdflib_graph is not None):
                yield Store(
                    'rdf', *other, format=format,
                    location=location, file=file, data=data, graph=graph,
                    rdflib_graph=rdflib_graph, skolemize=skolemize,
                    mapping=mapping, **kwargs)
        super().__init__(store_name, list(it()), **kwargs)

    @property
    def default_options(self) -> Options:
        return super().default_options  # type: ignore

    @override
    def get_default_options(self) -> Options:
        return self.context.options.store.sparql

    @property
    def options(self) -> Options:
        return super().options  # type: ignore

    def _update_options(self, **kwargs: Any) -> None:
        super()._update_options(**kwargs)
        if 'skolemize' in kwargs:
            self.set_skolemize(kwargs['skolemize'])

    @property
    def default_skolemize(self) -> bool:
        """The default value for :attr:`SPARQL_Store.skolemize`."""
        return self.get_default_skolemize()

    def get_default_skolemize(self) -> bool:
        """Gets the default value for :attr:`SPARQL_Store.skolemize`.

        Returns:
           Default skolemize flag.
        """
        return self.default_options.skolemize

    @property
    def skolemize(self) -> bool:
        """The skolemize flag of mixer."""
        return self.get_skolemize()

    @skolemize.setter
    def skolemize(self, skolemize: bool | None = None) -> None:
        self.set_skolemize(skolemize)

    def get_skolemize(self) -> bool:
        """Gets the skolemize flag of mixer.

        Returns:
           skolemize flag.
        """
        return self.options.skolemize

    def set_skolemize(self, skolemize: bool | None = None) -> None:
        """Sets the skolemize flag of mixer.

        If `skolemize` is ``None``, resets it to the default.

        Parameters:
           skolemize: skolemize flag.
        """
        self._set_option_with_hooks(
            skolemize,
            self.options.get_skolemize,
            functools.partial(
                self.options.set_skolemize,
                function=self.set_skolemize,
                name='skolemize',
                position=1),
            self._set_skolemize)

    def _set_skolemize(self, skolemize: bool) -> bool:
        return True


class DBpediaSPARQL_Store(
        SPARQL_Store,
        store_name='dbpedia-sparql',
        store_description='DBpedia SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with DBpedia mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.db.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._dbpedia_mapping_constructor()
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class PubChemSPARQL_Store(
        SPARQL_Store,
        store_name='pubchem-sparql',
        store_description='PubChem SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with PubChem mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            normalize_casrn: bool | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.pc.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._pubchem_mapping_constructor(
                normalize_casrn=normalize_casrn)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WikidataSPARQL_Store(
        SPARQL_Store,
        store_name='wikidata-sparql',
        store_description='Wikidata SPARQL store'
):
    """Alias for :class:`SPARQL_Store` with Wikidata mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            blazegraph: bool | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if not args:
            resolver_iri = self.context.options.vocabulary.wd.resolver
            if resolver_iri is not None:
                args = (resolver_iri,)
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=blazegraph,
                strict=strict,
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)


class WDQS_Store(
        WikidataSPARQL_Store,
        store_name='wdqs',
        store_description='Wikidata query service store'
):
    """Alias for :class:`WikidataSPARQL_Store` with stricter mappings."""

    def __init__(
            self,
            store_name: str,
            *args: SPARQL_Store.Args,
            format: str | None = None,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            rdflib_graph: rdflib.Graph | None = None,
            skolemize: bool | None = None,
            mapping: SPARQL_Mapping | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        if mapping is None:
            mapping = _SPARQL_Store._wikidata_mapping_constructor(
                blazegraph=True,  # force
                strict=True,      # force
                truthy=truthy)
        super().__init__(
            store_name, *args, format=format,
            location=location, file=file, data=data, graph=graph,
            rdflib_graph=rdflib_graph, skolemize=skolemize,
            mapping=mapping, **kwargs)
