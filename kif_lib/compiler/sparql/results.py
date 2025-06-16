# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0
#
# $Id$
#
# SPARQL query JSON results.
# See <https://www.w3.org/TR/sparql11-results-json>.
#
# ** KEEP THIS FILE SELF-CONTAINED! **

from __future__ import annotations

from collections.abc import Sequence
from typing import Union

from typing_extensions import Literal, NotRequired, TypeAlias, TypedDict


class SPARQL_ResultsHead(TypedDict):
    vars: NotRequired[Sequence[str]]
    link: NotRequired[Sequence[str]]


class SPARQL_ResultsTermBlankNode(TypedDict):
    type: Literal['bnode']
    value: str


class SPARQL_ResultsTermIRI(TypedDict):
    type: Literal['uri']
    value: str


SPARQL_ResultsTermLiteral = TypedDict(
    'SPARQL_ResultsTermLiteral', {
        'type': Literal['literal'],
        'value': str,
        'datatype': NotRequired[str],
        'xml:lang': NotRequired[str],
    })


SPARQL_ResultsTerm: TypeAlias = Union[
    SPARQL_ResultsTermBlankNode,
    SPARQL_ResultsTermIRI,
    SPARQL_ResultsTermLiteral]

SPARQL_ResultsBinding: TypeAlias = dict[str, SPARQL_ResultsTerm]


class SPARQL_ResultsBindings(TypedDict):
    bindings: Sequence[SPARQL_ResultsBinding]


class SPARQL_Results(TypedDict):
    head: NotRequired[SPARQL_ResultsHead]
    results: NotRequired[SPARQL_ResultsBindings]


class SPARQL_ResultsAsk(TypedDict):
    boolean: NotRequired[Literal[True, False]]
