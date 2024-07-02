# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import ClassVar, Iterable, override, Union
from .kif_object_set import KIF_ObjectSet
from .value import Text, TText, TValue, Value

TTextSet = Union['TextSet', Iterable[Text]]
TValueSet = Union['ValueSet', Iterable[Value]]


class ValueSet(KIF_ObjectSet, children_class=Value):
    """Set of values.

    Parameters:
       values: Values.
    """

    children_class: ClassVar[type[Value]]  # pyright: ignore

    @override
    def __init__(self, *objects: TValue):
        super().__init__(*objects)  # type: ignore


class TextSet(ValueSet, children_class=Text):
    """Set of texts.

    Parameters:
       texts: Texts.
    """

    children_class: ClassVar[type[Text]]  # pyright: ignore

    @override
    def __init__(self, *objects: TText):
        super().__init__(*objects)  # type: ignore
