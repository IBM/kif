# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    DeprecatedRank,
    ExternalIdDatatype,
    Filter,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    KIF_Object,
    LexemeDatatype,
    NormalRank,
    NoValueSnak,
    PreferredRank,
    Property,
    PropertyDatatype,
    Quantity,
    QuantityDatatype,
    ReferenceRecord,
    SnakSet,
    SomeValueSnak,
    String,
    StringDatatype,
    Text,
    TextDatatype,
    Time,
    TimeDatatype,
    ValueSnak,
)
from kif_lib.typing import cast
from kif_lib.vocabulary import wd

from ..tests import TestCase


class Test(TestCase):

    def md_link(self, label, url=None):
        return f'[{label}]({url or label})'

    def md_sexp(self, name, *args, f=None, sep1=' ', sep2=' ', sep3=''):
        if not args:
            return f'**{name}**'
        else:
            body = sep2.join(map(f or self._md_sexp_helper, args))
            return f'(**{name}**{sep1}{body}{sep3})'

    def _md_sexp_helper(self, x):
        return x.to_markdown() if isinstance(x, KIF_Object) else str(x)

    def assert_to_markdown(self, obj, md):
        self.assertEqual(obj.to_markdown(), md)

    def test_datatype_to_markdown(self) -> None:
        self.assert_to_markdown(
            ItemDatatype(), self.md_sexp('ItemDatatype'))
        self.assert_to_markdown(
            PropertyDatatype(), self.md_sexp('PropertyDatatype'))
        self.assert_to_markdown(
            LexemeDatatype(), self.md_sexp('LexemeDatatype'))
        self.assert_to_markdown(
            IRI_Datatype(), self.md_sexp('IRI_Datatype'))
        self.assert_to_markdown(
            TextDatatype(), self.md_sexp('TextDatatype'))
        self.assert_to_markdown(
            StringDatatype(), self.md_sexp('StringDatatype'))
        self.assert_to_markdown(
            ExternalIdDatatype(), self.md_sexp('ExternalIdDatatype'))
        self.assert_to_markdown(
            QuantityDatatype(), self.md_sexp('QuantityDatatype'))
        self.assert_to_markdown(
            TimeDatatype(), self.md_sexp('TimeDatatype'))

    def test_item_to_markdown(self) -> None:
        # known prefix: know label
        self.assert_to_markdown(
            wd.Adam, self.md_sexp('Item', self.md_link(
                'Adam', wd.Adam.iri.content)))
        # known prefix: unknown label
        self.assert_to_markdown(
            wd.Q('_'), self.md_sexp('Item', self.md_link(
                'wd:Q_', wd.Q('_').iri.content)))
        # unknown prefix
        self.assert_to_markdown(
            Item('x'), self.md_sexp('Item', self.md_link('x', 'x')))

    def test_property_to_markdown(self) -> None:
        # known prefix: know label
        self.assert_to_markdown(
            wd.mass, self.md_sexp('Property', self.md_link(
                'mass', wd.mass.iri.content)))
        # known prefix: unknown label
        self.assert_to_markdown(
            wd.P('_'), self.md_sexp('Property', self.md_link(
                'wd:P_', wd.P('_').iri.content)))
        # unknown prefix
        self.assert_to_markdown(
            Property('x'), self.md_sexp('Property', self.md_link('x', 'x')))

    def test_iri_to_markdown(self) -> None:
        # known prefix
        self.assert_to_markdown(
            IRI('http://www.wikidata.org/entity/Q5'),
            self.md_link('wd:Q5', 'http://www.wikidata.org/entity/Q5'))
        # unknown prefix: absolute iri
        self.assert_to_markdown(
            IRI('http://prefix/x'),
            self.md_link('http://prefix/x'))
        # unknown prefix: relative iri
        self.assert_to_markdown(
            IRI('prefix/x'),
            self.md_link('prefix/x', 'prefix/x'))
        self.assert_to_markdown(
            IRI('x'),
            self.md_link('x', 'x'))

    def test_text_to_markdown(self) -> None:
        self.assert_to_markdown(Text('abc'), '"abc"@en')
        self.assert_to_markdown(Text('abc', 'fr'), '"abc"@fr')
        # escape
        self.assert_to_markdown(Text('_', 'pt'), r'"\_"@pt')

    def test_string_to_markdown(self) -> None:
        self.assert_to_markdown(String('abc'), '"abc"')
        # escape
        self.assert_to_markdown(String('_'), r'"\_"')
        self.assert_to_markdown(String('*'), r'"\*"')
        self.assert_to_markdown(String('`'), r'"\`"')
        self.assert_to_markdown(String('[]'), r'"\[]"')

    def test_quantity_to_markdown(self) -> None:
        # amount
        self.assert_to_markdown(
            Quantity(0),
            self.md_sexp('Quantity', 0))
        # amount, unit
        self.assert_to_markdown(
            Quantity(0, wd.dalton),
            self.md_sexp('Quantity', 0, wd.dalton))
        # amount, unit, lower bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, -1),
            self.md_sexp('Quantity', 0, '[-1,∞]', wd.kilogram))
        # amount, unit, upper bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, None, 1),
            self.md_sexp('Quantity', 0, '[-∞,1]', wd.kilogram))
        # amount, unit, lower bound, upper bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, -1, 1),
            self.md_sexp('Quantity', 0, '±1', wd.kilogram))
        # amount, lower bound
        self.assert_to_markdown(
            Quantity(-1, None, 0),
            self.md_sexp('Quantity', -1, '[0,∞]'))
        # amount, upper bound
        self.assert_to_markdown(
            Quantity(-1, None, None, 0),
            self.md_sexp('Quantity', -1, '[-∞,0]'))
        # amount, lower bound, upper bound
        self.assert_to_markdown(
            Quantity(-1, None, -1, 0),
            self.md_sexp('Quantity', -1, '[-1,0]'))
        self.assert_to_markdown(
            Quantity('2', None, '1', '3'),
            self.md_sexp('Quantity', 2, '±1'))
        self.assert_to_markdown(
            Quantity('-2', None, '-3', '-1'),
            self.md_sexp('Quantity', -2, '±1'))

    def test_time_to_markdown(self) -> None:
        # time
        self.assert_to_markdown(
            Time('2023-09-28'),
            self.md_sexp('Time', '2023-09-28'))
        self.assert_to_markdown(
            Time('2023-09-28T00'),
            self.md_sexp('Time', '2023-09-28'))
        self.assert_to_markdown(
            Time('2023-09-28T00:00'),
            self.md_sexp('Time', '2023-09-28'))
        self.assert_to_markdown(
            Time('2023-09-28T00:00:00'),
            self.md_sexp('Time', '2023-09-28'))
        self.assert_to_markdown(
            Time('2023-09-28T00:00:01'),
            self.md_sexp('Time', '2023-09-28'))
        # time, precision
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.DAY),
            self.md_sexp('Time', '2023-09-28'))
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.HOUR),
            self.md_sexp('Time', '2023-09-28T00:00:00+00:00'))
        self.assert_to_markdown(
            Time('2023-09-28T01', Time.Precision.HOUR),
            self.md_sexp('Time', '2023-09-28T01:00:00+00:00'))
        # time, timezone
        self.assert_to_markdown(
            Time('2023-09-28', None, 3),
            self.md_sexp('Time', '2023-09-28'))
        # time, calendar
        self.assert_to_markdown(
            Time('2023-09-28', None, None, wd.proleptic_Gregorian_calendar),
            self.md_sexp('Time', '2023-09-28'))

    def test_snak_to_markdown(self) -> None:
        self.assert_to_markdown(
            wd.mass(Quantity(0)),
            self.md_sexp('ValueSnak', wd.mass, Quantity(0)))
        self.assert_to_markdown(
            SomeValueSnak(wd.mass),
            self.md_sexp('SomeValueSnak', wd.mass))
        self.assert_to_markdown(
            NoValueSnak(wd.mass),
            self.md_sexp('NoValueSnak', wd.mass))

    def test_statement_to_markdown(self) -> None:
        self.assert_to_markdown(
            wd.mass(wd.benzene, Quantity(0)),
            self.md_sexp('Statement', wd.benzene, wd.mass(Quantity(0))))

    def test_rank_to_markdown(self) -> None:
        self.assert_to_markdown(
            PreferredRank(), self.md_sexp('PreferredRank'))
        self.assert_to_markdown(
            NormalRank(), self.md_sexp('NormalRank'))
        self.assert_to_markdown(
            DeprecatedRank(), self.md_sexp('DeprecatedRank'))

    def test_reference_record_to_markdown(self) -> None:
        ref = ReferenceRecord()
        self.assert_to_markdown(ref, '(**ReferenceRecord**)')
        ref = ReferenceRecord(ValueSnak(wd.part_of, wd.benzene))
        self.assert_to_markdown(ref, '''\
(**ReferenceRecord**
- (**ValueSnak** (**Property** [part of](http://www.wikidata.org/entity/P361)) (**Item** [benzene](http://www.wikidata.org/entity/Q2270))))''')  # noqa: E501
        ref = ReferenceRecord(
            cast(ValueSnak, wd.canonical_SMILES(String('ABC'))),
            cast(ValueSnak, wd.country(wd.Brazil)),
            cast(ValueSnak, wd.mass(Quantity(0))))
        self.assert_to_markdown(ref, '''\
(**ReferenceRecord**
- (**ValueSnak** (**Property** [country](http://www.wikidata.org/entity/P17)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))
- (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) (**Quantity** 0))
- (**ValueSnak** (**Property** [canonical SMILES](http://www.wikidata.org/entity/P233)) "ABC"))''')  # noqa: E501

    def test_filter_to_markdown(self) -> None:
        self.assert_to_markdown(Filter(), '''\
(**Filter**
- (**FullFingerprint**)
- (**FullFingerprint**)
- (**FullFingerprint**)
- `0b111`)''')
        f = Filter(wd.benzene)
        self.assert_to_markdown(f, '''\
(**Filter**
- (**ValueFingerprint** (**Item** [benzene](http://www.wikidata.org/entity/Q2270)))
- (**FullFingerprint**)
- (**FullFingerprint**)
- `0b111`)''')  # noqa: E501
        f = Filter(
            None,
            None,
            [cast(ValueSnak, wd.country(wd.Brazil)),
             NoValueSnak(wd.date_of_birth)],
            Filter.NO_VALUE_SNAK)
        self.assert_to_markdown(
            f, '''\
(**Filter**
- (**FullFingerprint**)
- (**FullFingerprint**)
- (**AndFingerprint**
  - (**SnakFingerprint** (**ValueSnak** (**Property** [country](http://www.wikidata.org/entity/P17)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155))))
  - (**SnakFingerprint** (**NoValueSnak** (**Property** [date of birth](http://www.wikidata.org/entity/P569)))))
- `0b100`)''')  # noqa: E501

    def test_snak_set_to_markdown(self) -> None:
        s = SnakSet()
        self.assert_to_markdown(s, '(**SnakSet**)')
        s = SnakSet(cast(ValueSnak, wd.part_of(wd.benzene)))
        self.assert_to_markdown(s, '''\
(**SnakSet**
- (**ValueSnak** (**Property** [part of](http://www.wikidata.org/entity/P361)) (**Item** [benzene](http://www.wikidata.org/entity/Q2270))))''')  # noqa: E501


if __name__ == '__main__':
    Test.main()
