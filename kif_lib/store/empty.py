# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Iterable

from ..model import AnnotationRecordSet, FilterPattern, Statement
from ..typing import Iterator, Optional
from .abc import Store


class EmptyStore(Store, name='empty', description='Empty store'):
    """Empty store."""

    def _contains(self, pattern: FilterPattern) -> bool:
        return False

    def _count(self, pattern: FilterPattern) -> int:
        return 0

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        return iter([])

    def _get_annotations(
            self,
            stmts: Iterable[Statement],
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        for stmt in stmts:
            yield stmt, None
