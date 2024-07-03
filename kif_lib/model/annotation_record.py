# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..typing import (
    Any,
    ClassVar,
    Final,
    Iterable,
    Optional,
    override,
    TypeAlias,
    Union,
)
from .kif_object import KIF_Object
from .rank import NormalRank, Rank
from .set import (
    KIF_ObjectSet,
    ReferenceRecordSet,
    SnakSet,
    TReferenceRecordSet,
    TSnakSet,
)

TAnnotationRecordSet: TypeAlias =\
    Union['AnnotationRecordSet', Iterable['AnnotationRecord']]


class AnnotationRecord(KIF_Object):
    """Annotation record (qualifiers, references, and rank).

    Parameters:
       qualifiers: Qualifiers.
       references: References.
       rank: Rank.
    """

    #: Default qualifiers.
    default_qualifiers: Final[SnakSet] = SnakSet()

    #: Default references.
    default_references: Final[ReferenceRecordSet] = ReferenceRecordSet()

    #: Default rank.
    default_rank: Final[Rank] = NormalRank()

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
            return SnakSet.check_optional(
                arg, self.default_qualifiers, type(self), None, i)
        elif i == 2:
            return ReferenceRecordSet.check_optional(
                arg, self.default_references, type(self), None, i)
        elif i == 3:
            return Rank.check_optional(
                arg, self.default_rank, type(self), None, i)
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


class AnnotationRecordSet(
        KIF_ObjectSet[AnnotationRecord],
        children_class=AnnotationRecord
):
    """Set of annotation records.

    Parameters:
       annotation_records: Annotation records.
    """

    children_class: ClassVar[type[AnnotationRecord]]  # pyright: ignore

    @override
    def __init__(self, *annotation_records: AnnotationRecord):
        super().__init__(*annotation_records)
