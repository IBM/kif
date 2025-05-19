# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Filter,
    Item,
    Lexeme,
    Property,
    ReferenceRecord,
    ReferenceRecordSet,
    Store,
)
from kif_lib.typing import Any, Final

from ..tests import StoreTestCase


class Test(StoreTestCase):

    @classmethod
    def KB(cls, **kwargs: Any) -> Store:
        return Store('empty', **kwargs)

    def test_base_filter(self) -> None:
        f1: Final[Filter] = Filter(Item('x'))
        f2: Final[Filter] = Filter(
            Item('x0'), Property('y'), Item('z') | Lexeme('w'),
            snak_mask=Filter.VALUE_SNAK,
            subject_mask=Filter.ITEM,
            property_mask=Filter.PROPERTY,
            value_mask=Filter.ENTITY,
            rank_mask=Filter.PREFERRED,
            language='fr',
            annotated=True)
        kb = self.KB()
        self._test_option(
            kb, 'base_filter', [(f1, f1), (f2, f2)], type_error=0)

        def _test_option_proxy(name: str) -> None:
            saved_value = getattr(kb, name)
            with kb():
                setattr(kb, name, getattr(f1, name))
                self.assertEqual(getattr(kb, name), getattr(f1, name))
                with kb(base_filter=f2):
                    self.assertEqual(getattr(kb, name), getattr(f2, name))
                    setattr(kb, name, getattr(f1, name))
                    self.assertEqual(kb.base_filter, f2.replace(
                        **{name: getattr(f1, name)}))
                self.assertEqual(getattr(kb, name), getattr(f1, name))
            self.assertEqual(getattr(kb, name), saved_value)
        _test_option_proxy('subject')
        _test_option_proxy('property')
        _test_option_proxy('value')
        _test_option_proxy('snak_mask')
        _test_option_proxy('subject_mask')
        _test_option_proxy('property_mask')
        _test_option_proxy('value_mask')
        _test_option_proxy('rank_mask')
        _test_option_proxy('language')
        _test_option_proxy('annotated')

    def test_best_ranked(self) -> None:
        self._test_option_bool(self.KB(), 'best_ranked')

    def test_debug(self) -> None:
        self._test_option_bool(self.KB(), 'debug')

    def test_distinct(self) -> None:
        self._test_option_bool(self.KB(), 'distinct')

    def test_extra_references(self) -> None:
        ref1: Final[ReferenceRecord] = ReferenceRecord(
            Property('p')('abc'),
            Property('q')(Property('p')))
        ref2: Final[ReferenceRecord] = ReferenceRecord(Property('r')(0))
        ref3: Final[ReferenceRecord] = ReferenceRecord()
        refs: Final[ReferenceRecordSet] = ReferenceRecordSet(ref1, ref2, ref3)
        self._test_option(
            self.KB(), 'extra_references',
            [([ref1, ref2, ref3], refs),
             ([], ReferenceRecordSet())], type_error=0)

    def test_limit(self) -> None:
        self._test_option_int(
            self.KB(), 'limit', lower_bound=0, optional=True)

    def test_lookahead(self) -> None:
        self._test_option_int(self.KB(), 'lookahead', lower_bound=1)

    def test_page_size(self) -> None:
        self._test_option_int(self.KB(), 'page_size', lower_bound=0)

    def test_timeout(self) -> None:
        self._test_option_float(
            self.KB(), 'timeout', lower_bound=0, optional=True)


if __name__ == '__main__':
    Test.main()
