# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .... import functools, itertools
from ....context import Context
from ....model import IRI, Item, Normal, Text, Time, Variables
from ....namespace import DCT, RDF, RDFS
from ....namespace.dcat import DCAT
from ....namespace.europa import Europa
from ....typing import Final, TypeAlias
from ....vocabulary import wd
from ..filter_compiler import SPARQL_FilterCompiler as C
from .mapping import SPARQL_Mapping as M

if TYPE_CHECKING:  # pragma: no cover
    from .europa_options import EuropaMappingOptions

__all__ = (
    'EuropaMapping',
)

Arg: TypeAlias = M.EntryCallbackArg
URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
Var: TypeAlias = C.Query.Variable
VLiteral: TypeAlias = C.Query.VLiteral

#: Variables used in register patterns.
s, s0, p, v, v0 = Variables('s', 's0', 'p', 'v', 'v0')


class EuropaMapping(M):
    """Europa (data.europa.eu) SPARQL mapping."""

# -- Checks ----------------------------------------------------------------

    _re_dataset_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Europa.DATASET)}.*$')

    #: Checks whether argument is a dataset URI.
    CheckDataset: Final[M.EntryCallbackArgProcessorAlias] =\
        functools.partial(M.CheckURI, match=_re_dataset_uri)

# -- Initialization --------------------------------------------------------

    __slots__ = (
        '_options',
    )

    #: Europa SPARQL mapping options.
    _options: EuropaMappingOptions

    def __init__(
            self,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()

    def _get_context_options(self) -> EuropaMappingOptions:
        return self.context.options.compiler.sparql.mapping.europa

    @property
    def options(self) -> EuropaMappingOptions:
        """The Europa SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> EuropaMappingOptions:
        """Gets the Europa SPARQL mapping options.

        Returns:
           Europa SPARQL mapping options.
        """
        return self._options

    def _start_dataset(self, c: C, x: V_URI, *xs: V_URI) -> None:
        c.q.triples()(*map(
            lambda y: (y, RDF.type, DCAT.Dataset), itertools.chain((x,), xs)))

    def _p_text(
            self,
            c: C,
            s: V_URI,
            p: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        if isinstance(v0, Var):
            c.q.triples()((s, p, v))
            c.q.bind(c.q.lang(v), v0)
        elif isinstance(v, Var):
            c.q.triples()((s, p, v))
            c.q.filter(c.q.eq(c.q.lang(v), v0))
        else:
            c.q.triples()((s, p, c.q.Literal(v, v0)))

# -- Dataset ---------------------------------------------------------------

    @M.register(
        [wd.label(Item(s), Text(v, v0))],
        {s: CheckDataset()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_label_dataset(
            self,
            c: C,
            s: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        self._start_dataset(c, s)
        with c.q.union():
            with c.q.group():
                self._p_text(c, s, DCT.title, v, v0)
            with c.q.group():
                self._p_text(c, s, RDFS.label, v, v0)

    @M.register(
        [wd.description(Item(s), Text(v, v0))],
        {s: CheckDataset()},
        priority=M.LOW_PRIORITY,
        rank=Normal)
    def wd_description_dataset(
            self,
            c: C,
            s: V_URI,
            v: VLiteral,
            v0: VLiteral
    ) -> None:
        self._start_dataset(c, s)
        self._p_text(c, s, DCT.description, v, v0)

    @M.register(
        [wd.instance_of(Item(s), wd.dataset)],
        {s: CheckDataset()},
        rank=Normal)
    def wd_instance_of_dataset(self, c: C, s: V_URI) -> None:
        self._start_dataset(c, s)

    @M.register(
        [wd.last_update(Item(s), Time(
            v, Time.DAY, 0, wd.proleptic_Gregorian_calendar))],
        {s: CheckDataset()},
        rank=Normal)
    def wd_last_update(self, c: C, s: V_URI, v: VLiteral) -> None:
        self._start_dataset(c, s)
        c.q.triples()((s, DCT.modified, v))

    @M.register(
        [wd.publication_date(Item(s), Time(
            v, Time.DAY, 0, wd.proleptic_Gregorian_calendar))],
        {s: CheckDataset()},
        rank=Normal)
    def wd_publication_date(self, c: C, s: V_URI, v: VLiteral) -> None:
        self._start_dataset(c, s)
        c.q.triples()((s, DCT.created|DCT.issued, v))  # type: ignore

    @M.register(
        [wd.reference_URL(Item(s), IRI(v))],
        {s: CheckDataset()},
        rank=Normal)
    def wd_reference_url_dataset(self, c: C, s: V_URI, v: V_URI) -> None:
        self._start_dataset(c, s)
        c.q.triples()((s, DCAT.landingPage, v))
