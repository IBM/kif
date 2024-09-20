# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from kif_lib import (
    Entity,
    ExternalId,
    Filter,
    Item,
    NoValueSnak,
    Property,
    Quantity,
    Snak,
    SomeValueSnak,
    Statement,
    Store,
    String,
    Value,
    Variable,
    Variables,
)
from kif_lib.model import (
    TEntity,
    TFingerprint,
    TValue,
    VEntity,
    VSnak,
    VStatement,
    VValue,
)
from kif_lib.typing import Any, Callable, Iterable, Mapping, TypeAlias, Union
from kif_lib.vocabulary import pc, wd

from ...tests import PubChemStoreTestCase

TFingerprintPair: TypeAlias = tuple[TFingerprint, TFingerprint]
TEntityValue: TypeAlias = tuple[TEntity, TValue]
VEntityValue: TypeAlias = tuple[VEntity, VValue]

x, y, z = Variables('x', 'y', 'z')


class Test(PubChemStoreTestCase):

    def _test_filter(
            self,
            empty: Iterable[Filter] = (),
            equals: Iterable[tuple[Filter, Statement]] = (),
            contains: Iterable[tuple[Filter, Iterable[Statement]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        kb = kb or self.new_Store()
        fr = (lambda x: kb.filter(filter=x, limit=limit))
        self.assert_it(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), t[1]), equals),
            contains=map(lambda t: (fr(t[0]), t[1]), contains))

    def _test_filter_matches(
            self,
            filter: Filter,
            pattern: VStatement,
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        kb = kb or self.new_Store()
        limit = limit if limit is not None else kb.page_size
        for stmt in kb.filter(filter=filter, limit=limit):
            self.assertIsNotNone(pattern.match(stmt))

    def _test_filter_with_fixed_subject(
            self,
            subject: Entity,
            empty: Iterable[TFingerprintPair] = (),
            equals: Iterable[tuple[TFingerprintPair, Snak]] = (),
            contains: Iterable[tuple[TFingerprintPair, Iterable[Snak]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        fr = (lambda p: Filter(subject, *p))
        st = (lambda s: Statement(subject, s))
        self._test_filter(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), st(t[1])), equals),
            contains=map(lambda t: (fr(t[0]), map(st, t[1])), contains),
            kb=kb,
            limit=limit)

    def _test_filter_with_fixed_property(
            self,
            property: Property,
            empty: Iterable[TFingerprintPair] = (),
            equals: Iterable[tuple[TFingerprintPair, TEntityValue]] = (),
            contains: Iterable[
                tuple[TFingerprintPair, Iterable[TEntityValue]]] = (),
            kb: Store | None = None,
            limit: int | None = None
    ) -> None:
        fr = (lambda p: Filter(p[0], property, p[1]))
        st = (lambda t: Statement(t[0], property(t[1])))
        self._test_filter(
            empty=map(fr, empty),
            equals=map(lambda t: (fr(t[0]), st(t[1])), equals),
            contains=map(lambda t: (fr(t[0]), map(st, t[1])), contains),
            kb=kb,
            limit=limit)

    def test_empty(self) -> None:
        self._test_filter(
            empty=[
                Filter(0),
                Filter(None, 0),
                Filter(None, None, 0, snak_mask=Filter.SOME_VALUE_SNAK),
            ])

    def test_subject_CID(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.CID(241),
            contains=[
                ((None, None), [  # FF
                    pc.Isotope_Atom_Count(0),
                    wd.canonical_SMILES('C1=CC=CC=C1'),
                    wd.mass('78.11'@wd.gram_per_mole),
                    wd.PubChem_CID('241'),
                ]),
            ])

    def test_subject_Isotope_Atom_Count(self) -> None:
        self._test_filter_with_fixed_subject(
            subject=pc.Isotope_Atom_Count,
            equals=[
                ((None, None),  # FF
                 wd.instance_of(wd.Wikidata_property_related_to_chemistry)),
            ])

    def test_property_canonical_SMILES(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.canonical_SMILES,
            empty=[
                (pc.CID(241), 'x'),  # VV
                (wd.benzene, 'x'),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (None, 'x'),    # FV
            ],
            equals=[
                ((pc.CID(241), 'C1=CC=CC=C1'),  # VV
                 (pc.CID(241), 'C1=CC=CC=C1')),
                ((pc.CID(241), None),  # VF
                 (pc.CID(241), 'C1=CC=CC=C1')),
            ],
            contains=[
                ((None, 'C1=CC=CC=C1'), [  # FV
                    (pc.CID(241), 'C1=CC=CC=C1'),
                    (pc.CID(12196274), 'C1=CC=CC=C1'),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.canonical_SMILES, None),
            wd.canonical_SMILES(Item(x), String(y)))

    def test_property_has_part(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.has_part,
            empty=[
                (wd.benzene, wd.caffeine),  # VV
                (pc.Isotope_Atom_Count, pc.CID(421)),
                (pc.CID(241), pc.CID(340032)),
                (wd.benzene, None),  # VF
                (pc.Isotope_Atom_Count, None),
                (pc.CID(241), None),
                (None, wd.benzene),  # FV
                (None, pc.CID(340032)),
            ],
            equals=[
                ((pc.CID(340032), None),  # VF
                 (pc.CID(340032), pc.CID(241))),
            ],
            contains=[
                ((None, pc.CID(421)), [  # FV
                    (pc.CID(10236840), pc.CID(421)),
                ]),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.has_part, None),
            wd.has_part(Item(x), Item(y)))

    def test_instance_of(self) -> None:
        self._test_filter_with_fixed_property(
            property=wd.instance_of,
            empty=[
                (wd.chemical_formula,  # VV
                 wd.Wikidata_property_related_to_medicine),
                (wd.benzene, None),  # VF
                (pc.CID(421), None),
                (None, wd.benzene),  # FV
            ],
            equals=[
                ((pc.Isotope_Atom_Count,  # VV
                  wd.Wikidata_property_related_to_chemistry),
                 (pc.Isotope_Atom_Count,
                  wd.Wikidata_property_related_to_chemistry)),
                ((pc.Isotope_Atom_Count, None),  # VF
                 (pc.Isotope_Atom_Count,
                  wd.Wikidata_property_related_to_chemistry)),
                ((None, wd.Wikidata_property_related_to_chemistry),  # FV
                 (pc.Isotope_Atom_Count,
                  wd.Wikidata_property_related_to_chemistry)),
            ])
        self._test_filter_matches(  # FF
            Filter(None, wd.instance_of, None),
            wd.instance_of(x, Item(y)))

    def test_V_Isotope_Atom_Count_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, pc.Isotope_Atom_Count))
        # success
        it = kb.filter(pc.CID(241), pc.Isotope_Atom_Count)
        self.assert_it_equals(it, pc.Isotope_Atom_Count(pc.CID(241), 0))

    def test_F_Isotope_Atom_Count_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(
            kb.filter(None, pc.Isotope_Atom_Count, 201@wd.kilogram))
        # success
        it = kb.filter(snak=pc.Isotope_Atom_Count(201))
        self.assert_it_contains(
            it, pc.Isotope_Atom_Count(pc.CID(160456303), 201))

    def test_V_mass_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(
            wd.benzene, wd.mass, Quantity('78.11', wd.gram_per_mole)))
        self.assert_it_equals(kb.filter(
            pc.CID(241), wd.mass, Quantity('78.10', wd.gram_per_mole)))
        # success
        it = kb.filter(
            pc.CID(241), wd.mass, Quantity('78.11', wd.gram_per_mole))
        self.assert_it_equals(
            it, wd.mass(pc.CID(241), Quantity('78.11', wd.gram_per_mole)))

    def test_V_mass_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.mass))
        self.assert_it_empty(kb.filter(pc.Isotope_Atom_Count, wd.mass))
        # success
        it = kb.filter(pc.CID(241), wd.mass)
        self.assert_it_equals(
            it, wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole))

    def test_F_mass_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity('78.11', wd.kilogram)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity('78.11', wd.gram_per_mole, 1)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity(
                '78.11', wd.gram_per_mole, None, 80)))
        self.assert_it_empty(
            kb.filter(None, wd.mass, Quantity(10**8, wd.gram_per_mole)))
        # success
        it = kb.filter(None, wd.mass, Quantity('78.11', wd.gram_per_mole))
        self.assert_it_contains(
            it, wd.mass(pc.CID(241), '78.11'@wd.gram_per_mole))

    def test_V_PubChem_CID_F(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(wd.benzene, wd.PubChem_CID))
        self.assert_it_empty(kb.filter(pc.Isotope_Atom_Count, wd.PubChem_CID))
        # success
        it = kb.filter(pc.CID(241), wd.PubChem_CID)
        self.assert_it_equals(it, wd.PubChem_CID(pc.CID(241), '241'))

    def test_F_PubChem_CID_V(self) -> None:
        kb = self.new_Store()
        # failure
        self.assert_it_empty(kb.filter(None, wd.PubChem_CID, String('241')))
        self.assert_it_empty(
            kb.filter(None, wd.PubChem_CID, ExternalId('abc')))
        # success
        it = kb.filter(None, wd.PubChem_CID, ExternalId('241'))
        self.assert_it_equals(it, wd.PubChem_CID(pc.CID(241), '241'))


if __name__ == '__main__':
    Test.main()
