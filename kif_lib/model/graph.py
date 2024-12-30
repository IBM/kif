# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ..typing import ClassVar, Iterable, override, TypeAlias, Union
from .set import ClosedTermSet
from .statement import Statement, TStatement
from .term import Variable

TGraph: TypeAlias = Union['Graph', Iterable[TStatement]]
VGraph: TypeAlias = Union['GraphVariable', 'Graph']
VTGraph: TypeAlias = Union[Variable, VGraph, TGraph]


class GraphVariable(Variable):
    """Graph variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Graph]]  # pyright: ignore


class Graph(
        ClosedTermSet[Statement],
        children_class=Statement,
        variable_class=GraphVariable
):
    """Graph (set of statements).

    Parameters:
       statements: Statements.
    """

    children_class: ClassVar[type[Statement]]       # pyright: ignore
    variable_class: ClassVar[type[GraphVariable]]   # pyright: ignore

    @override
    def __init__(self, *statements: Statement) -> None:
        super().__init__(*statements)
