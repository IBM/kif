# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import Any, cast, Iterable, Optional, override, Union
from .kif_object import TLocation
from .kif_object_set import KIF_ObjectSet
from .reference_record import ReferenceRecord

TFrozenset = frozenset
TReferenceRecordSet = Union['ReferenceRecordSet', Iterable[ReferenceRecord]]


class ReferenceRecordSet(KIF_ObjectSet):
    """Set of reference records.

    Parameters:
       refs: Reference records.
    """

    @classmethod
    def _check_arg_reference_record_set(
            cls,
            arg: TReferenceRecordSet,
            function: Optional[TLocation] = None,
            name: Optional[str] = None,
            position: Optional[int] = None
    ) -> 'ReferenceRecordSet':
        return cast(ReferenceRecordSet, cls._check_arg_kif_object_set(
            arg, function, name, position))

    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._preprocess_arg_reference_record(arg, i)

    @property
    @override
    def frozenset(self) -> TFrozenset[ReferenceRecord]:
        """The set of reference records as a frozen set."""
        return self.get_frozenset()

    @override
    def get_frozenset(self) -> TFrozenset[ReferenceRecord]:
        """Gets the set of reference records as a frozen set.

        Returns:
           Frozen set.
        """
        return cast(frozenset[ReferenceRecord], self._get_frozenset())

    @override
    def union(self, *others: KIF_ObjectSet) -> 'ReferenceRecordSet':
        """Computes the union of set and `others`.

        Parameters:
           others: Reference record sets.

        Returns:
           The resulting reference record set.
        """
        return cast(ReferenceRecordSet, self._union(others))
