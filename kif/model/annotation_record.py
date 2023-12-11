# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from typing import Optional

from .kif_object import KIF_Object
from .rank import Normal, Rank
from .reference_record_set import ReferenceRecordSet, TReferenceRecordSet
from .snak_set import SnakSet, TSnakSet


class AnnotationRecord(KIF_Object):
    """Annotation record (qualifiers, references, and rank).

    Parameters:
       arg1: Qualifiers.
       arg2: References.
       arg3: Rank.
    """

    def __init__(
            self,
            arg1: Optional[TSnakSet] = None,
            arg2: Optional[TReferenceRecordSet] = None,
            arg3: Optional[Rank] = None
    ):
        super().__init__(arg1, arg2, arg3)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_optional_arg_snak_set(arg, i, SnakSet())
        elif i == 2:
            return self._preprocess_optional_arg_reference_record_set(
                arg, i, ReferenceRecordSet())
        elif i == 3:
            return self._preprocess_optional_arg_rank(arg, i, Normal)
        else:
            return self._should_not_get_here()

    @property
    def qualifiers(self) -> SnakSet:
        """Annotated qualifiers."""
        return self.get_qualifiers()

    def get_qualifiers(self) -> SnakSet:
        """Gets annotated qualifiers.

        Returns:
           Annotated qualifiers.
        """
        return self.args[0]

    @property
    def references(self) -> ReferenceRecordSet:
        """Annotated references."""
        return self.get_references()

    def get_references(self) -> ReferenceRecordSet:
        """Gets annotated references.

        Returns:
           Annotated references.
        """
        return self.args[1]

    @property
    def rank(self) -> Rank:
        """Annotated rank."""
        return self.get_rank()

    def get_rank(self) -> Rank:
        """Gets annotated rank.

        Returns:
           Annotated rank.
        """
        return self.args[2]
