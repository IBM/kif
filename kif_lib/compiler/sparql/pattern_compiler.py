# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from ... import itertools
from ... import namespace as NS
from ...model import (
    DatatypeVariable,
    Entity,
    EntityTemplate,
    EntityVariable,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    KIF_Object,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnakVariable,
    Pattern,
    Property,
    PropertyTemplate,
    PropertyVariable,
    QuantityVariable,
    SnakVariable,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    StringVariable,
    TemplatePattern,
    TimeVariable,
    TPattern,
    ValueSnakVariable,
    ValueVariable,
    Variable,
    VariablePattern,
)
from ...typing import cast, Iterator, Optional, override, Self, TypeVar
from .builder import Query
from .compiler import SPARQL_Compiler
from .substitution import Substitution

T = TypeVar('T')
V_URI1 = TypeVar('V_URI1', bound=Query.V_URI)
V_URI2 = TypeVar('V_URI2', bound=Query.V_URI)


class SPARQL_PatternCompiler(SPARQL_Compiler):
    """SPARQL pattern compiler."""

    __slots__ = (
        '_pattern',
        '_theta',
    )

    #: The source pattern.
    _pattern: Pattern

    #: The compiled substitution.
    _theta: Substitution

    def __init__(
            self,
            pattern: TPattern,
            flags: Optional['SPARQL_PatternCompiler.Flags'] = None
    ):
        super().__init__(flags)
        self._pattern = Pattern.check(pattern, type(self), 'pattern', 1)
        self._theta = Substitution()

    @property
    def pattern(self) -> Pattern:
        """The source pattern."""
        return self.get_pattern()

    def get_pattern(self) -> Pattern:
        """Gets the source pattern.

        Returns:
           Pattern.
        """
        return self._pattern

    @property
    def theta(self) -> Substitution:
        """The compiled substitution."""
        return self.get_theta()

    def get_theta(self) -> Substitution:
        """Gets the compiled substitution.

        Returns:
           Substitution.
        """
        return self._theta

    def _theta_add(self, var: Variable, v: T) -> T:
        if self.has_flags(self.DEBUG):
            self._q.comments()(f'{var} := {Substitution._dump_value(v)}')
        return self._theta.add(var, v)

    def _theta_add_default(
            self,
            var: Variable,
            value: Optional[KIF_Object]
    ) -> Variable:
        return self._theta.add_default(var, value)

    def _fresh_variable(self, variable_class: type[Variable]) -> Variable:
        return variable_class(str(self._fresh_qvar()))

    def _fresh_variables(
            self,
            variable_class: type[Variable],
            n: int
    ) -> Iterator[Variable]:
        return map(
            lambda qvar: variable_class(str(qvar)), self._fresh_qvars(n))

    def _fresh_datatype_variable(self) -> DatatypeVariable:
        return cast(DatatypeVariable, self._fresh_variable(DatatypeVariable))

    def _fresh_value_variable(self) -> ValueVariable:
        return cast(ValueVariable, self._fresh_variable(ValueVariable))

    def _fresh_entity_variable(self) -> EntityVariable:
        return cast(EntityVariable, self._fresh_variable(EntityVariable))

    def _fresh_item_variable(self) -> ItemVariable:
        return cast(ItemVariable, self._fresh_variable(ItemVariable))

    def _fresh_property_variable(self) -> PropertyVariable:
        return cast(PropertyVariable, self._fresh_variable(PropertyVariable))

    def _fresh_lexeme_variable(self) -> LexemeVariable:
        return cast(LexemeVariable, self._fresh_variable(LexemeVariable))

    def _fresh_iri_variable(self) -> IRI_Variable:
        return cast(IRI_Variable, self._fresh_variable(IRI_Variable))

    def _fresh_string_variable(self) -> StringVariable:
        return cast(StringVariable, self._fresh_variable(StringVariable))

    def _fresh_quantity_variable(self) -> QuantityVariable:
        return cast(QuantityVariable, self._fresh_variable(QuantityVariable))

    def _fresh_time_variable(self) -> TimeVariable:
        return cast(TimeVariable, self._fresh_variable(TimeVariable))

    def _fresh_snak_variable(self) -> SnakVariable:
        return cast(SnakVariable, self._fresh_variable(SnakVariable))

    def _fresh_value_snak_variable(self) -> ValueSnakVariable:
        return cast(ValueSnakVariable, self._fresh_variable(
            ValueSnakVariable))

    def _fresh_some_value_snak_variable(self) -> SomeValueSnakVariable:
        return cast(SomeValueSnakVariable, self._fresh_variable(
            SomeValueSnakVariable))

    def _fresh_no_value_snak_variable(self) -> NoValueSnakVariable:
        return cast(NoValueSnakVariable, self._fresh_variable(
            NoValueSnakVariable))

    def _fresh_statement_variable(self) -> StatementVariable:
        return cast(StatementVariable, self._fresh_variable(StatementVariable))

    def _as_qvar(self, var: Variable) -> Query.Variable:
        return self._qvar(var.name)

    def _as_qvars(
            self,
            var: Variable,
            *vars: Variable
    ) -> Iterator[Query.Variable]:
        return map(self._as_qvar, itertools.chain((var,), vars))

    @override
    def compile(self) -> Self:
        self._push_pattern(self.pattern)
        return self

    def _push_pattern(self, pattern: Pattern):
        if isinstance(pattern, TemplatePattern):
            if isinstance(pattern.template, StatementTemplate):
                self._push_statement_template(pattern.template)
            else:
                raise self._cannot_compile_error(pattern)
        elif isinstance(pattern, VariablePattern):
            if isinstance(pattern.variable, StatementVariable):
                self._push_statement_variable(pattern.variable)
            else:
                raise self._cannot_compile_error(pattern)
        else:
            raise self._should_not_get_here()

    def _push_statement(self, obj: Statement):
        raise NotImplementedError

    def _push_statement_template(self, tpl: StatementTemplate):
        if isinstance(tpl.subject, Entity):
            self._push_entity(tpl.subject)
        elif isinstance(tpl.subject, EntityTemplate):
            self._push_entity_template(tpl.subject)
        elif isinstance(tpl.subject, EntityVariable):
            self._push_entity_variable(tpl.subject)
        else:
            raise self._should_not_get_here()

    def _push_statement_variable(self, var: StatementVariable):
        self._push_statement_template(
            self._theta_add(
                var,
                StatementTemplate(
                    self._fresh_entity_variable(),
                    self._fresh_snak_variable())))

    def _push_entity(
            self,
            obj: Entity
    ) -> tuple[Query.URI, Optional[Query.V_URI]]:
        if isinstance(obj, Item):
            return self._push_item(obj), None
        elif isinstance(obj, Property):
            return self._push_property(obj)
        elif isinstance(obj, Lexeme):
            return self._push_lexeme(obj), None
        else:
            raise self._should_not_get_here()

    def _push_entity_template(self, tpl: EntityTemplate) -> Query.Variable:
        if isinstance(tpl, ItemTemplate):
            return self._push_item_template(tpl)
        elif isinstance(tpl, PropertyTemplate):
            raise NotImplementedError
        elif isinstance(tpl, LexemeTemplate):
            return self._push_lexeme_template(tpl)
        else:
            raise self._should_not_get_here()

    def _push_entity_variable(self, var: EntityVariable) -> Query.Variable:
        if isinstance(var, ItemVariable):
            return self._push_item_variable(var)
        elif isinstance(var, PropertyVariable):
            raise NotImplementedError
        elif isinstance(var, LexemeVariable):
            return self._push_lexeme_variable(var)
        else:
            raise NotImplementedError

    def _push_item(self, obj: Item) -> Query.URI:
        return self._do_push_item(self._q._mk_uri(obj.iri.content))

    def _push_item_template(self, tpl: ItemTemplate) -> Query.Variable:
        if isinstance(tpl.iri, IRI_Template):
            assert isinstance(tpl.iri.content, StringVariable)
            return self._do_push_item(self._theta_add(
                tpl.iri.content, self._as_qvar(tpl.iri.content)))
        elif isinstance(tpl.iri, IRI_Variable):
            return self._do_push_item(self._theta_add(
                tpl.iri, self._as_qvar(tpl.iri)))
        else:
            raise self._should_not_get_here()

    def _push_item_variable(self, var: ItemVariable) -> Query.Variable:
        return self._push_item_template(
            self._theta_add(var, ItemTemplate(self._fresh_iri_variable())))

    def _do_push_item(self, v_item: V_URI1) -> V_URI1:
        self._q.triples()((v_item, NS.WIKIBASE.sitelinks, self._q.bnode()))
        return v_item

    def _push_property(self, obj: Property) -> tuple[Query.URI, Query.V_URI]:
        return self._do_push_property(
            self._q._mk_uri(obj.iri.content),
            obj.range._to_rdflib() if obj.range is not None
            else self._fresh_qvar())

    def _do_push_property(
            self,
            v_property: V_URI1,
            v_datatype: V_URI2
    ) -> tuple[V_URI1, V_URI2]:
        self._q.triples()(
            (v_property, NS.RDF.type, NS.WIKIBASE.Property),
            (v_property, NS.WIKIBASE.propertyType, v_datatype))
        return v_property, v_datatype

    def _push_lexeme(self, obj: Lexeme) -> Query.URI:
        return self._do_push_lexeme(self._q._mk_uri(obj.iri.content))

    def _push_lexeme_template(self, tpl: LexemeTemplate) -> Query.Variable:
        if isinstance(tpl.iri, IRI_Template):
            assert isinstance(tpl.iri.content, StringVariable)
            return self._do_push_lexeme(self._theta_add(
                tpl.iri.content, self._as_qvar(tpl.iri.content)))
        elif isinstance(tpl.iri, IRI_Variable):
            return self._do_push_lexeme(self._theta_add(
                tpl.iri, self._as_qvar(tpl.iri)))
        else:
            raise self._should_not_get_here()

    def _push_lexeme_variable(self, var: LexemeVariable) -> Query.Variable:
        return self._push_lexeme_template(
            self._theta_add(var, LexemeTemplate(self._fresh_iri_variable())))

    def _do_push_lexeme(self, v_lexeme: V_URI1) -> V_URI1:
        self._q.triples()((v_lexeme, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        return v_lexeme
