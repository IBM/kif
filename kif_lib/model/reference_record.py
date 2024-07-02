# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import ClassVar, Iterable, override, TypeAlias, Union
from .snak import Snak
from .snak_set import SnakSet

TReferenceRecord: TypeAlias = Union['ReferenceRecord', SnakSet, Iterable[Snak]]


class ReferenceRecord(SnakSet, children_class=Snak):
    """Reference record (set of snaks).

    Parameters:
       snaks: Snaks.
    """

    children_class: ClassVar[type[Snak]]  # pyright: ignore

    @override
    def __init__(self, *objects: Snak):
        super().__init__(*objects)  # type: ignore
