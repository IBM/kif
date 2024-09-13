# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ... import namespace as NS
from ...model import (
    ClosedPattern,
    Datatype,
    DatatypeVariable,
    DataValue,
    DataValueVariable,
    DeepDataValue,
    DeepDataValueVariable,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    ExternalIdVariable,
    IRI,
    IRI_Template,
    IRI_Variable,
    Item,
    ItemTemplate,
    ItemVariable,
    Lexeme,
    LexemeTemplate,
    LexemeVariable,
    NoValueSnak,
    NoValueSnakVariable,
    Pattern,
    Property,
    PropertyTemplate,
    PropertyVariable,
    Quantity,
    QuantityVariable,
    ShallowDataValue,
    ShallowDataValueVariable,
    Snak,
    SnakTemplate,
    SnakVariable,
    SomeValueSnak,
    SomeValueSnakVariable,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    StringVariable,
    TemplatePattern,
    Term,
    Text,
    TextVariable,
    Time,
    TimeVariable,
    TPattern,
    Value,
    ValueSnak,
    ValueSnakVariable,
    ValueVariable,
    Variable,
    VariablePattern,
)
from ...typing import (
    cast,
    Iterator,
    override,
    Self,
    TypeAlias,
    TypedDict,
    TypeVar,
)
from .builder import Query
from .compiler import SPARQL_Compiler
from .substitution import Substitution

T = TypeVar('T')
VTerm1 = TypeVar('VTerm1', bound=Query.VTerm)
VTerm2 = TypeVar('VTerm2', bound=Query.VTerm)
V_URI1 = TypeVar('V_URI1', bound=Query.V_URI)
V_URI2 = TypeVar('V_URI2', bound=Query.V_URI)
V_URI3 = TypeVar('V_URI3', bound=Query.V_URI)

StmtCtx: TypeAlias = 'SPARQL_PatternCompiler.StatementContext'
SnakCtx: TypeAlias = 'SPARQL_PatternCompiler.SnakContext'


class SPARQL_PatternCompiler(SPARQL_Compiler):
    """SPARQL pattern compiler."""

    class StatementContext(TypedDict):
        """Context to be used when compiling statement patterns."""
        v_wds: Query.V_URI

    class SnakContext(StatementContext):
        """Context to be used when compiling snaks."""
        v_property: Query.V_URI

    @classmethod
    def _mk_stmtctx(cls, v_wds: Query.V_URI) -> StmtCtx:
        return {'v_wds': v_wds}

    @classmethod
    def _mk_snakctx(
            cls,
            v_wds: Query.V_URI,
            v_property: Query.V_URI
    ) -> SnakCtx:
        return {'v_wds': v_wds, 'v_property': v_property}

    @classmethod
    def _as_snakctx(
            cls,
            ctx: StmtCtx,
            v_property: Query.V_URI
    ) -> SnakCtx:
        return cls._mk_snakctx(ctx['v_wds'], v_property)

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
            flags: SPARQL_PatternCompiler.Flags | None = None
    ) -> None:
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
            self.q.comments()(f'{var} := {Substitution._dump_value(v)}')
        return self._theta.add(var, v)

    def _theta_add_as_qvar(self, var: Variable) -> Query.Variable:
        return self._theta_add(var, self.as_qvar(var))

    def _theta_add_default(
            self,
            var: Variable,
            value: Term | None
    ) -> Variable:
        return self._theta.add_default(var, value)

    def _fresh_variable(self, variable_class: type[Variable]) -> Variable:
        return variable_class(str(self.fresh_qvar()))

    def _fresh_variables(
            self,
            variable_class: type[Variable],
            n: int
    ) -> Iterator[Variable]:
        return map(
            lambda qvar: variable_class(str(qvar)), self.fresh_qvars(n))

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

    def _fresh_data_value_variable(self) -> DataValueVariable:
        return cast(DataValueVariable, self._fresh_variable(DataValueVariable))

    def _fresh_shallow_data_value_variable(self) -> ShallowDataValueVariable:
        return cast(ShallowDataValueVariable, self._fresh_variable(
            ShallowDataValueVariable))

    def _fresh_iri_variable(self) -> IRI_Variable:
        return cast(IRI_Variable, self._fresh_variable(IRI_Variable))

    def _fresh_text_variable(self) -> TextVariable:
        return cast(TextVariable, self._fresh_variable(TextVariable))

    def _fresh_string_variable(self) -> StringVariable:
        return cast(StringVariable, self._fresh_variable(StringVariable))

    def _fresh_external_id_variable(self) -> ExternalIdVariable:
        return cast(ExternalIdVariable, self._fresh_variable(
            ExternalIdVariable))

    def _fresh_deep_data_value_variable(self) -> DeepDataValueVariable:
        return cast(DeepDataValueVariable, self._fresh_variable(
            DeepDataValueVariable))

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

    def _as_simple_value(
            self,
            value: Value
    ) -> Query.Literal | Query.URI:
        if isinstance(value, Entity):
            return self.uri(value.iri.content)
        elif isinstance(value, IRI):
            return self.uri(value.content)
        elif isinstance(value, Text):
            return self.literal(value.content, value.language)
        elif isinstance(value, (String, ExternalId)):
            return self.literal(value.content)
        elif isinstance(value, Quantity):
            return self.literal(value.amount)
        elif isinstance(value, Time):
            return self.literal(value.time)
        else:
            raise self._should_not_get_here()

    @override
    def compile(self) -> Self:
        self._push_pattern(self.pattern)
        return self

    # -- Pattern --

    def _push_pattern(self, pattern: Pattern) -> None:
        if isinstance(pattern, ClosedPattern):
            if isinstance(pattern.object, Statement):
                self._push_statement(pattern.object)
            else:
                raise self._cannot_compile_error(pattern.object)
        elif isinstance(pattern, TemplatePattern):
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

    # -- Statement --

    def _push_statement(
            self,
            obj: Statement
    ) -> StmtCtx:
        ctx = self._mk_stmtctx(self.fresh_qvar())
        self.q.stash_begin()
        self.q.comments()('subject')
        v_subject = self._push_entity(obj.subject)
        self.q.comments()('snak')
        v_property = self._push_snak(obj.snak, ctx)
        self.q.stash_end()
        self._do_push_statement(ctx['v_wds'], v_subject, v_property)
        self.q.stash_pop()
        return ctx

    def _push_statement_template(
            self,
            tpl: StatementTemplate
    ) -> StmtCtx:
        ctx = self._mk_stmtctx(self.fresh_qvar())
        self.q.stash_begin()
        if isinstance(tpl.subject, Entity):
            v_subject = self._push_entity(tpl.subject)
        elif isinstance(tpl.subject, EntityTemplate):
            v_subject = self._push_entity_template(tpl.subject)
        elif isinstance(tpl.subject, EntityVariable):
            v_subject = self._push_entity_variable(tpl.subject)
        else:
            raise self._should_not_get_here()
        if isinstance(tpl.snak, Snak):
            v_property = self._push_snak(tpl.snak, ctx)
        elif isinstance(tpl.snak, SnakTemplate):
            raise NotImplementedError
        elif isinstance(tpl.snak, SnakVariable):
            raise NotImplementedError
        else:
            raise self._should_not_get_here()
        self.q.stash_end()
        self._do_push_statement(ctx['v_wds'], v_subject, v_property)
        self.q.stash_pop()
        return ctx

    def _push_statement_variable(self, var: StatementVariable) -> StmtCtx:
        return self._push_statement_template(
            self._theta_add(
                var,
                StatementTemplate(
                    self._fresh_entity_variable(),
                    self._fresh_snak_variable())))

    def _do_push_statement(
            self,
            v_wds: V_URI1,
            v_subject: V_URI2,
            v_property: V_URI3
    ) -> tuple[V_URI1, V_URI2, V_URI3]:
        p = self.fresh_qvar()
        self.q.triples()(
            (v_subject, p, v_wds),
            (v_property, NS.WIKIBASE.claim, p))
        best_ranked = self.has_flags(self.BEST_RANK)
        if best_ranked:
            self.q.triples()((v_wds, NS.RDF.type, NS.WIKIBASE.BestRank))
        return v_wds, v_subject, v_property

    # -- Entity --

    def _push_entity(self, obj: Entity) -> Query.V_URI:
        if isinstance(obj, Item):
            return self._push_item(obj)
        elif isinstance(obj, Property):
            return self._push_property(obj)
        elif isinstance(obj, Lexeme):
            return self._push_lexeme(obj)
        else:
            raise self._should_not_get_here()

    def _push_entity_template(self, tpl: EntityTemplate) -> Query.V_URI:
        if isinstance(tpl, ItemTemplate):
            return self._push_item_template(tpl)
        elif isinstance(tpl, PropertyTemplate):
            return self._push_property_template(tpl)
        elif isinstance(tpl, LexemeTemplate):
            return self._push_lexeme_template(tpl)
        else:
            raise self._should_not_get_here()

    def _push_entity_variable(self, var: EntityVariable) -> Query.V_URI:
        if isinstance(var, ItemVariable):
            return self._push_item_variable(var)
        elif isinstance(var, PropertyVariable):
            return self._push_property_variable(var)
        elif isinstance(var, LexemeVariable):
            return self._push_lexeme_variable(var)
        elif isinstance(var, EntityVariable):
            v_entity = self.as_qvar(var)
            with self.q.union():
                with self.q.group():  # item
                    item_iri = self._fresh_iri_variable()
                    self._theta_add(
                        ItemVariable.check(var), ItemTemplate(item_iri))
                    self._do_push_item(v_entity)
                    self.q.bind(v_entity, self._theta_add_as_qvar(item_iri))
                with self.q.group():  # property
                    datatype = self._fresh_datatype_variable()
                    datatype_iri = self._theta_add(
                        datatype, self._fresh_iri_variable())
                    property_iri = self._fresh_iri_variable()
                    self._theta_add(
                        PropertyVariable.check(var),
                        PropertyTemplate(property_iri, datatype))
                    self._do_push_property(
                        v_entity, self._theta_add_as_qvar(datatype_iri))
                    self.q.bind(
                        v_entity, self._theta_add_as_qvar(property_iri))
                with self.q.group():  # lexeme
                    lexeme_iri = self._fresh_iri_variable()
                    self._theta_add(
                        LexemeVariable.check(var),
                        LexemeTemplate(lexeme_iri))
                    self._do_push_lexeme(v_entity)
                    self.q.bind(
                        v_entity, self._theta_add_as_qvar(lexeme_iri))
            return v_entity
        else:
            raise self._should_not_get_here()

    # -- Item --

    def _push_item(self, obj: Item) -> Query.V_URI:
        return self._do_push_item(self.q._mk_uri(obj.iri.content))

    def _push_item_template(self, tpl: ItemTemplate) -> Query.V_URI:
        if isinstance(tpl.iri, IRI_Template):
            assert isinstance(tpl.iri.content, StringVariable)
            return self._do_push_item(self._theta_add_as_qvar(tpl.iri.content))
        elif isinstance(tpl.iri, IRI_Variable):
            return self._do_push_item(self._theta_add_as_qvar(tpl.iri))
        else:
            raise self._should_not_get_here()

    def _push_item_variable(self, var: ItemVariable) -> Query.V_URI:
        return self._push_item_template(
            self._theta_add(var, ItemTemplate(self._fresh_iri_variable())))

    def _do_push_item(self, v_item: V_URI1) -> V_URI1:
        self.q.triples()((v_item, NS.WIKIBASE.sitelinks, self.bnode()))
        return v_item

    # -- Property --

    def _push_property(self, obj: Property) -> Query.V_URI:
        if obj.range is None:
            return self._push_property_template(
                PropertyTemplate(obj.iri, self._fresh_datatype_variable()))
        else:
            v_property, _ = self._do_push_property(
                self.q._mk_uri(obj.iri.content), obj.range._to_rdflib())
            return v_property

    def _push_property_template(self, tpl: PropertyTemplate) -> Query.V_URI:
        if isinstance(tpl.iri, IRI):
            v_property: Query.V_URI = self.q._mk_uri(tpl.iri.content)
        elif isinstance(tpl.iri, IRI_Template):
            assert isinstance(tpl.iri.content, StringVariable)
            v_property = self._theta_add_as_qvar(tpl.iri.content)
        elif isinstance(tpl.iri, IRI_Variable):
            v_property = self._theta_add_as_qvar(tpl.iri)
        else:
            raise self._should_not_get_here()
        if tpl.range is None:
            v_datatype: Query.V_URI = self.fresh_qvar()
        elif isinstance(tpl.range, Datatype):
            v_datatype = self.q._mk_uri(tpl.range._to_rdflib())
        elif isinstance(tpl.range, DatatypeVariable):
            v_datatype = self._theta_add_as_qvar(self._theta_add(
                tpl.range, self._fresh_iri_variable()))
        else:
            raise self._should_not_get_here()
        self._do_push_property(v_property, v_datatype)
        return v_property

    def _push_property_variable(self, var: PropertyVariable) -> Query.V_URI:
        return self._push_property_template(
            self._theta_add(var, PropertyTemplate(
                self._fresh_iri_variable(),
                self._fresh_datatype_variable())))

    def _do_push_property(
            self,
            v_property: V_URI1,
            v_datatype: V_URI2
    ) -> tuple[V_URI1, V_URI2]:
        self.q.triples()(
            (v_property, NS.RDF.type, NS.WIKIBASE.Property),
            (v_property, NS.WIKIBASE.propertyType, v_datatype))
        return v_property, v_datatype

    # -- Lexeme --

    def _push_lexeme(self, obj: Lexeme) -> Query.V_URI:
        return self._do_push_lexeme(self.q._mk_uri(obj.iri.content))

    def _push_lexeme_template(self, tpl: LexemeTemplate) -> Query.V_URI:
        if isinstance(tpl.iri, IRI_Template):
            assert isinstance(tpl.iri.content, StringVariable)
            return self._do_push_lexeme(
                self._theta_add_as_qvar(tpl.iri.content))
        elif isinstance(tpl.iri, IRI_Variable):
            return self._do_push_lexeme(self._theta_add_as_qvar(tpl.iri))
        else:
            raise self._should_not_get_here()

    def _push_lexeme_variable(self, var: LexemeVariable) -> Query.V_URI:
        return self._push_lexeme_template(
            self._theta_add(var, LexemeTemplate(self._fresh_iri_variable())))

    def _do_push_lexeme(self, v_lexeme: V_URI1) -> V_URI1:
        self.q.triples()((v_lexeme, NS.RDF.type, NS.ONTOLEX.LexicalEntry))
        return v_lexeme

    # -- Snak --

    def _push_snak(self, obj: Snak, ctx: StmtCtx) -> Query.V_URI:
        if isinstance(obj, ValueSnak):
            return self._push_value_snak(obj, ctx)
        elif isinstance(obj, SomeValueSnak):
            raise NotImplementedError
        elif isinstance(obj, NoValueSnak):
            raise NotImplementedError
        else:
            raise self._should_not_get_here()

    # -- ValueSnak --

    def _push_value_snak(
            self,
            obj: ValueSnak,
            ctx: StmtCtx
    ) -> Query.V_URI:
        v_property = self._push_property(obj.property)
        v_value = self._push_value(
            obj.value, self._as_snakctx(ctx, v_property))
        self._do_push_value_snak(ctx['v_wds'], v_property, v_value)
        return v_property

    def _do_push_value_snak(
            self,
            v_wds: V_URI1,
            v_property: V_URI2,
            v_value: VTerm1
    ) -> tuple[V_URI1, V_URI2, VTerm1]:
        ps = self.q.fresh_var()
        self.q.triples()(
            (v_property, NS.WIKIBASE.statementProperty, ps),
            (v_wds, ps, v_value))
        return v_wds, v_property, v_value

    # -- Value --

    def _push_value(
            self,
            obj: Value,
            ctx: SnakCtx
    ) -> Query.VTerm:
        if isinstance(obj, Entity):
            return self._push_entity(obj)
        elif isinstance(obj, DataValue):
            return self._push_data_value(obj, ctx)
        elif isinstance(obj, DeepDataValue):
            raise NotImplementedError
        else:
            raise self._should_not_get_here()

    # -- DataValue --

    def _push_data_value(
            self,
            obj: DataValue,
            ctx: SnakCtx
    ) -> Query.Term:
        if isinstance(obj, ShallowDataValue):
            return self._push_shallow_data_value(obj, ctx)
        else:
            raise self._should_not_get_here()

    # -- ShallowDataValue --

    def _push_shallow_data_value(
            self,
            obj: ShallowDataValue,
            ctx: SnakCtx
    ) -> Query.Term:
        if isinstance(obj, IRI):
            return self._push_iri(obj, ctx)
        elif isinstance(obj, Text):
            raise NotImplementedError
        elif isinstance(obj, ExternalId):
            raise NotImplementedError
        elif isinstance(obj, String):
            raise NotImplementedError
        else:
            raise self._should_not_get_here()

    # -- IRI --

    def _push_iri(
            self,
            obj: IRI,
            ctx: SnakCtx
    ) -> Query.URI:
        self.q.triples()(
            (ctx['v_property'], NS.WIKIBASE.propertyType, NS.WIKIBASE.Url))
        return self.uri(obj.content)
