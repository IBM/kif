# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import namespace as NS
from ...error import ShouldNotGetHere
from ...model import (
    EntityVariable,
    ItemVariable,
    KIF_Object,
    LexemeVariable,
    PropertyVariable,
    SnakVariable,
    SomeValueSnakTemplate,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
)
from .builder import Query, SelectQuery
from .builder import Variable as QueryVariable


class Converter(SelectQuery):

    subject: str
    property: str
    value: str

    def __init__(
            self,
            subject: str = 'subject',
            property: str = 'property',
            value: str = 'value',
            wds: str = 'wds',
            p: str = 'p',
            rank: str = 'rank',
    ):
        super().__init__()
        self.subject = subject
        self.property = property
        self.value = value
        self.wds = wds
        self.p = p
        self.rank = rank

    def convert(self, obj: KIF_Object) -> Query:
        if isinstance(obj, Statement):
            raise NotImplementedError
        elif isinstance(obj, StatementTemplate):
            raise NotImplementedError
        elif isinstance(obj, StatementVariable):
            self._push_statement_variable(obj)
        elif isinstance(obj, SnakVariable):
            if isinstance(obj, SomeValueSnakVariable):
                self._push_some_value_snak_variable(obj)
            else:
                raise NotImplementedError
        elif isinstance(obj, EntityVariable):
            if isinstance(obj, ItemVariable):
                self._push_item_variable(obj)
            elif isinstance(obj, PropertyVariable):
                self._push_property_variable(obj)
            elif isinstance(obj, LexemeVariable):
                self._push_lexeme_variable(obj)
            else:
                self._push_entity_variable(obj)
        else:
            raise ShouldNotGetHere
        return self

    def _push_statement_variable(self, obj: StatementVariable):
        subj = self._push_entity_variable(EntityVariable(self.subject))
        prop = self._push_property_variable(PropertyVariable(self.property))
        p, wds = self.vars(f'{prop}_p', obj.name)
        with self.group():
            self.triples(
                (prop, NS.WIKIBASE.claim, p),
                (subj, p, wds),
                (wds, NS.WIKIBASE.rank, self.bnode()))

    def _push_some_value_snak_template(
            self,
            obj: SomeValueSnakTemplate
    ) -> QueryVariable:
        if isinstance(obj[0], PropertyVariable):
            prop = self._push_property_variable(obj[0])
        else:
            raise NotImplementedError
        with self.group():
            wdt, value = self.vars(f'{prop}_wdt', self.value)
            self.triples(
                (prop, NS.WIKIBASE.directClaim, wdt),
                (self.bnode(), wdt, value))
            self.filter(
                self.is_uri(value) & self.strstarts(
                    self.str(value), NS.WDGENID))
        return prop

    def _push_some_value_snak_variable(
            self,
            obj: SomeValueSnakVariable
    ) -> QueryVariable:
        return self._push_some_value_snak_template(
            SomeValueSnakTemplate(PropertyVariable(obj.name)))

    def _push_entity_variable(self, obj: EntityVariable) -> QueryVariable:
        with self.union():
            entity1 = self._push_item_variable(ItemVariable(obj.name))
            entity2 = self._push_property_variable(PropertyVariable(obj.name))
            entity3 = self._push_lexeme_variable(LexemeVariable(obj.name))
            assert entity1 == entity2
            assert entity2 == entity3
            return entity3

    def _push_item_variable(self, obj: ItemVariable) -> QueryVariable:
        with self.group():
            var = self.var(obj.name)
            self.triple(var, NS.SCHEMA.version, self.bnode())
            return var

    def _push_property_variable(self, obj: PropertyVariable) -> QueryVariable:
        with self.group():
            var = self.var(obj.name)
            self.triples(
                (var, NS.SCHEMA.version, self.bnode()),
                (var, NS.RDF.type, NS.WIKIBASE.Property))
            return var

    def _push_lexeme_variable(self, obj: LexemeVariable) -> QueryVariable:
        with self.group():
            var = self.var(obj.name)
            self.triples(
                (var, NS.SCHEMA.version, self.bnode()),
                (var, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
            return var
