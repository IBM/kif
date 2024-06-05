# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import json
import logging
from pathlib import PurePath

from ..itertools import chain
from ..model import KIF_Object
from ..rdflib import Graph, InputSource, RDFLibError
from ..typing import Any, BinaryIO, cast, IO, Optional, override, TextIO, Union
from .sparql import SPARQL_Store
from .sparql_results import SPARQL_Results

LOG = logging.getLogger(__name__)


class RDF_Store(SPARQL_Store, store_name='rdf', store_description='RDF file'):
    """RDF store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       source: An input source, file, path, or string.
       args: More input sources, files, paths, or strings.
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

    _graph: Graph

    def __init__(
            self,
            store_name: str,
            source: Optional[Union[IO[bytes], TextIO, InputSource,
                                   str, bytes, PurePath]] = None,
            *args: Optional[Union[IO[bytes], TextIO, InputSource,
                                  str, bytes, PurePath]],
            publicID: Optional[str] = None,
            format: Optional[str] = None,
            location: Optional[str] = None,
            file: Optional[Union[BinaryIO, TextIO]] = None,
            data: Optional[Union[str, bytes]] = None,
            graph: Optional[Graph] = None,
            skolemize: bool = True,
            **kwargs: Any
    ):
        super().__init__(store_name, 'file:///dev/null', **kwargs)
        sources = [s for s in chain([source], args) if s is not None]
        input = {
            'source': sources,
            'location': location,
            'file': file,
            'data': data,
        }
        nonempty = list(filter(lambda t: bool(t[1]), input.items()))
        if len(nonempty) > 1:
            names = list(map(lambda t: t[0], nonempty))
            sep = ' and ' if len(names) == 2 else ', and '
            msg = ', '.join(names[:-1]) + sep + names[-1]
            raise KIF_Object._arg_error(
                f'{msg} are mutually exclusive', self.__class__, names[0])
        graph = KIF_Object._check_optional_arg_isinstance(
            graph, Graph, Graph(), self.__class__, 'graph', None)
        assert graph is not None
        try:
            if location or file or data:
                assert not sources
                graph.parse(
                    publicID=publicID, format=format,
                    location=location, file=file, data=data)
            else:
                assert not location and not file and not data
                for src in sources:
                    graph.parse(src, publicID=publicID, format=format)
        except RDFLibError as err:
            raise self._error(str(err))
        if skolemize:
            self._graph = graph.skolemize()
        else:
            self._graph = graph

    @override
    def _eval_select_query_string(
            self,
            text: str,
            headers: Optional[dict[str, Any]] = None,
            **kwargs
    ) -> SPARQL_Results:
        LOG.debug('%s()\n%s', self._eval_query_string.__qualname__, text)
        res = self._graph.query(self._prepare_query_string(text))
        data = cast(bytes, res.serialize(format='json'))
        assert data is not None
        return SPARQL_Results(json.loads(data))
