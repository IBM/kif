# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .... import functools
from ....context import Context
from ....model import Item, Normal, Property, Variables
from ....namespace import OWL, Wikidata
from ....namespace.yago import YAGO
from ....typing import Final, TypeAlias
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M
from .wikidata import WikidataMapping

if TYPE_CHECKING:  # pragma: no cover
    from .yago_options import YagoMappingOptions

__all__ = (
    'YagoMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral

#: Variables used in register patterns.
s, s0, p, v, v0 = Variables('s', 's0', 'p', 'v', 'v0')


class YagoMapping(M):
    """Yago SPARQL mapping."""

# -- Checks ----------------------------------------------------------------

    _re_resource_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(str(YAGO))}.*$')

    #: Checks whether argument is a resource URI.
    CheckResource: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_resource_uri)

    #: Checks whether argument is a Wikidata item.
    CheckWikidataItem: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=WikidataMapping._re_item_uri)

    #: Checks whether argument is a Wikidata property.
    CheckWikidataProperty: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=WikidataMapping._re_property_uri)

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    #: Yago SPARQL mapping options.
    _options: YagoMappingOptions

    def __init__(
            self,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()

    def _get_context_options(self) -> YagoMappingOptions:
        return self.context.options.compiler.sparql.mapping.yago

    @property
    def options(self) -> YagoMappingOptions:
        """The Yago SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> YagoMappingOptions:
        """Gets the Yago SPARQL mapping options.

        Returns:
           Yago SPARQL mapping options.
        """
        return self._options

    @M.register(
        [Property(p)(Item(s), Item(v))],
        {s: CheckResource(),
         v: CheckResource()},
        rank=Normal)
    def p_r_r(
            self,
            c: C,
            p: V_URI,
            s: V_URI,
            v: V_URI
    ) -> None:
        c.q.triples()((s, p, v))

    @M.register(
        [wd.said_to_be_the_same_as(Item(s), Item(v))],
        {s: CheckResource(),
         v: CheckWikidataItem()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_said_to_be_the_same_as(self, c: C, s: V_URI, v: V_URI) -> None:
        c.q.triples()((s, OWL.sameAs, v))
        if isinstance(v, Var):
            c.q.filter(c.q.strstarts(c.q.str(v), str(Wikidata.WD)))
