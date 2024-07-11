# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from kif_lib import (
    AnnotationRecord,
    Deprecated,
    EntityFingerprint,
    ExternalIdDatatype,
    Filter,
    Fingerprint,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemDescriptor,
    KIF_Object,
    LexemeDatatype,
    Normal,
    NoValueSnak,
    Preferred,
    Property,
    PropertyDatatype,
    PropertyFingerprint,
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

from .tests import kif_TestCase


class TestCodecMarkdown(kif_TestCase):

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

    def test_datatype_to_markdown(self):
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

    def test_item_to_markdown(self):
        # known prefix: know label
        self.assert_to_markdown(
            wd.Adam, self.md_sexp('Item', self.md_link(
                'Adam', wd.Adam.iri.value)))
        # known prefix: unknown label
        self.assert_to_markdown(
            wd.Q('_'), self.md_sexp('Item', self.md_link(
                'wd:Q_', wd.Q('_').iri.value)))
        # unknown prefix
        self.assert_to_markdown(
            Item('x'), self.md_sexp('Item', self.md_link('x', 'http://x')))

    def test_property_to_markdown(self):
        # known prefix: know label
        self.assert_to_markdown(
            wd.mass, self.md_sexp('Property', self.md_link(
                'mass', wd.mass.iri.value)))
        # known prefix: unknown label
        self.assert_to_markdown(
            wd.P('_'), self.md_sexp('Property', self.md_link(
                'wd:P_', wd.P('_').iri.value)))
        # unknown prefix
        self.assert_to_markdown(
            Property('x'), self.md_sexp('Property', self.md_link(
                'x', 'http://x')))

    def test_iri_to_markdown(self):
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
            self.md_link('prefix/x', 'http://prefix/x'))
        self.assert_to_markdown(
            IRI('x'),
            self.md_link('x', 'http://x'))

    def test_text_to_markdown(self):
        self.assert_to_markdown(Text('abc'), '"abc"@en')
        self.assert_to_markdown(Text('abc', 'fr'), '"abc"@fr')
        # escape
        self.assert_to_markdown(Text('_', 'pt'), r'"\_"@pt')

    def test_string_to_markdown(self):
        self.assert_to_markdown(String('abc'), '"abc"')
        # escape
        self.assert_to_markdown(String('_'), r'"\_"')
        self.assert_to_markdown(String('*'), r'"\*"')
        self.assert_to_markdown(String('`'), r'"\`"')
        self.assert_to_markdown(String('[]'), r'"\[]"')

    def test_quantity_to_markdown(self):
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

    def test_time_to_markdown(self):
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

    def test_snak_to_markdown(self):
        self.assert_to_markdown(
            wd.mass(Quantity(0)),
            self.md_sexp('ValueSnak', wd.mass, Quantity(0)))
        self.assert_to_markdown(
            SomeValueSnak(wd.mass),
            self.md_sexp('SomeValueSnak', wd.mass))
        self.assert_to_markdown(
            NoValueSnak(wd.mass),
            self.md_sexp('NoValueSnak', wd.mass))

    def test_statement_to_markdown(self):
        self.assert_to_markdown(
            wd.mass(wd.benzene, Quantity(0)),
            self.md_sexp('Statement', wd.benzene, wd.mass(Quantity(0))))

    def test_annotation_record_to_markdown(self):
        annots = AnnotationRecord([], [], Normal)
        self.assert_to_markdown(annots, '''\
(**AnnotationRecord**
- (**SnakSet**)
- (**ReferenceRecordSet**)
- **NormalRank**)''')
        annots = AnnotationRecord([NoValueSnak(Property('p'))], [], Normal)
        self.assert_to_markdown(annots, '''\
(**AnnotationRecord**
- (**SnakSet**
  - (**NoValueSnak** (**Property** [p](http://p))))
- (**ReferenceRecordSet**)
- **NormalRank**)''')
        annots = AnnotationRecord(
            [NoValueSnak(Property('p')),
             cast(ValueSnak, Property('q')(IRI('x')))],
            [ReferenceRecord(NoValueSnak(Property('q'))),
             ReferenceRecord(SomeValueSnak(Property('q')))],
            Deprecated)
        self.assert_to_markdown(annots, '''\
(**AnnotationRecord**
- (**SnakSet**
  - (**NoValueSnak** (**Property** [p](http://p)))
  - (**ValueSnak** (**Property** [q](http://q)) [x](http://x)))
- (**ReferenceRecordSet**
  - (**ReferenceRecord**
    - (**NoValueSnak** (**Property** [q](http://q))))
  - (**ReferenceRecord**
    - (**SomeValueSnak** (**Property** [q](http://q)))))
- **DeprecatedRank**)''')

    def test_rank_to_markdown(self):
        self.assert_to_markdown(Preferred, self.md_sexp('PreferredRank'))
        self.assert_to_markdown(Normal, self.md_sexp('NormalRank'))
        self.assert_to_markdown(Deprecated, self.md_sexp('DeprecatedRank'))

    def test_reference_record_to_markdown(self):
        ref = ReferenceRecord()
        self.assert_to_markdown(ref, '(**ReferenceRecord**)')
        ref = ReferenceRecord(ValueSnak(wd.mass, wd.benzene))
        self.assert_to_markdown(ref, '''\
(**ReferenceRecord**
- (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) (**Item** [benzene](http://www.wikidata.org/entity/Q2270))))''')  # noqa: E501
        ref = ReferenceRecord(
            cast(ValueSnak, wd.canonical_SMILES(String('ABC'))),
            cast(ValueSnak, wd.country(wd.Brazil)),
            cast(ValueSnak, wd.mass(Quantity(0))))
        self.assert_to_markdown(ref, '''\
(**ReferenceRecord**
- (**ValueSnak** (**Property** [country](http://www.wikidata.org/entity/P17)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))
- (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) (**Quantity** 0))
- (**ValueSnak** (**Property** [canonical SMILES](http://www.wikidata.org/entity/P233)) "ABC"))''')  # noqa: E501

    def test_item_descriptor_to_markdown(self):
        desc = ItemDescriptor()
        self.assert_to_markdown(desc, '''\
(**ItemDescriptor**
- *no label*
- *no aliases*
- *no description*)''')
        desc = ItemDescriptor(
            Text("rótulo", 'pt'),
            [Text('outro nome', 'pt'), Text('sinônimo', 'pt')],
            Text('descrição', 'pt'))
        self.assert_to_markdown(desc, '''\
(**ItemDescriptor**
- "rótulo"@pt
- (**TextSet**
  - "outro nome"@pt
  - "sinônimo"@pt)
- "descrição"@pt)''')

    def test_fingerprint_to_markdown(self):
        fp = Fingerprint(Quantity(0))
        self.assert_to_markdown(
            fp, self.md_sexp('Fingerprint', Quantity(0)))
        fp = PropertyFingerprint([])
        self.assert_to_markdown(fp, '''\
(**PropertyFingerprint** (**SnakSet**))''')
        fp = EntityFingerprint([
            cast(ValueSnak, wd.mass(Quantity(0))),
            cast(ValueSnak, wd.country(wd.Brazil))])

        self.assert_to_markdown(
            fp, '''\
(**EntityFingerprint** (**SnakSet**
  - (**ValueSnak** (**Property** [country](http://www.wikidata.org/entity/P17)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))
  - (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) (**Quantity** 0))))''')  # noqa: E501

    def test_filter_pattern_to_markdown(self):
        self.assert_to_markdown(Filter(), '''\
(**Filter**
- *any entity*
- *any property*
- *any value*
- `0b111`)''')
        pat = Filter(wd.benzene)
        self.assert_to_markdown(pat, '''\
(**Filter**
- (**EntityFingerprint** (**Item** [benzene](http://www.wikidata.org/entity/Q2270)))
- *any property*
- *any value*
- `0b111`)''')  # noqa: E501
        pat = Filter(
            None,
            None,
            [cast(ValueSnak, wd.country(wd.Brazil)),
             NoValueSnak(wd.date_of_birth)],
            Filter.NO_VALUE_SNAK)
        self.assert_to_markdown(
            pat, '''\
(**Filter**
- *any entity*
- *any property*
- (**Fingerprint** (**SnakSet**
    - (**NoValueSnak** (**Property** [date of birth](http://www.wikidata.org/entity/P569)))
    - (**ValueSnak** (**Property** [country](http://www.wikidata.org/entity/P17)) (**Item** [Brazil](http://www.wikidata.org/entity/Q155)))))
- `0b100`)''')  # noqa: E501

    def test_snak_set_to_markdown(self):
        s = SnakSet()
        self.assert_to_markdown(s, '(**SnakSet**)')
        s = SnakSet(cast(ValueSnak, wd.mass(wd.benzene)))
        self.assert_to_markdown(s, '''\
(**SnakSet**
- (**ValueSnak** (**Property** [mass](http://www.wikidata.org/entity/P2067)) (**Item** [benzene](http://www.wikidata.org/entity/Q2270))))''')  # noqa: E501


if __name__ == '__main__':
    TestCodecMarkdown.main()
