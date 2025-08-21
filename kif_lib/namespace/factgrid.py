# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..rdflib import Namespace
from ..typing import Final


class FactGrid:
    """The FactGrid namespace."""

    FACTGRID: Final[Namespace] = Namespace('https://database.factgrid.de/')
    P: Final[Namespace] = Namespace(FACTGRID['prop/'])
    PQ: Final[Namespace] = Namespace(P['qualifier/'])
    PQN: Final[Namespace] = Namespace(PQ['value-normalized/'])
    PQV: Final[Namespace] = Namespace(PQ['value/'])
    PR: Final[Namespace] = Namespace(P['reference/'])
    PRN: Final[Namespace] = Namespace(PR['value-normalized/'])
    PRV: Final[Namespace] = Namespace(PR['value/'])
    PS: Final[Namespace] = Namespace(P['statement/'])
    PSN: Final[Namespace] = Namespace(PS['value-normalized/'])
    PSV: Final[Namespace] = Namespace(PS['value/'])
    WD: Final[Namespace] = Namespace(FACTGRID['entity/'])
    WDGENID: Final[Namespace] = Namespace(FACTGRID['.well-known/genid/'])
    WDNO: Final[Namespace] = Namespace(P['novalue/'])
    WDREF: Final[Namespace] = Namespace(FACTGRID['reference/'])
    WDS: Final[Namespace] = Namespace(WD['statement/'])
    WDT: Final[Namespace] = Namespace(P['direct/'])
    WDV: Final[Namespace] = Namespace(FACTGRID['value/'])

    schema: Final[dict[str, Namespace]] = {
        'p': P,
        'pq': PQ,
        'pqv': PQV,
        'pr': PR,
        'prv': PRV,
        'ps': PS,
        'psv': PSV,
        'wdno': WDNO,
        'wdt': WDT,
    }
