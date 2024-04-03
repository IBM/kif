# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ...rdflib import URIRef
from ...typing import Sequence, TypeAlias, Union

T_URI: TypeAlias = Union[URIRef, str]


class Query:
    prefix_declarations: Sequence[tuple[str, T_URI]] = list()
