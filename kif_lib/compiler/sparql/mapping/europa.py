# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from .... import functools
from ....context import Context
from ....model import Item, Normal, Variables
from ....namespace import RDF
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
        f'^{re.escape(Europa.DATASET)}CID[1-9][0-9]*$')

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

# -- Dataset ---------------------------------------------------------------

    @M.register(
        [wd.instance_of(Item(s), wd.data_set)],
        {s: CheckDataset()},
        rank=Normal)
    def wd_instance_of_data_set(self, c: C, s: V_URI) -> None:
        c.q.triples()((s, RDF.type, DCAT.Dataset))
