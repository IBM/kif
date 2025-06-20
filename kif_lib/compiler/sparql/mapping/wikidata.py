# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import functools
import re

from ....context import Context
from ....model import (
    AliasProperty,
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    Datatype,
    DescriptionProperty,
    ExternalId,
    Filter,
    IRI,
    IRI_Datatype,
    Item,
    ItemDatatype,
    ItemVariable,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexemeDatatype,
    LexicalCategoryProperty,
    Normal,
    NoValueSnak,
    Property,
    PropertyDatatype,
    QualifierRecord,
    Quantity,
    QuantityDatatype,
    Rank,
    ReferenceRecord,
    ReferenceRecordSet,
    Snak,
    Statement,
    StatementVariable,
    String,
    StringDatatype,
    Term,
    Text,
    TextDatatype,
    Theta,
    Time,
    TimeDatatype,
    Variable,
    VariablePattern,
    Variables,
)
from ....namespace import (
    DCT,
    ONTOLEX,
    PROV,
    RDF,
    RDFS,
    SCHEMA,
    SKOS,
    WIKIBASE,
    Wikidata,
)
from ....typing import (
    Any,
    cast,
    Final,
    Iterable,
    Iterator,
    Optional,
    override,
    TypeAlias,
    TypedDict,
    Union,
)
from ..filter_compiler import SPARQL_FilterCompiler as C
from ..results import SPARQL_ResultsBinding
from .mapping import SPARQL_Mapping as M
from .options import WikidataMappingOptions

__all__ = (
    'WikidataMapping',
)

Arg: TypeAlias = M.EntryCallbackArg

BNode: TypeAlias = C.Query.BNode

Literal: TypeAlias = C.Query.Literal
VLiteral: TypeAlias = C.Query.VLiteral

URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI
V_URI3: TypeAlias = tuple[V_URI, V_URI, V_URI]

Var: TypeAlias = C.Query.Variable

T_WDS: TypeAlias = Union[BNode, Var]

#: Variables used in register patterns.
d, e, p, r, w, x, y, z = Variables(*'deprwxyz')
As, Rs = Variables('As', 'Rs')


class WikidataMapping(M):
    """Wikidata SPARQL mapping.

    Parameters:
       blazegraph: Whether to target Blazegraph (use named subqueries).
       strict: Whether to be strict (assume full Wikidata compatibility).
       truthy: Truthy mask to be used in the filter compilation phase.
    """

    _re_item_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}Q[1-9][0-9]*$')

    _re_lexeme_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}L[1-9][0-9]*$')

    _re_property_uri: Final[re.Pattern] = re.compile(
        f'^{re.escape(Wikidata.WD)}P[1-9][0-9]*$')

    class CheckDatatype(M.EntryCallbackArgProcessor):
        """Checks whether argument is a datatype value."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            if isinstance(arg, Datatype):
                return arg._to_rdflib()
            else:
                return arg

    class CheckItem(M.CheckURI):
        """Checks whether argument is an item URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_item_uri if m.options.strict else None)(
                m, c, arg)

    class CheckProperty(M.CheckURI):
        """Checks whether argument is a property URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_property_uri if m.options.strict else None)(
                m, c, arg)

    class CheckLexeme(M.CheckURI):
        """Checks whether argument is a lexeme URI."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            assert isinstance(m, WikidataMapping)
            return m.CheckURI(
                match=m._re_lexeme_uri if m.options.strict else None)(
                m, c, arg)

    class CheckIRI(M.CheckStr):
        """Checks whether argument is a IRI content."""

        def __call__(self, m: M, c: C, arg: Arg) -> Arg:
            return URI(str(super().__call__(m, c, arg)))

    class URI_Schema(TypedDict):
        """Resolved property schema with URI values."""

        p: URI
        pq: URI
        pqv: URI
        pr: URI
        prv: URI
        ps: URI
        psv: URI
        wdno: URI
        wdt: URI

    __slots__ = (
        '_context',
        '_options',
        '_uri_schema',
        '_wds',
    )

    #: Wikidata SPARQL mapping options.
    _options: WikidataMappingOptions

    #: Resolved property URI schema indexed by property URI.
    _uri_schema: dict[URI, URI_Schema]

    #: Current wds (stack).
    _wds: list[T_WDS]

    def __init__(
            self,
            blazegraph: bool | None = None,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None,
            use_schema: bool | None = None,
            context: Context | None = None
    ) -> None:
        super().__init__(context)
        self._options = self._get_context_options().copy()
        if blazegraph is not None:
            self.options.set_blazegraph(blazegraph)
        if strict is not None:
            self.options.set_strict(strict)
        if truthy is not None:
            self.options.set_truthy(truthy)
        if use_schema is not None:
            self.options.set_use_schema(use_schema)
        self._uri_schema = {}
        self._wds = []

    def _get_context_options(self) -> WikidataMappingOptions:
        return self.context.options.compiler.sparql.mapping.wikidata

    @property
    def options(self) -> WikidataMappingOptions:
        """The Wikidata SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> WikidataMappingOptions:
        """Gets the Wikidata SPARQL mapping options.

        Returns:
           Wikidata SPARQL mapping options.
        """
        return self._options

    def get_uri_schema(
            self,
            target: Any
    ) -> URI_Schema | None:
        """Gets the resolved property URI schema of target.

        If `target` cannot be coerced to URI, returns ``None``.

        If `target` has no property schema, returns ``None``.

        Parameters:
           target: URI.

        Returns:
           Resolved URI schema or ``None``.
        """
        if not self.options.use_schema:
            return None         # nothing to do
        if isinstance(target, Property):
            property = target
            uri = URI(target.iri.content)
        elif isinstance(target, IRI):
            property = Property(target)
            uri = URI(target.content)
        elif isinstance(target, URI):
            property = Property(target)
            uri = target
        else:
            return None         # cannot coerce target to URI
        if uri not in self._uri_schema:
            with self.context:
                schema = property.schema
                if schema is not None:
                    self._uri_schema[uri] = cast(
                        WikidataMapping.URI_Schema,
                        {k: URI(cast(IRI, v).content)
                         for k, v in schema.items()})
        return self._uri_schema.get(uri)

    @property
    def wds(self) -> T_WDS:
        """The current wds variable."""
        return self.get_wds()

    def get_wds(self) -> T_WDS:
        """Gets the current wds variable.

        Returns:
           Query variable or blank note.
        """
        assert len(self._wds) > 0
        return self._wds[-1]

    @override
    def frame_pushed(self, compiler: C, frame: C.Frame) -> C.Frame:
        frame = super().frame_pushed(compiler, frame)
        phase = frame['phase']
        if phase == C.READY:
            self._wds.append(compiler.fresh_qvar())
        elif phase == C.COMPILING_FILTER:
            if not compiler.filter.annotated:
                ###
                # FIXME: If we're not collecting annotations, use a blank
                # node for wds instead of a variable.  This way statements
                # with the same (s,p,v) will *not* be counted as distinct.
                ###
                self._wds.append(compiler.bnode())
        elif phase == C.COMPILING_FINGERPRINT:
            self._wds.append(compiler.bnode())
        return frame

    @override
    def frame_popped(self, compiler: C, frame: C.Frame) -> C.Frame:
        phase = frame['phase']
        if phase == C.DONE:
            self._wds.pop()
        elif phase == C.COMPILING_FILTER:
            if not compiler.filter.annotated:
                ###
                # FIXME: Now we do the converse of what we did above.
                ###
                self._wds.pop()
        elif phase == C.COMPILING_FINGERPRINT:
            self._wds.pop()
        return super().frame_popped(compiler, frame)

    @override
    def postamble(
            self,
            compiler: C,
            targets: Iterable[M.EntryPattern]
    ) -> None:
        c = compiler
        if not c.q.where_is_empty():
            annotation_of_some_target_is_open = any(map(lambda s: (
                isinstance(s, AnnotatedStatementTemplate)
                and any(map(Term.is_open, (
                    s.qualifiers, s.references, s.rank)))), targets))
            if annotation_of_some_target_is_open:
                ###
                # FIXME: Monkey-patch the compiler to wrap the un-annotated
                # query into a subquery.  It's not pretty but works.
                ###
                v = c.qvar
                subquery = c._q
                c._q = c.Query()
                c._q._fresh_var_counter = subquery._fresh_var_counter
                if self.options.blazegraph:
                    c.q.named_subquery('Q', subquery)()
                else:
                    c.q.subquery(subquery)()
                with c.q.optional():
                    with c.q.union():
                        self._postamble_push_annotations(c)  # qualifiers
                        self._postamble_push_annotations(    # references
                            c, references=True)
                        with c.q.group():  # rank
                            c.q.triples()(
                                (self.wds, WIKIBASE.rank, v('_rank')))

    def _postamble_push_annotations(
            self,
            c: C,
            references: bool = False
    ) -> None:
        v = c.qvar
        if references:
            px = WIKIBASE.reference
            pxv = WIKIBASE.referenceValue
            wds: T_WDS = v('_wdref')
        else:
            px = WIKIBASE.qualifier
            pxv = WIKIBASE.qualifierValue
            wds = self.wds
        with c.q.group():
            c.q.triples()(
                (self.wds, WIKIBASE.rank, v('_rank')))
            if references:
                c.q.triples()((self.wds, PROV.wasDerivedFrom, wds))
            c.q.triples()(
                (wds, v('_px'), v('_xvalue')),
                (v('_xprop'), px, v('_px')),
                (v('_xprop'), pxv, v('_pxv')),
                (v('_xprop'), WIKIBASE.propertyType, v('_xprop_dt')))
            with c.q.optional():  # value is a property
                c.q.triples()(
                    (v('_xvalue'), WIKIBASE.propertyType, v('_xvalue_dt')))
            with c.q.optional():  # value is deep
                wdv = v('_wdv')
                with c.q.union():
                    with c.q.group():  # quantity
                        c.q.triples()(
                            (wds, v('_pxv'), wdv),
                            (wdv, RDF.type, WIKIBASE.QuantityValue),
                            (wdv, WIKIBASE.quantityAmount, v('_xvalue')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.quantityUnit,
                                 v('_qt_unit')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.quantityLowerBound,
                                 v('_qt_lower_bound')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.quantityUpperBound,
                                 v('_qt_upper_bound')))
                    with c.q.group():  # time
                        c.q.triples()(
                            (wds, v('_pxv'), wdv),
                            (wdv, RDF.type, WIKIBASE.TimeValue),
                            (wdv, WIKIBASE.timeValue,
                             v('_xvalue')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.timePrecision,
                                 v('_tm_precision')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.timeTimezone,
                                 v('_tm_timezone')))
                        with c.q.optional():
                            c.q.triples()(
                                (wdv, WIKIBASE.timeCalendarModel,
                                 v('_tm_calendar')))
        with c.q.group():  # no value
            c.q.triples()(
                (self.wds, WIKIBASE.rank, v('_rank')))
            if references:
                c.q.triples()((self.wds, PROV.wasDerivedFrom, wds))
            c.q.triples()(
                (wds, RDF.type, v('_xnovalue')),
                (v('_xprop'), WIKIBASE.novalue, v('_xnovalue')),
                (v('_xprop'), WIKIBASE.propertyType, v('_xprop_dt')))
            ###
            # In May 2025, we observed inconsistencies in WDQS, cases where
            # the same statement was being assigned both "no-value" and
            # "some-value".  This was causing Store.filter_annotated() to
            # return the "some-value" version qualified with the "no-value"
            # snak.  One way to "fix" this is to filter this qualifier out
            # (checking whether its property coincides with that of the main
            # snak).  E.g.,
            #
            #       (v('_prop'), WIKIBASE.claim, v('_claim'))
            #       (c.bnode(), v('_claim'), wds)
            #     c.q.filter(~c.q.eq(v('_xprop'), v('_prop')))
            #
            # However, we decided not to do that because it adds an overhead
            # to handle a cause that shouldn't exist in the first place.
            ###

    @override
    def build_query(
            self,
            compiler: C,
            projection: C.Projection | None = None,
            distinct: bool | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> C.Query:
        if not compiler.q.where.subselect_blocks:
            return super().build_query(
                compiler, projection, distinct, limit, offset)
        else:
            assert len(compiler.q.where.subselect_blocks) == 1
            sb = compiler.q.where.subselect_blocks[0]
            sb.query = sb.query.select(
                compiler._entry_id_qvar, self.wds,
                *self._build_query_get_target_variables(compiler, projection),
                distinct=distinct, limit=limit, offset=offset)
            return compiler.q.select(  # type: ignore
                distinct=distinct, limit=None, offset=None,
                order_by=self.wds)

    class ResultBuilder(M.ResultBuilder):

        #: The current thetas.
        cur_thetas: list[Theta] | None

        #: The current wds.
        cur_wds: str | None

        #: The current qualifiers.
        cur_qualifiers: list[Snak] | None

        #: The current references indexed by wdref.
        cur_references: dict[str, list[Snak]] | None

        #: The current rank.
        cur_rank: str | None

        def __init__(self, mapping: M, compiler: C) -> None:
            super().__init__(mapping, compiler)
            self.cur_qualifiers = None
            self.cur_references = None
            self.cur_rank = None
            self.cur_thetas = None
            self.cur_wds = None

        @override
        def push(self, binding: SPARQL_ResultsBinding) -> Iterator[Theta]:
            if self.cur_wds is None:
                pat = self.c.pattern
                assert isinstance(pat, VariablePattern)
                assert isinstance(pat.variable, StatementVariable)
                thetas = list(super().push(binding))
                ###
                # If the statements resulting from pushing the binding,
                # (i.e., the content of theta[pat.variable] for theta in
                # thetas) does not contain an open annotation (i.e., a
                # variable occurring in qualifier, reference, or rank
                # position) then there is nothing left to do: we can simply
                # yield the obtained thetas.  Otherwise, we must call
                # _push_annotated() to update the query to get the desired
                # annotations.
                ###
                if not any(map(
                        lambda s:
                        isinstance(s, AnnotatedStatementTemplate)
                        and Term.is_open(s.qualifiers)
                        and Term.is_open(s.references)
                        and Term.is_open(s.rank),
                        map(lambda t: t[pat.variable], thetas))):
                    yield from thetas
                else:
                    self._push_new_cur(binding, thetas)
                    yield from self._push_annotated(binding)
            else:
                yield from self._push_annotated(binding)

        def _push_some_pat_variable_has_an_open_annotation(
                self,
                variable: Variable,
                thetas: Iterable[Theta]
        ) -> bool:
            for theta in thetas:
                stmt = theta[variable]
                if isinstance(stmt, AnnotatedStatementTemplate):
                    return (
                        Term.is_open(stmt.qualifiers)
                        or Term.is_open(stmt.references)
                        or Term.is_open(stmt.rank))
            return False

        def _push_new_cur(
                self,
                binding: SPARQL_ResultsBinding,
                thetas: list[Theta]
        ) -> None:
            mapping = cast(WikidataMapping, self.mapping)
            self.cur_thetas = thetas
            self.cur_wds = binding[str(mapping.wds)]['value']
            self.cur_qualifiers = []
            self.cur_references = {}
            if '_rank' in binding:
                self.cur_rank = binding['_rank']['value']
            else:
                self.cur_rank = None

        def _push_annotated(
                self,
                binding: SPARQL_ResultsBinding
        ) -> Iterator[Theta]:
            if not binding:     # finished
                # print('-- done:', self.cur_wds)
                yield from self._push_annotated_emit()
            else:
                mapping = cast(WikidataMapping, self.mapping)
                wds = binding[str(mapping.wds)]['value']
                if wds != self.cur_wds:  # emit
                    yield from self._push_annotated_emit()
                    thetas = list(super().push(binding))
                    self._push_new_cur(binding, thetas)
                # print('-- collect:', self.cur_wds)
                if '_xprop' in binding:
                    if '_wdref' not in binding:  # qualifier
                        assert self.cur_qualifiers is not None
                        self.cur_qualifiers.append(
                            self._push_annotated_check_snak(binding))
                    else:
                        wdref = binding['_wdref']['value']
                        assert self.cur_references is not None
                        if wdref not in self.cur_references:
                            self.cur_references[wdref] = []
                        self.cur_references[wdref].append(
                            self._push_annotated_check_snak(binding))

        def _push_annotated_check_snak(
                self,
                binding: SPARQL_ResultsBinding
        ) -> Snak:
            dt = Datatype.check(binding['_xprop_dt']['value'])
            prop = Property(binding['_xprop']['value'], dt)
            if '_xnovalue' in binding:
                return prop.no_value()
            value = binding['_xvalue']['value']
            if Wikidata.is_wd_some_value(value):
                return prop.some_value()
            elif isinstance(dt, ItemDatatype):
                return prop(Item(value))
            elif isinstance(dt, PropertyDatatype):
                if '_xvalue_dt' in binding:
                    value_dt = Datatype.check(binding['_xvalue_dt']['value'])
                else:
                    value_dt = None
                return prop(Property(value, value_dt))
            elif isinstance(dt, LexemeDatatype):
                return prop(Lexeme(value))
            elif isinstance(dt, (IRI_Datatype, StringDatatype)):
                return prop(value)
            elif isinstance(dt, TextDatatype):
                language = cast(
                    Optional[str], binding['_xvalue'].get('xml:lang'))
                return prop(Text(value, language))
            elif isinstance(dt, QuantityDatatype):
                if '_qt_unit' in binding:
                    unit = binding['_qt_unit']['value']
                else:
                    unit = None
                if '_qt_lower_bound' in binding:
                    lower_bound = binding['_qt_lower_bound']['value']
                else:
                    lower_bound = None
                if '_qt_upper_bound' in binding:
                    upper_bound = binding['_qt_upper_bound']['value']
                else:
                    upper_bound = None
                return prop(Quantity(value, unit, lower_bound, upper_bound))
            elif isinstance(dt, TimeDatatype):
                if '_tm_precision' in binding:
                    precision = binding['_tm_precision']['value']
                else:
                    precision = None
                if '_tm_timezone' in binding:
                    timezone = binding['_tm_timezone']['value']
                else:
                    timezone = None
                if '_tm_calendar' in binding:
                    calendar = binding['_tm_calendar']['value']
                else:
                    calendar = None
                return prop(Time(value, precision, timezone, calendar))
            else:
                raise self.c._should_not_get_here()

        def _push_annotated_emit(self) -> Iterator[Theta]:
            assert self.cur_thetas is not None
            # print('-- emit:', self.cur_wds)
            return map(self._push_annotated_emit_helper, cast(
                list[dict[Variable, Optional[Term]]], self.cur_thetas))

        def _push_annotated_emit_helper(
                self,
                theta: dict[Variable, Term | None]
        ) -> Theta:
            pat = self.c.pattern
            assert isinstance(pat, VariablePattern)
            assert isinstance(pat.variable, StatementVariable)
            assert self.cur_thetas is not None
            stmt = theta[pat.variable]
            assert isinstance(
                stmt, (AnnotatedStatement, AnnotatedStatementTemplate))
            if isinstance(stmt.qualifiers, Variable):
                assert self.cur_qualifiers is not None
                quals: Iterable[Snak] = self.cur_qualifiers
                if isinstance(stmt.snak, NoValueSnak):
                    # Remove ambiguous no-value qualifier snak.
                    quals = filter(lambda s: s != stmt.snak, quals)
                theta[stmt.qualifiers] = QualifierRecord.check(quals)
            if isinstance(stmt.references, Variable):
                assert self.cur_references is not None
                refs: Iterable[Iterable[Snak]] = self.cur_references.values()
                if isinstance(stmt.snak, NoValueSnak):
                    # Remove ambiguous no-value reference snak.
                    refs = map(functools.partial(
                        filter, lambda s: s != stmt.snak), refs)
                theta[stmt.references] = ReferenceRecordSet.check(map(
                    ReferenceRecord.check, refs))
            if isinstance(stmt.rank, Variable):
                assert self.cur_rank is not None
                theta[stmt.rank] = Rank.check(self.cur_rank)
            theta[pat.variable] = stmt.instantiate(theta)
            return theta

    def _start_Q(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> V_URI3:
        t = self._start_any(c, e, p, dt)
        self._start_Q_tail(c, e)
        return t

    def _start_Q_tail(self, c: C, e: V_URI) -> None:
        if c.is_compiling_filter():
            c.q.triples()((e, WIKIBASE.sitelinks, c.q.bnode()))

    def _start_L(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> V_URI3:
        t = self._start_any(c, e, p, dt)
        self._start_L_tail(c, e)
        return t

    def _start_L_tail(self, c: C, e: V_URI) -> None:
        if c.is_compiling_filter():
            c.q.triples()((e, RDF.type, ONTOLEX.LexicalEntry))

    def _start_P(
            self,
            c: C,
            e: V_URI,
            edt: V_URI,
            p: V_URI,
            pdt: V_URI
    ) -> V_URI3:
        t = self._start_any(c, e, p, pdt)
        self._start_P_tail(c, e, edt)
        return t

    def _start_P_tail(self, c: C, e: V_URI, edt: V_URI) -> None:
        if c.is_compiling_filter():
            c.q.triples()(
                (e, RDF.type, WIKIBASE.Property),
                (e, WIKIBASE.propertyType, edt))

    def _start_any(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> V_URI3:
        wds = cast(V_URI, self.wds)
        p_: V_URI = self._get_schema_uri_or_fresh_qvar(c, p, 'p')
        ps: V_URI = self._get_schema_uri_or_fresh_qvar(c, p, 'ps')
        c.q.triples()(
            (e, p_, wds),
            (p, RDF.type, WIKIBASE.Property),
            (p, WIKIBASE.propertyType, dt),
            (wds, WIKIBASE.rank, c.bnode()))
        if isinstance(p_, Var):
            c.q.triples()((p, WIKIBASE.claim, p_))
        if isinstance(ps, Var):
            c.q.triples()((p, WIKIBASE.statementProperty, ps))
        if c.has_flags(c.BEST_RANK):
            c.q.triples()((wds, RDF.type, WIKIBASE.BestRank))
        return p_, ps, wds

    def _get_schema_uri_or_fresh_qvar(
            self,
            c: C,
            p: V_URI,
            name: str
    ) -> V_URI:
        schema = self.get_uri_schema(p)
        if schema is not None:
            if name in schema:
                return schema[name]  # type: ignore
        return c.fresh_qvar()

    def _ensure_wds_is_bound_fix(self, c: C) -> None:
        ###
        # IMPORTANT: Due to the way subqueries are evaluated, when wds is a
        # variable, make sure we bind it to something (a BNode) otherwise
        # some SPARQL engines, including RDFLib and Jena, generate spurious
        # binds.
        ###
        if isinstance(self.wds, Var):
            c.q.bind(c.q.BNODE(), self.wds)

    # -- label (pseudo-property) --

    @M.register(
        [Statement(Item(e), LabelProperty()(Text(x, y)))],
        {e: CheckItem()},
        rank=Normal)
    def p_item_label(
            self,
            c: C,
            e: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_Q_tail(c, e)
        self._p_text_tail(c, RDFS.label, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    @M.register(
        [Statement(Property(e, d), LabelProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()},
        rank=Normal)
    def p_property_label(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, RDFS.label, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    # -- alias (pseudo-property) --

    @M.register(
        [Statement(Item(e), AliasProperty()(Text(x, y)))],
        {e: CheckItem()},
        rank=Normal)
    def p_item_alias(
            self,
            c: C,
            e: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_Q_tail(c, e)
        self._p_text_tail(c, SKOS.altLabel, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    @M.register(
        [Statement(Property(e, d), AliasProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()},
        rank=Normal)
    def p_property_alias(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, SKOS.altLabel, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    # -- description (pseudo-property) --

    @M.register(
        [Statement(Item(e), DescriptionProperty()(Text(x, y)))],
        {e: CheckItem()},
        rank=Normal)
    def p_item_description(
            self,
            c: C,
            e: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_Q_tail(c, e)
        self._p_text_tail(c, SCHEMA.description, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    @M.register(
        [Statement(Property(e, d), DescriptionProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()},
        rank=Normal)
    def p_property_description(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, SCHEMA.description, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    # -- lemma, lexical category, language (pseudo-properties) --

    @M.register(
        [Statement(Lexeme(e), LemmaProperty()(Text(x, y)))],
        {e: CheckLexeme()},
        rank=Normal)
    def p_lexeme_lemma(
            self,
            c: C,
            e: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._start_L_tail(c, e)
        self._p_text_tail(c, WIKIBASE.lemma, e, x, y)
        self._ensure_wds_is_bound_fix(c)

    @M.register(
        [Statement(Lexeme(e), LexicalCategoryProperty()(Item(x)))],
        {e: CheckLexeme(),
         x: CheckItem()},
        rank=Normal)
    def p_lexeme_lexical_category(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._start_L_tail(c, e)
        self._p_item_tail(c, WIKIBASE.lexicalCategory, e, x)
        self._ensure_wds_is_bound_fix(c)

    @M.register(
        [Statement(Lexeme(e), LanguageProperty()(Item(x)))],
        {e: CheckLexeme(),
         x: CheckItem()},
        rank=Normal)
    def p_lexeme_langauge(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._start_L_tail(c, e)
        self._p_item_tail(c, DCT.language, e, x)
        self._ensure_wds_is_bound_fix(c)

    # -- item --

    @M.register(
        [Statement(Item(e), Property(p)(Item(x))),
         Statement(Item(e), Property(p)(Item(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_item_item(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_item(c, p, x, self._start_Q(c, e, p, WIKIBASE.WikibaseItem))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Item(x))),
         Statement(Lexeme(e), Property(p)(Item(x))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_lexeme_item(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_item(c, p, x, self._start_L(c, e, p, WIKIBASE.WikibaseItem))

    @M.register(
        [Statement(Property(e, d), Property(p)(Item(x))),
         Statement(Property(e, d), Property(p)(Item(x))).annotate(As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_property_item(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_item(c, p, x, self._start_P(c, e, d, p, WIKIBASE.WikibaseItem))

    def _p_item(self, c: C, p: V_URI, x: V_URI, t: V_URI3) -> None:
        _, ps, wds = t
        self._p_item_tail(c, ps, wds, x)

    def _p_item_tail(self, c: C, ps: V_URI, wds: V_URI, x: V_URI) -> None:
        c.q.triples()(
            (wds, ps, x),
            (x, WIKIBASE.sitelinks, c.q.bnode()))

    # -- property --

    @M.register(
        [Statement(Item(e), Property(p)(Property(x, y))),
         Statement(Item(e), Property(p)(Property(x, y))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_property(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_property(c, p, x, y, self._start_Q(
            c, e, p, WIKIBASE.WikibaseProperty))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Property(x, y))),
         Statement(Lexeme(e), Property(p)(Property(x, y))).annotate(
             As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_lexeme_property(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_property(c, p, x, y, self._start_L(
            c, e, p, WIKIBASE.WikibaseProperty))

    @M.register(
        [Statement(Property(e, d), Property(p)(Property(x, y))),
         Statement(Property(e, d), Property(p)(Property(x, y))).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_property_property(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_property(c, p, x, y, self._start_P(
            c, e, d, p, WIKIBASE.WikibaseProperty))

    def _p_property(
            self,
            c: C,
            p: V_URI,
            x: V_URI,
            y: V_URI,
            t: V_URI3
    ) -> None:
        _, ps, wds = t
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, WIKIBASE.Property),
            (x, WIKIBASE.propertyType, y))

    # -- lexeme --

    @M.register(
        [Statement(Item(e), Property(p)(Lexeme(x))),
         Statement(Item(e), Property(p)(Lexeme(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_item_lexeme(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_lexeme(c, p, x, self._start_Q(
            c, e, p, WIKIBASE.WikibaseLexeme))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Lexeme(x))),
         Statement(Lexeme(e), Property(p)(Lexeme(x))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_lexeme_lexeme(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_lexeme(c, p, x, self._start_L(
            c, e, p, WIKIBASE.WikibaseLexeme))

    @M.register(
        [Statement(Property(e, d), Property(p)(Lexeme(x))),
         Statement(Property(e, d), Property(p)(Lexeme(x))).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_property_lexeme(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_lexeme(c, p, x, self._start_P(
            c, e, d, p, WIKIBASE.WikibaseLexeme))

    def _p_lexeme(
            self,
            c: C,
            p: V_URI,
            x: V_URI,
            t: V_URI3
    ) -> None:
        _, ps, wds = t
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, ONTOLEX.LexicalEntry))

    # -- iri --

    @M.register(
        [Statement(Item(e), Property(p)(IRI(x))),
         Statement(Item(e), Property(p)(IRI(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_item_iri(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_iri(c, p, x, self._start_Q(c, e, p, WIKIBASE.Url))

    @M.register(
        [Statement(Lexeme(e), Property(p)(IRI(x))),
         Statement(Lexeme(e), Property(p)(IRI(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_lexeme_iri(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_iri(c, p, x, self._start_L(c, e, p, WIKIBASE.Url))

    @M.register(
        [Statement(Property(e, d), Property(p)(IRI(x))),
         Statement(Property(e, d), Property(p)(IRI(x))).annotate(As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_property_iri(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: V_URI,
            **kwargs
    ) -> None:
        self._p_iri(c, p, x, self._start_P(c, e, d, p, WIKIBASE.Url))

    def _p_iri(self, c: C, p: V_URI, x: V_URI, t: V_URI3) -> None:
        _, ps, wds = t
        c.q.triples()((wds, ps, x))
        if isinstance(x, Var):
            c.q.filter(c.q.is_uri(x) & ~self._is_some_value(c, x))

    # -- text --

    @M.register(
        [Statement(Item(e), Property(p)(Text(x, y))),
         Statement(Item(e), Property(p)(Text(x, y))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_text(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._p_text(c, p, x, y, self._start_Q(
            c, e, p, WIKIBASE.Monolingualtext))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Text(x, y))),
         Statement(Lexeme(e), Property(p)(Text(x, y))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_text(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._p_text(c, p, x, y, self._start_L(
            c, e, p, WIKIBASE.Monolingualtext))

    @M.register(
        [Statement(Property(e, d), Property(p)(Text(x, y))),
         Statement(Property(e, d), Property(p)(Text(x, y))).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()})
    def p_property_text(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            **kwargs
    ) -> None:
        self._p_text(c, p, x, y, self._start_P(
            c, e, d, p, WIKIBASE.Monolingualtext))

    def _p_text(
            self,
            c: C,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            t: V_URI3
    ) -> None:
        _, ps, wds = t
        self._p_text_tail(c, ps, wds, x, y)

    def _p_text_tail(
            self,
            c: C,
            ps: V_URI,
            wds: V_URI,
            x: VLiteral,
            y: VLiteral
    ) -> None:
        if isinstance(y, Var):
            c.q.triples()((wds, ps, x))
            c.q.bind(c.q.lang(x), y)
            c.q.filter(c.q.is_literal(x))
        elif isinstance(x, Var):
            c.q.triples()((wds, ps, x))
            c.q.filter(c.q.eq(c.q.lang(x), y))
            c.q.filter(c.q.is_literal(x))
        else:
            c.q.triples()((wds, ps, c.q.Literal(x, y)))

    # -- string --

    @M.register(
        [Statement(Item(e), Property(p)(String(x))),
         Statement(Item(e), Property(p)(String(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_string(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_Q(c, e, p, WIKIBASE.String))

    @M.register(
        [Statement(Lexeme(e), Property(p)(String(x))),
         Statement(Lexeme(e), Property(p)(String(x))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_string(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_L(c, e, p, WIKIBASE.String))

    @M.register(
        [Statement(Property(e, d), Property(p)(String(x))),
         Statement(Property(e, d), Property(p)(String(x))).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()})
    def p_property_string(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_P(c, e, d, p, WIKIBASE.String))

    def _p_string(self, c: C, p: V_URI, x: VLiteral, t: V_URI3) -> None:
        _, ps, wds = t
        c.q.triples()((wds, ps, x))
        c.q.filter(c.q.is_literal(x))

    # -- external id --

    @M.register(
        [Statement(Item(e), Property(p)(ExternalId(x))),
         Statement(Item(e), Property(p)(ExternalId(x))).annotate(As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_external_id(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_Q(c, e, p, WIKIBASE.ExternalId))

    @M.register(
        [Statement(Lexeme(e), Property(p)(ExternalId(x))),
         Statement(Lexeme(e), Property(p)(ExternalId(x))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_external_id(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_L(c, e, p, WIKIBASE.ExternalId))

    @M.register(
        [Statement(Property(e, d), Property(p)(ExternalId(x))),
         Statement(Property(e, d), Property(p)(ExternalId(x))).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()})
    def p_property_external_id(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral,
            **kwargs
    ) -> None:
        self._p_string(c, p, x, self._start_P(
            c, e, d, p, WIKIBASE.ExternalId))

    # -- quantity --

    @M.register(
        [Statement(Item(e), Property(p)(Quantity(x, y@Item, z, w))),
         Statement(Item(e), Property(p)(Quantity(x, y@Item, z, w))).annotate(
             As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty()},
        defaults={y: None, z: None, w: None})
    def p_item_quantity(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral,
            **kwargs
    ) -> None:
        self._p_quantity(
            c, p, x, y, z, w, self._start_Q(c, e, p, WIKIBASE.Quantity))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Quantity(x, y@Item, z, w))),
         Statement(Lexeme(e), Property(p)(Quantity(
             x, y@Item, z, w))).annotate(As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty()},
        defaults={y: None, z: None, w: None})
    def p_lexeme_quantity(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral,
            **kwargs
    ) -> None:
        self._p_quantity(
            c, p, x, y, z, w, self._start_L(c, e, p, WIKIBASE.Quantity))

    @M.register(
        [Statement(Property(e, d), Property(p)(Quantity(x, y@Item, z, w))),
         Statement(Property(e, d), Property(p)(Quantity(
             x, y@Item, z, w))).annotate(As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()},
        defaults={y: None, z: None, w: None})
    def p_property_quantity(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral,
            **kwargs
    ) -> None:
        self._p_quantity(
            c, p, x, y, z, w, self._start_P(c, e, d, p, WIKIBASE.Quantity))

    def _p_quantity(
            self,
            c: C,
            p: V_URI,
            x: VLiteral,
            y: V_URI,
            z: VLiteral,
            w: VLiteral,
            t: V_URI3
    ) -> None:
        _, ps, wds = t
        psv = self._get_schema_uri_or_fresh_qvar(c, p, 'psv')
        wdv = c.fresh_qvar()
        if isinstance(psv, Var):
            c.q.triples()((p, WIKIBASE.statementValue, psv))
        c.q.triples()(
            (wds, ps, x),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.QuantityValue),
            (wdv, WIKIBASE.quantityAmount, x))
        if isinstance(y, URI):
            c.q.triples()(
                (wdv, WIKIBASE.quantityUnit, y))
        elif isinstance(y, ItemVariable):
            if not c.is_compiling_fingerprint():
                with c.q.optional_if(self.options.relax):
                    iri = c._fresh_iri_variable()
                    c.theta_add(y, Item(iri))
                    c.q.triples()(
                        (wdv, WIKIBASE.quantityUnit,
                         c.theta_add_as_qvar(iri)))
                    c.q.bind(c.as_qvar(iri), c.as_qvar(y))
        else:
            raise c._should_not_get_here()
        if not (isinstance(z, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(z, Var)):
                c.q.triples()((wdv, WIKIBASE.quantityLowerBound, z))
        if not (isinstance(w, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(w, Var)):
                c.q.triples()((wdv, WIKIBASE.quantityUpperBound, w))

    # -- time --

    @M.register(
        [Statement(Item(e), Property(p)(Time(x, y, z, w@Item))),
         Statement(Item(e), Property(p)(Time(x, y, z, w@Item))).annotate(
             As, Rs, r)],
        {e: CheckItem(),
         p: CheckProperty(),
         y: M.CheckInt(),
         z: M.CheckInt()},
        defaults={y: None, z: None})
    def p_item_time(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            z: VLiteral,
            w: V_URI,
            **kwargs
    ) -> None:
        self._p_time(
            c, p, x, y, z, w, self._start_Q(c, e, p, WIKIBASE.Time))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Time(x, y, z, w@Item))),
         Statement(Lexeme(e), Property(p)(Time(x, y, z, w@Item))).annotate(
             As, Rs, r)],
        {e: CheckLexeme(),
         p: CheckProperty(),
         y: M.CheckInt(),
         z: M.CheckInt()},
        defaults={y: None, z: None})
    def p_lexeme_time(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            z: VLiteral,
            w: V_URI,
            **kwargs
    ) -> None:
        self._p_time(
            c, p, x, y, z, w, self._start_L(c, e, p, WIKIBASE.Time))

    @M.register(
        [Statement(Property(e, d), Property(p)(Time(x, y, z, w@Item))),
         Statement(Property(e, d), Property(p)(Time(
             x, y, z, w@Item))).annotate(As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         y: M.CheckInt(),
         z: M.CheckInt()},
        defaults={y: None, z: None})
    def p_property_time(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            z: VLiteral,
            w: V_URI,
            **kwargs
    ) -> None:
        self._p_time(
            c, p, x, y, z, w, self._start_P(c, e, d, p, WIKIBASE.Time))

    def _p_time(
            self,
            c: C,
            p: V_URI,
            x: VLiteral,
            y: VLiteral,
            z: VLiteral,
            w: V_URI,
            t: V_URI3
    ) -> None:
        _, ps, wds = t
        psv = self._get_schema_uri_or_fresh_qvar(c, p, 'psv')
        wdv = c.fresh_qvar()
        if isinstance(psv, Var):
            c.q.triples()((p, WIKIBASE.statementValue, psv))
        c.q.triples()(
            (wds, ps, x),
            (wds, psv, wdv),
            (wdv, RDF.type, WIKIBASE.TimeValue),
            (wdv, WIKIBASE.timeValue, x))
        if not (isinstance(y, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(y, Var) and self.options.relax):
                c.q.triples()((wdv, WIKIBASE.timePrecision, y))
        if not (isinstance(z, Var) and c.is_compiling_fingerprint()):
            with c.q.optional_if(isinstance(z, Var) and self.options.relax):
                c.q.triples()((wdv, WIKIBASE.timeTimezone, z))
        if isinstance(w, URI):
            c.q.triples()((wdv, WIKIBASE.timeCalendarModel, w))
        elif isinstance(w, ItemVariable):
            if not c.is_compiling_fingerprint():
                with c.q.optional_if(self.options.relax):
                    iri = c._fresh_iri_variable()
                    c.theta_add(w, Item(iri))
                    c.q.triples()(
                        (wdv, WIKIBASE.timeCalendarModel,
                         c.theta_add_as_qvar(iri)))
                    c.q.bind(c.as_qvar(iri), c.as_qvar(w))
        else:
            raise c._should_not_get_here()

    # -- some value --

    @M.register(
        [Statement(Item(e), Property(x, y).some_value()),
         Statement(Item(e), Property(x, y).some_value()).annotate(As, Rs, r)],
        {e: CheckItem(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_some_value(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_some_value(c, self._start_Q(c, e, x, y))

    @M.register(
        [Statement(Lexeme(e), Property(x, y).some_value()),
         Statement(Lexeme(e), Property(x, y).some_value()).annotate(
             As, Rs, r)],
        {e: CheckLexeme(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_lexeme_some_value(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_some_value(c, self._start_L(c, e, x, y))

    @M.register(
        [Statement(Property(e, d), Property(x, y).some_value()),
         Statement(Property(e, d), Property(x, y).some_value()).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_property_some_value(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_some_value(c, self._start_P(c, e, d, x, y))

    def _p_some_value(self, c: C, t: V_URI3) -> None:
        _, ps, wds = t
        some = c.fresh_qvar()
        c.q.triples()((wds, ps, some))
        c.q.filter(self._is_some_value(c, some))

    def _is_some_value(self, c: C, some: Var) -> C.Query.BooleanExpression:
        if self.options.strict:
            return c.q.call(WIKIBASE.isSomeValue, some)
        else:
            return c.q.is_blank(some) | (
                c.q.is_uri(some) & c.q.strstarts(
                    c.q.str(some), str(Wikidata.WDGENID)))

    # -- no value --

    @M.register(
        [Statement(Item(e), Property(x, y).no_value()),
         Statement(Item(e), Property(x, y).no_value()).annotate(
             As, Rs, r)],
        {e: CheckItem(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_no_value(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_no_value(c, x, y, self._start_Q(c, e, x, y))

    @M.register(
        [Statement(Lexeme(e), Property(x, y).no_value()),
         Statement(Lexeme(e), Property(x, y).no_value()).annotate(
             As, Rs, r)],
        {e: CheckLexeme(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_lexeme_no_value(
            self,
            c: C,
            e: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_no_value(c, x, y, self._start_L(c, e, x, y))

    @M.register(
        [Statement(Property(e, d), Property(x, y).no_value()),
         Statement(Property(e, d), Property(x, y).no_value()).annotate(
             As, Rs, r)],
        {e: CheckProperty(),
         d: CheckDatatype(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_property_no_value(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: V_URI,
            y: V_URI,
            **kwargs
    ) -> None:
        self._p_no_value(c, x, y, self._start_P(c, e, d, x, y))

    def _p_no_value(self, c: C, x: V_URI, y: V_URI, t: V_URI3) -> None:
        _, _, wds = t
        wdno = self._get_schema_uri_or_fresh_qvar(c, x, 'wdno')
        if isinstance(wdno, Var):
            c.q.triples()((x, WIKIBASE.novalue, wdno))
        c.q.triples()(
            (x, WIKIBASE.propertyType, y),
            (wds, RDF.type, wdno))
