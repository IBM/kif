# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re

from ....model import Lexeme, LexemeTemplate, LexemeVariable
from ....namespace.factgrid import FactGrid
from ....typing import override
from .factgrid_options import FactGridMappingOptions
from .wikidata import Wikidata, WikidataMapping


class FactGridMapping(WikidataMapping):
    """FactGrid SPARQL mapping."""

    _entries = [                # exclude lexeme related stuff
        entry for entry in WikidataMapping._entries if not any(map(
            lambda pat: next(pat.traverse(lambda x: isinstance(
                x, (Lexeme, LexemeTemplate, LexemeVariable))), None),
            entry.patterns))]

    _default_type = FactGrid.WDT.P2 / (FactGrid.WDT.P420 * '*')  # type: ignore

    _default_subtype = FactGrid.WDT.P420 * '+'  # type: ignore

    _re_item_uri = re.compile(
        f'^{re.escape(FactGrid.WD)}Q[1-9][0-9]*$')

    _re_property_uri = re.compile(
        f'^{re.escape(FactGrid.WD)}P[1-9][0-9]*$')

    _repl_item_uri = {
        Wikidata.WD[k]: FactGrid.WD[v] for k, v in {
            'Q5': 'Q7',         # human
        }.items()
    }

    _repl_property_uri = {
        Wikidata.WD[k]: FactGrid.WD[v] for k, v in {
            'P31': 'P2',        # instance of
            'P279': 'P420',     # subclass of
        }.items()
    }

    @override
    def _get_context_options(self) -> FactGridMappingOptions:
        return self.context.options.compiler.sparql.mapping.factgrid
