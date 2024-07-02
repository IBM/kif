# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing_extensions import TYPE_CHECKING

from ..typing import Any, Optional, override
from .kif_object import KIF_Object
from .rank import Normal, Rank

if TYPE_CHECKING:               # pragma: no cover
    from .set import ReferenceRecordSet, SnakSet, TReferenceRecordSet, TSnakSet


class AnnotationRecord(KIF_Object):
    """Annotation record (qualifiers, references, and rank).

    Parameters:
       qualifiers: Qualifiers.
       references: References.
       rank: Rank.
    """

    def __init__(
            self,
            qualifiers: Optional['TSnakSet'] = None,
            references: Optional['TReferenceRecordSet'] = None,
            rank: Optional[Rank] = None
    ):
        super().__init__(qualifiers, references, rank)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:
            from .set import SnakSet
            return SnakSet.check_optional(arg, SnakSet(), type(self), None, i)
        elif i == 2:
            from .set import ReferenceRecordSet
            return ReferenceRecordSet.check_optional(
                arg, ReferenceRecordSet(), type(self), None, i)
        elif i == 3:
            return Rank.check_optional(arg, Normal, type(self), None, i)
        else:
            raise self._should_not_get_here()

    @property
    def qualifiers(self) -> 'SnakSet':
        """The qualifiers of annotation record."""
        return self.get_qualifiers()

    def get_qualifiers(self) -> 'SnakSet':
        """Gets the qualifiers of annotation record.

        Returns:
           Qualifiers.
        """
        return self.args[0]

    @property
    def references(self) -> 'ReferenceRecordSet':
        """The references of annotation record."""
        return self.get_references()

    def get_references(self) -> 'ReferenceRecordSet':
        """Gets the references of annotation record.

        Returns:
           References.
        """
        return self.args[1]

    @property
    def rank(self) -> Rank:
        """The rank of annotation record."""
        return self.get_rank()

    def get_rank(self) -> Rank:
        """Gets rank of annotation record.

        Returns:
           Rank.
        """
        return self.args[2]
