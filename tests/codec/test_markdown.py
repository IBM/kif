# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Context,
    DeprecatedRank,
    ExternalId,
    ExternalIdDatatype,
    Filter,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    KIF_Object,
    Lexeme,
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
        self.assert_to_markdown(Item('x'), self.md_sexp('Item', 'x'))

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
            Property('x'), self.md_sexp('Property', 'x'))

    def test_lexeme_to_markdown(self) -> None:
        # known prefix: know lemma, category, language
        with Context():
            wd.English.register(label='English')
            wd.verb.register(label='verb')
            wd.L(33).register(
                lemma='change', category=wd.verb, language=wd.English)
            self.assert_to_markdown(
                wd.L(33), self.md_sexp(
                    'Lexeme',
                    self.md_link('change', wd.L(33).iri.content) + ' ('
                    + self.md_link('English', wd.English.iri.content) + ' '
                    + self.md_link("verb", wd.verb.iri.content) + ')'))
        # known prefix: unknown lemma, category, language
        with Context():
            self.assert_to_markdown(
                wd.L(33), self.md_sexp('Lexeme', self.md_link(
                    'wd:L33', wd.L(33).iri.content)))
        # unknown prefix
        self.assert_to_markdown(
            Lexeme('x'), self.md_sexp('Lexeme', 'x'))

    def test_iri_to_markdown(self) -> None:
        # known prefix
        self.assert_to_markdown(
            IRI('http://www.wikidata.org/entity/Q5'),
            'http://www.wikidata.org/entity/Q5')
        # unknown prefix: absolute iri
        self.assert_to_markdown(
            IRI('http://prefix/x'), 'http://prefix/x')
        # unknown prefix: relative iri
        self.assert_to_markdown(IRI('prefix/x'), 'prefix/x')
        self.assert_to_markdown(IRI('x'), 'x')

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

    def test_external_id_to_markdown(self) -> None:
        self.assert_to_markdown(ExternalId('abc'), '"abc"')
        # escape
        self.assert_to_markdown(ExternalId('_'), r'"\_"')
        self.assert_to_markdown(ExternalId('*'), r'"\*"')
        self.assert_to_markdown(ExternalId('`'), r'"\`"')
        self.assert_to_markdown(ExternalId('[]'), r'"\[]"')

    def test_quantity_to_markdown(self) -> None:
        dalton = self.md_link('dalton', wd.dalton.iri.content)
        kilogram = self.md_link('kilogram', wd.kilogram.iri.content)
        # amount
        self.assert_to_markdown(Quantity(0), '0')
        # amount, unit
        self.assert_to_markdown(
            Quantity(0, wd.dalton), '0 ' + dalton)
        # amount, unit, lower bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, -1), '0 [-1,+∞] ' + kilogram)
        # amount, unit, upper bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, None, 1), '0 [-∞,1] ' + kilogram)
        # amount, unit, lower bound, upper bound
        self.assert_to_markdown(
            Quantity(0, wd.kilogram, -1, 1), '0 ±1 ' + kilogram)
        # amount, lower bound
        self.assert_to_markdown(
            Quantity(-1, None, 0), '-1 [0,+∞]')
        # amount, upper bound
        self.assert_to_markdown(
            Quantity(-1, None, None, 0), '-1 [-∞,0]')
        # amount, lower bound, upper bound
        self.assert_to_markdown(
            Quantity(-1, None, -1, 0), '-1 [-1,0]')
        self.assert_to_markdown(
            Quantity('2', None, '1', '3'), '2 ±1')
        self.assert_to_markdown(
            Quantity('-2', None, '-3', '-1'), '-2 ±1')

    def test_time_to_markdown(self) -> None:
        self.assert_to_markdown(
            Time('2023-09-28'), '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28T00'), '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28T00:00'), '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28T00:00:00'), '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28T00:00:01'), '2023-09-28')
        # time, precision
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.BILLION_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.HUNDRED_THOUSAND_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.TEN_MILLION_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.MILLION_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.HUNDRED_THOUSAND_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.TEN_THOUSAND_YEARS),
            '2023-09-28')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.MILLENNIA), '3. millennium')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.CENTURY), '21. century')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.YEAR), '2023')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.MONTH), 'September 2023')
        self.assert_to_markdown(
            Time('2023-09-28', Time.Precision.DAY), '28 September 2023')
        self.assert_to_markdown(
            Time('2023-09-28T01:01', Time.Precision.HOUR),
            '28 September 2023 at 01:01')
        self.assert_to_markdown(
            Time('2023-09-28T00:04', Time.Precision.MINUTE),
            '28 September 2023 at 00:04')
        self.assert_to_markdown(
            Time('2023-09-28T01:02:03', Time.Precision.SECOND),
            '28 September 2023 at 01:02:03')
        # time, timezone
        self.assert_to_markdown(Time('2023-09-28', None, 3), '2023-09-28')
        # time, calendar
        self.assert_to_markdown(
            Time('2023-09-28', None, None,
                 wd.proleptic_Gregorian_calendar), '2023-09-28')

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
- (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) 0)
- (**ValueSnak** (**Property** [canonical SMILES](http://www.wikidata.org/entity/P233)) "ABC"))''')  # noqa: E501

    def test_filter_to_markdown(self) -> None:
        self.assert_to_markdown(Filter(), '''\
(**Filter**
- (**FullFingerprint**)
- (**FullFingerprint**)
- (**FullFingerprint**)
- **:snak_mask** `SnakMask.ALL`
- **:subject_mask** `DatatypeMask.ENTITY`
- **:property_mask** `DatatypeMask.PROPERTY`
- **:value_mask** `DatatypeMask.VALUE`
- **:rank_mask** `RankMask.ALL`
- **:best_ranked** `True`
- **:language** `None`
- **:annotated** `False`)''')
        f = Filter(wd.benzene)
        self.assert_to_markdown(f, '''\
(**Filter**
- (**ValueFingerprint** (**Item** [benzene](http://www.wikidata.org/entity/Q2270)))
- (**FullFingerprint**)
- (**FullFingerprint**)
- **:snak_mask** `SnakMask.ALL`
- **:subject_mask** `DatatypeMask.ENTITY`
- **:property_mask** `DatatypeMask.PROPERTY`
- **:value_mask** `DatatypeMask.VALUE`
- **:rank_mask** `RankMask.ALL`
- **:best_ranked** `True`
- **:language** `None`
- **:annotated** `False`)''')  # noqa: E501
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
- **:snak_mask** `SnakMask.NO_VALUE_SNAK`
- **:subject_mask** `DatatypeMask.ENTITY`
- **:property_mask** `DatatypeMask.PROPERTY`
- **:value_mask** `DatatypeMask.VALUE`
- **:rank_mask** `RankMask.ALL`
- **:best_ranked** `True`
- **:language** `None`
- **:annotated** `False`)''')  # noqa: E501

    def test_snak_set_to_markdown(self) -> None:
        s = SnakSet()
        self.assert_to_markdown(s, '(**SnakSet**)')
        s = SnakSet(cast(ValueSnak, wd.part_of(wd.benzene)))
        self.assert_to_markdown(s, '''\
(**SnakSet**
- (**ValueSnak** (**Property** [part of](http://www.wikidata.org/entity/P361)) (**Item** [benzene](http://www.wikidata.org/entity/Q2270))))''')  # noqa: E501


if __name__ == '__main__':
    Test.main()
