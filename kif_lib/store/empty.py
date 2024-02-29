# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ..model import AnnotationRecordSet, FilterPattern, Statement
from ..typing import Any, Iterable, Iterator, Optional
from .abc import Store


class EmptyStore(Store, store_name='empty', store_description='Empty store'):
    """Empty store.

    Parameters:
       store_name: Name of the store plugin to instantiate.
    """

    def __init__(self, store_name: str, *args, **kwargs: Any):
        assert store_name == self.store_name
        super().__init__(*args, **kwargs)

    def _contains(self, pattern: FilterPattern) -> bool:
        return False

    def _count(self, pattern: FilterPattern) -> int:
        return 0

    def _filter(
            self,
            pattern: FilterPattern,
            limit: int
    ) -> Iterator[Statement]:
        return iter(())

    def _get_annotations(
            self,
            stmts: Iterable[Statement],
    ) -> Iterator[tuple[Statement, Optional[AnnotationRecordSet]]]:
        return map(lambda stmt: (stmt, None), stmts)
