# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...typing import TypeAlias
from .builder import Query
from .compiler import SPARQL_Compiler
from .filter_compiler import SPARQL_FilterCompiler
from .mapping import SPARQL_Mapping

BNode: TypeAlias = Query.BNode
Literal: TypeAlias = Query.Literal
URI: TypeAlias = Query.URI
Variable: TypeAlias = Query.Variable
Term: TypeAlias = Query.Term

V_BNode: TypeAlias = Query.V_BNode
VLiteral: TypeAlias = Query.VLiteral
V_URI: TypeAlias = Query.V_URI
VTerm: TypeAlias = Query.VTerm


__all__ = (
    'Query',
    'SPARQL_Compiler',
    'SPARQL_FilterCompiler',
    'SPARQL_Mapping',
)
