# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from collections.abc import Collection, Iterable, Mapping
from typing import Any, cast, NoReturn, Optional, Union

from rdflib.paths import Path
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.parserutils import CompValue
from rdflib.term import Identifier as Id
from rdflib.term import Literal, URIRef, Variable

from .. import namespace as NS
from ..error import ShouldNotGetHere
from ..model import (
    EntityFingerprint,
    FilterPattern,
    Fingerprint,
    Property,
    PropertyFingerprint,
    Snak,
    Value,
    ValueSnak,
)
from ..model.kif_object import Decoder, DecoderError, Object


class SPARQL_Decoder(
        Decoder, format='sparql', description='SPARQL decoder'):
    """SPARQL decoder."""

    _namespace: Optional[Mapping[str, Any]]

    @classmethod
    def _error_bad_query(
            self,
            query: str,
            line: int,
            column: int,
            details: str
    ) -> DecoderError:
        return DecoderError(f'''\
bad query:
{query}
At line {line}, column {column}:
{details}''')

    @classmethod
    def _error_unsupported_bgp(
            self,
            details: str
    ) -> DecoderError:
        return DecoderError(f'unsupported BGP: {details}')

    @classmethod
    def _error_unsupported_expression(
            self,
            details: str,
    ) -> DecoderError:
        return DecoderError(f'unsupported expression: {details}')

    def __init__(self):
        self._namespace = dict(NS._DEFAULT_NSM.namespaces())

    def decode(self, s: str) -> Union[Object, NoReturn]:
        from pyparsing.exceptions import ParseException
        try:
            query = prepareQuery(s, initNs=self._namespace)
        except ParseException as err:
            raise self._error_bad_query(
                s, err.lineno, err.column, err.explain())
        fpmap: dict[Variable, list[Snak]] = dict()
        snmap: dict[ValueSnak, tuple[Id, Id]] = dict()
        subj: Optional[Id] = None
        pred: Optional[Id] = None
        obj: Optional[Id] = None
        for (s, p, o) in self._get_bgp_triples(query.algebra):
            if (isinstance(s, Variable)
                and isinstance(p, URIRef)
                    and isinstance(o, (URIRef, Literal))):
                if s not in fpmap:
                    fpmap[s] = list()
                assert isinstance(p, URIRef)
                sp = self._uriref_to_property(p)
                if isinstance(o, URIRef):
                    sv: Value = self._uriref_to_value(o)
                elif isinstance(o, Literal):
                    sv = self._literal_to_value(o)
                else:
                    raise ShouldNotGetHere
                snak = ValueSnak(sp, sv)
                snmap[snak] = (p, o)
                fpmap[s].append(snak)
            elif isinstance(p, Path):
                continue        # skip: property path
            else:
                subj = s
                if not isinstance(s, (URIRef, Variable)):
                    raise self._error_unsupported_bgp(
                        f"bad subject ({s})")
                pred = p
                if not isinstance(s, (URIRef, Variable)):
                    raise self._error_unsupported_bgp(
                        f"bad predicate ({p})")
                obj = o
                if not isinstance(s, (URIRef, Literal, Variable)):
                    raise self._error_unsupported_bgp(
                        f"bad object ({o})")
        if subj is None and pred is None and obj is None:
            if not fpmap:
                return FilterPattern(None, None, None, 0)
            else:
                assert len(fpmap) == 1
                snaks = list(fpmap.values())[0]
                assert len(snaks) > 0
                if len(snaks) > 1:
                    subj = list(fpmap.keys())[0]
                else:
                    ###
                    # If it is a single triple, do the right thing, i.e.,
                    # return the pattern FilterPattern(s, p, o).
                    ###
                    subj = None
                    pred, obj = snmap[cast(ValueSnak, snaks[0])]
        return FilterPattern(
            self._subject_to_entity_fingerprint(subj, fpmap),
            self._predicate_to_property_fingerprint(pred, fpmap),
            self._object_to_fingerprint(obj, fpmap)
        )

    def _get_bgp_triples(
            self,
            part: CompValue
    ) -> Iterable[tuple[Id, Id, Id]]:
        if part.name == 'BGP':
            return part.triples
        elif part.name == 'Project':
            return self._get_bgp_triples(part.p)
        elif part.name == 'SelectQuery':
            return self._get_bgp_triples(part.p)
        elif part.name == 'Slice':
            return self._get_bgp_triples(part.p)
        else:
            raise self._error_unsupported_expression(part.name)

    def _uriref_to_value(
            self,
            uri: URIRef,
            property_prefixes: Collection[NS.T_NS] = [NS.WD, NS.WDT]
    ) -> Value:
        return Value._from_rdflib(uri, property_prefixes=property_prefixes)

    def _uriref_to_property(self, uri: URIRef) -> Property:
        val = self._uriref_to_value(uri)
        if isinstance(val, Property):
            return cast(Property, val)
        else:
            raise self._error_unsupported_bgp(
                f"expected Wikidata property, got '{uri}'")

    def _literal_to_value(self, literal: Literal) -> Value:
        return Value._from_rdflib(literal)

    def _subject_to_entity_fingerprint(
            self,
            subj: Optional[Id],
            fpmap: dict[Variable, list[Snak]]
    ) -> Optional[EntityFingerprint]:
        if subj is None:
            return None
        elif isinstance(subj, URIRef):
            return EntityFingerprint(self._uriref_to_value(subj))
        elif isinstance(subj, Variable):
            if subj in fpmap:
                return EntityFingerprint(fpmap[subj])
            else:
                return None
        else:
            raise ShouldNotGetHere

    def _predicate_to_property_fingerprint(
            self,
            pred: Optional[Id],
            fpmap: dict[Variable, list[Snak]]
    ) -> Optional[PropertyFingerprint]:
        if pred is None:
            return None
        elif isinstance(pred, URIRef):
            return PropertyFingerprint(self._uriref_to_property(pred))
        elif isinstance(pred, Variable):
            if pred in fpmap:
                return PropertyFingerprint(fpmap[pred])
            else:
                return None
        else:
            raise ShouldNotGetHere

    def _object_to_fingerprint(
            self,
            obj: Optional[Id],
            fpmap: dict[Variable, list[Snak]]
    ) -> Optional[Fingerprint]:
        if obj is None:
            return None
        elif isinstance(obj, URIRef):
            return Fingerprint(self._uriref_to_value(obj))
        elif isinstance(obj, Literal):
            return Fingerprint(self._literal_to_value(obj))
        elif isinstance(obj, Variable):
            if obj in fpmap:
                return Fingerprint(fpmap[obj])
            else:
                return None
        else:
            raise ShouldNotGetHere
