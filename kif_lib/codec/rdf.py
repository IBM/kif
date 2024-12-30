# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..model import AnnotatedStatement, Entity, Property, Snak, Statement
from ..model.kif_object import Encoder, Object
from ..namespace import RDF, WIKIBASE
from ..rdflib import BNode, Literal, URIRef
from ..typing import cast, Iterator, override, TypeAlias

TSubject: TypeAlias = URIRef | BNode
TPredicate: TypeAlias = URIRef
TObject: TypeAlias = URIRef | BNode | Literal
TTriple: TypeAlias = tuple[TSubject, TPredicate, TObject]


class RDF_Encoder(
        Encoder,
        format='rdf',
        description='RDF encoder'
):
    """RDF encoder."""

    @override
    def iterencode(self, input: Object) -> Iterator[str]:
        if isinstance(input, Statement):
            if isinstance(input, AnnotatedStatement):
                stmt: AnnotatedStatement = input
            else:
                stmt = input.annotate()
            yield from self._iterencode_annotated_statement(stmt)
        else:
            raise self._error(f'cannot encode to RDF: {input}')

    def _iterencode_annotated_statement(
            self,
            stmt: AnnotatedStatement
    ) -> Iterator[str]:
        yield from self._iterencode_subject(stmt.subject)
        yield from self._iterencode_snak(stmt.snak)

    def _iterencode_subject(self, entity: Entity) -> Iterator[str]:
        yield from self._tr(
            (cast(URIRef, entity._to_rdflib()),
             WIKIBASE.sitelinks, Literal(0)))

    def _iterencode_snak(self, snak: Snak) -> Iterator[str]:
        yield from self._iterencode_property(snak.property)

    def _iterencode_property(
            self,
            property: Property
    ) -> Iterator[str]:
        prop = cast(URIRef, property._to_rdflib())
        yield from self._tr((prop, RDF.type, WIKIBASE.Property))

    def _tr(self, tr: TTriple, *trs: TTriple) -> Iterator[str]:
        for (s, p, o) in itertools.chain((tr,), trs):
            yield s.n3()
            yield ' '
            yield p.n3()
            yield ' '
            yield o.n3()
            yield ' .\n'
