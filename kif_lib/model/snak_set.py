# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import ClassVar, Iterable, override, TypeAlias, Union
from .kif_object_set import KIF_ObjectSet
from .snak import Snak

TFrozenset = frozenset
TSnakSet: TypeAlias = Union['SnakSet', Iterable[Snak]]


class SnakSet(KIF_ObjectSet, children_class=Snak):
    """Set of snaks.

    Parameters:
       snaks: Snaks.
    """

    children_class: ClassVar[type[Snak]]  # pyright: ignore

    @override
    def __init__(self, *objects: Snak):
        super().__init__(*objects)  # type: ignore
