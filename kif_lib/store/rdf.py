# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import json
import logging
from pathlib import PurePath

from .. import rdflib
from ..model import KIF_Object
from ..typing import Any, BinaryIO, cast, IO, Optional, override, TextIO, Union
from .sparql import SPARQL_Store
from .sparql_results import SPARQL_Results

LOG = logging.getLogger(__name__)


class RDF_Store(SPARQL_Store, store_name='rdf', store_description='RDF file'):
    """RDF store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources, files, paths, or strings.
       publicID: Logical URI to use as the document base.
       format: Input source format (file extension or media type).
       location: Relative or absolute URL of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: RDFLib graph to use.
       skolemize: Whether to skolemize the resulting graph.
    """

    __slots__ = (
        '_graph',
    )

    _graph: rdflib.Graph

    def __init__(
            self,
            store_name: str,
            *args: Optional[Union[IO[bytes], TextIO, rdflib.InputSource,
                                  str, bytes, PurePath]],
            publicID: Optional[str] = None,
            format: Optional[str] = None,
            location: Optional[str] = None,
            file: Optional[Union[BinaryIO, TextIO]] = None,
            data: Optional[Union[str, bytes]] = None,
            graph: Optional[rdflib.Graph] = None,
            skolemize: bool = True,
            **kwargs: Any
    ):
        super().__init__(store_name, 'file:///dev/null', **kwargs)
        graph = KIF_Object._check_optional_arg_isinstance(
            graph, rdflib.Graph, rdflib.Graph(),
            self.__class__, 'graph', None)
        assert graph is not None
        load = functools.partial(
            graph.parse, format=format, publicID=publicID)
        try:
            if location is not None:
                load(location=location)
            if file is not None:
                load(file=file)
            if data is not None:
                load(data=data)
            for src in args:
                load(src)
        except Exception as err:
            raise self._error(str(err)) from err
        if skolemize:
            self._graph = graph.skolemize()
        else:
            self._graph = graph

    @override
    def _eval_select_query_string(
            self,
            text: str,
            fake_results: bool = False,
            headers: Optional[dict[str, Any]] = None,
            **kwargs
    ) -> SPARQL_Results:
        LOG.debug('%s()\n%s', self._eval_query_string.__qualname__, text)
        res = self._graph.query(self._prepare_query_string(text))
        data = cast(bytes, res.serialize(format='json'))
        assert data is not None
        if not fake_results:
            return SPARQL_Results(json.loads(data))
        else:
            ###
            # FIXME: Fake results.
            ###
            return cast(SPARQL_Results, json.loads(data))
