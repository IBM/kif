# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re

from ....context import Section
from ....model import (
    AliasProperty,
    Datatype,
    DescriptionProperty,
    ExternalId,
    Filter,
    IRI,
    Item,
    ItemVariable,
    LabelProperty,
    LanguageProperty,
    LemmaProperty,
    Lexeme,
    LexicalCategoryProperty,
    Property,
    Quantity,
    Statement,
    StatementTemplate,
    String,
    Term,
    Text,
    Time,
    Variables,
)
from ....namespace import (
    DCT,
    ONTOLEX,
    RDF,
    RDFS,
    SCHEMA,
    SKOS,
    WIKIBASE,
    Wikidata,
)
from ....typing import Any, ClassVar, Final, Iterable, override, TypeAlias
from ..mapping_filter_compiler import SPARQL_MappingFilterCompiler as C
from .mapping import SPARQL_Mapping as M

__all__ = (
    'WikidataMapping',
)

Arg: TypeAlias = M.EntryCallbackArg

Literal: TypeAlias = C.Query.Literal
VLiteral: TypeAlias = C.Query.VLiteral

URI: TypeAlias = C.Query.URI
V_URI: TypeAlias = C.Query.V_URI

Var: TypeAlias = C.Query.Variable
Var3: TypeAlias = tuple[Var, Var, Var]

d, e, p, w, x, y, z = Variables(*'depwxyz')


@dataclasses.dataclass
class WikidataOptions(Section, name='wikidata'):
    """Wikidata SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_strict(kwargs)
        self._init_truthy(kwargs)

    # -- strict --

    _v_strict: ClassVar[tuple[str, bool | None]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_STRICT', None)

    _strict: bool | None

    def _init_strict(self, kwargs: dict[str, Any]) -> None:
        self.strict = kwargs.get('_strict', self.getenv(*self._v_strict))

    @property
    def strict(self) -> bool:
        """Whether to assume full Wikidata SPARQL compatibility."""
        return self.get_strict()

    @strict.setter
    def strict(self, strict: bool | None) -> None:
        self.set_strict(strict)

    @property
    def relax(self) -> bool:
        """Whether to assume only standard SPARQL compatibility."""
        return not self.strict

    def get_strict(self) -> bool:
        """Gets the value of the strict flag.

        Returns:
           Strict flag value.
        """
        return bool(self._strict)

    def set_strict(self, strict: bool | None) -> None:
        """Sets the value of the strict flag.

        Parameters:
           strict: Strict flag value or ``None``.
        """
        self._strict = bool(strict)

    # -- truthy --

    _v_truthy: ClassVar[tuple[str, Filter.DatatypeMask]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_WIKIDATA_TRUTHY',
         Filter.DatatypeMask(0))

    _truthy: Filter.DatatypeMask

    def _init_truthy(self, kwargs: dict[str, Any]) -> None:
        self.truthy = kwargs.get(
            '_truthy', int(self.getenv(
                self._v_truthy[0], self._v_truthy[1].value)))

    @property
    def truthy(self) -> Filter.DatatypeMask:
        """The truthy mask for filter compilation phase."""
        return self.get_truthy()

    @truthy.setter
    def truthy(self, truthy: Filter.TDatatypeMask) -> None:
        self.set_truthy(truthy)

    def get_truthy(self) -> Filter.DatatypeMask:
        """Gets the truthy mask for the filter compilation phase.

        Returns:
           Datatype mask.
        """
        return self._truthy

    def set_truthy(self, truthy: Filter.TDatatypeMask) -> None:
        """Sets the truthy mask for the filter compilation phase.

        Parameters:
           truthy: Datatype mask.
        """
        self._truthy = Filter.DatatypeMask.check(
            truthy, self.set_truthy, 'truthy', 1)


class WikidataMapping(M):
    """Wikidata SPARQL mapping.

    Parameters:
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

    __slots__ = (
        '_options',
    )

    #: Wikidata SPARQL mapping options.
    _options: WikidataOptions

    def __init__(
            self,
            strict: bool | None = None,
            truthy: Filter.TDatatypeMask | None = None
    ) -> None:
        self._options = dataclasses.replace(
            self.context.options.compiler.sparql.mapping.wikidata)
        if strict is not None:
            self.options.set_strict(strict)
        if truthy is not None:
            self.options.set_truthy(truthy)

    @property
    def options(self) -> WikidataOptions:
        """The Wikidata SPARQL mapping options."""
        return self.get_options()

    def get_options(self) -> WikidataOptions:
        """Gets the Wikidata SPARQL mapping options.

        Returns:
           Wikidata SPARQL mapping options.
        """
        return self._options

    @override
    def postamble(self, c: C, targets: Iterable[M.EntryPattern]) -> None:
        subject_of_all_targets_is_fixed = all(map(lambda s: (
            isinstance(s, (Statement, StatementTemplate))
            and Term.is_closed(s.subject)), targets))
        if subject_of_all_targets_is_fixed:
            ###
            # IMPORTANT: We use ORDER BY(?wds) only if the subject of all
            # target patterns is fixed.  We do this to ensure that the
            # expected number of results is not too large.
            ###
            c.q.set_order_by(c.wds)

    def _start_Q(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> Var3:
        t = self._start_any(c, e, p, dt)
        self._start_Q_tail(c, e)
        return t

    def _start_Q_tail(self, c: C, e: V_URI):
        if c.is_compiling_filter():
            c.q.triples()((e, WIKIBASE.sitelinks, c.q.bnode()))

    def _start_L(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> Var3:
        t = self._start_any(c, e, p, dt)
        self._start_L_tail(c, e)
        return t

    def _start_L_tail(self, c: C, e: V_URI):
        if c.is_compiling_filter():
            c.q.triples()((e, RDF.type, ONTOLEX.LexicalEntry))

    def _start_P(
            self,
            c: C,
            e: V_URI,
            edt: V_URI,
            p: V_URI,
            pdt: V_URI
    ) -> Var3:
        t = self._start_any(c, e, p, pdt)
        self._start_P_tail(c, e, edt)
        return t

    def _start_P_tail(self, c: C, e: V_URI, edt: V_URI):
        if c.is_compiling_filter():
            c.q.triples()(
                (e, RDF.type, WIKIBASE.Property),
                (e, WIKIBASE.propertyType, edt))

    def _start_any(self, c: C, e: V_URI, p: V_URI, dt: V_URI) -> Var3:
        wds = c.wds
        p_, ps = c.fresh_qvars(2)
        c.q.triples()(
            (e, p_, wds),
            (p, RDF.type, WIKIBASE.Property),
            (p, WIKIBASE.claim, p_),
            (p, WIKIBASE.propertyType, dt),
            (p, WIKIBASE.statementProperty, ps),
            (wds, WIKIBASE.rank, c.bnode()))
        if c.has_flags(c.BEST_RANK):
            c.q.triples()((wds, RDF.type, WIKIBASE.BestRank))
        return p_, ps, wds

    # -- label (pseudo-property) --

    @M.register(
        [Statement(Item(e), LabelProperty()(Text(x, y)))],
        {e: CheckItem()})
    def p_item_label(self, c: C, e: V_URI, x: VLiteral, y: VLiteral):
        self._start_Q_tail(c, e)
        self._p_text_tail(c, RDFS.label, e, x, y)

    @M.register(
        [Statement(Property(e, d), LabelProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()})
    def p_property_label(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral
    ):
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, RDFS.label, e, x, y)

    # -- alias (pseudo-property) --

    @M.register(
        [Statement(Item(e), AliasProperty()(Text(x, y)))],
        {e: CheckItem()})
    def p_item_alias(self, c: C, e: V_URI, x: VLiteral, y: VLiteral):
        self._start_Q_tail(c, e)
        self._p_text_tail(c, SKOS.altLabel, e, x, y)

    @M.register(
        [Statement(Property(e, d), AliasProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()})
    def p_property_alias(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral
    ):
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, SKOS.altLabel, e, x, y)

    # -- description (pseudo-property) --

    @M.register(
        [Statement(Item(e), DescriptionProperty()(Text(x, y)))],
        {e: CheckItem()})
    def p_item_description(self, c: C, e: V_URI, x: VLiteral, y: VLiteral):
        self._start_Q_tail(c, e)
        self._p_text_tail(c, SCHEMA.description, e, x, y)

    @M.register(
        [Statement(Property(e, d), DescriptionProperty()(Text(x, y)))],
        {e: CheckProperty(),
         d: CheckDatatype()})
    def p_property_description(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            x: VLiteral,
            y: VLiteral
    ):
        self._start_P_tail(c, e, d)
        self._p_text_tail(c, SCHEMA.description, e, x, y)

    # -- lemma, lexical category, language (pseudo-properties) --

    @M.register(
        [Statement(Lexeme(e), LemmaProperty()(Text(x, y)))],
        {e: CheckLexeme()})
    def p_lexeme_lemma(self, c: C, e: V_URI, x: VLiteral, y: VLiteral):
        self._start_L_tail(c, e)
        self._p_text_tail(c, WIKIBASE.lemma, e, x, y)

    @M.register(
        [Statement(Lexeme(e), LexicalCategoryProperty()(Item(x)))],
        {e: CheckLexeme(),
         x: CheckItem()})
    def p_lexeme_lexical_category(self, c: C, e: V_URI, x: V_URI):
        self._start_L_tail(c, e)
        self._p_item_tail(c, WIKIBASE.lexicalCategory, e, x)

    @M.register(
        [Statement(Lexeme(e), LanguageProperty()(Item(x)))],
        {e: CheckLexeme(),
         x: CheckItem()})
    def p_lexeme_langauge(self, c: C, e: V_URI, x: V_URI):
        self._start_L_tail(c, e)
        self._p_item_tail(c, DCT.language, e, x)

    # -- item --

    @M.register(
        [Statement(Item(e), Property(p)(Item(x)))],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_item_item(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_item(c, p, x, self._start_Q(c, e, p, WIKIBASE.WikibaseItem))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Item(x)))],
        {e: CheckLexeme(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_lexeme_item(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_item(c, p, x, self._start_L(c, e, p, WIKIBASE.WikibaseItem))

    @M.register(
        [Statement(Property(e, d), Property(p)(Item(x)))],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckItem()})
    def p_property_item(self, c: C, e: V_URI, d: V_URI, p: V_URI, x: V_URI):
        self._p_item(c, p, x, self._start_P(c, e, d, p, WIKIBASE.WikibaseItem))

    def _p_item(self, c: C, p: V_URI, x: V_URI, var3: Var3):
        _, ps, wds = var3
        self._p_item_tail(c, ps, wds, x)

    def _p_item_tail(self, c: C, ps: V_URI, wds: V_URI, x: V_URI):
        c.q.triples()(
            (wds, ps, x),
            (x, WIKIBASE.sitelinks, c.q.bnode()))

    # -- property --

    @M.register(
        [Statement(Item(e), Property(p)(Property(x, y)))],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_property(self, c: C, e: V_URI, p: V_URI, x: V_URI, y: V_URI):
        self._p_property(c, p, x, y, self._start_Q(
            c, e, p, WIKIBASE.WikibaseProperty))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Property(x, y)))],
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
            y: V_URI
    ):
        self._p_property(c, p, x, y, self._start_L(
            c, e, p, WIKIBASE.WikibaseProperty))

    @M.register(
        [Statement(Property(e, d), Property(p)(Property(x, y)))],
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
            y: V_URI
    ):
        self._p_property(c, p, x, y, self._start_P(
            c, e, d, p, WIKIBASE.WikibaseProperty))

    def _p_property(self, c: C, p: V_URI, x: V_URI, y: V_URI, var3: Var3):
        _, ps, wds = var3
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, WIKIBASE.Property),
            (x, WIKIBASE.propertyType, y))

    # -- lexeme --

    @M.register(
        [Statement(Item(e), Property(p)(Lexeme(x)))],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_item_lexeme(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_lexeme(c, p, x, self._start_Q(
            c, e, p, WIKIBASE.WikibaseLexeme))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Lexeme(x)))],
        {e: CheckLexeme(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_lexeme_lexeme(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_lexeme(c, p, x, self._start_L(
            c, e, p, WIKIBASE.WikibaseLexeme))

    @M.register(
        [Statement(Property(e, d), Property(p)(Lexeme(x)))],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckLexeme()})
    def p_property_lexeme(self, c: C, e: V_URI, d: V_URI, p: V_URI, x: V_URI):
        self._p_lexeme(c, p, x, self._start_P(
            c, e, d, p, WIKIBASE.WikibaseLexeme))

    def _p_lexeme(self, c: C, p: V_URI, x: V_URI, var3: Var3):
        _, ps, wds = var3
        c.q.triples()(
            (wds, ps, x),
            (x, RDF.type, ONTOLEX.LexicalEntry))

    # -- iri --

    @M.register(
        [Statement(Item(e), Property(p)(IRI(x)))],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_item_iri(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_iri(c, p, x, self._start_Q(c, e, p, WIKIBASE.Url))

    @M.register(
        [Statement(Lexeme(e), Property(p)(IRI(x)))],
        {e: CheckItem(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_lexeme_iri(self, c: C, e: V_URI, p: V_URI, x: V_URI):
        self._p_iri(c, p, x, self._start_L(c, e, p, WIKIBASE.Url))

    @M.register(
        [Statement(Property(e, d), Property(p)(IRI(x)))],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty(),
         x: CheckIRI()})
    def p_property_iri(self, c: C, e: V_URI, d: V_URI, p: V_URI, x: V_URI):
        self._p_iri(c, p, x, self._start_P(c, e, d, p, WIKIBASE.Url))

    def _p_iri(self, c: C, p: V_URI, x: V_URI, var3: Var3):
        _, ps, wds = var3
        c.q.triples()((wds, ps, x))

    # -- text --

    @M.register(
        [Statement(Item(e), Property(p)(Text(x, y)))],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_text(self, c: C, e: V_URI, p: V_URI, x: VLiteral, y: VLiteral):
        self._p_text(c, p, x, y, self._start_Q(
            c, e, p, WIKIBASE.Monolingualtext))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Text(x, y)))],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_text(
            self,
            c: C,
            e: V_URI,
            p: V_URI,
            x: VLiteral,
            y: VLiteral
    ):
        self._p_text(c, p, x, y, self._start_L(
            c, e, p, WIKIBASE.Monolingualtext))

    @M.register(
        [Statement(Property(e, d), Property(p)(Text(x, y)))],
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
            y: VLiteral
    ):
        self._p_text(c, p, x, y, self._start_P(
            c, e, d, p, WIKIBASE.Monolingualtext))

    def _p_text(self, c: C, p: V_URI, x: VLiteral, y: VLiteral, var3: Var3):
        _, ps, wds = var3
        self._p_text_tail(c, ps, wds, x, y)

    def _p_text_tail(
            self,
            c: C,
            ps: V_URI,
            wds: V_URI,
            x: VLiteral,
            y: VLiteral
    ):
        if isinstance(y, Var):
            c.q.triples()((wds, ps, x))
            c.q.bind(c.q.lang(x), y)
        elif isinstance(x, Var):
            c.q.triples()((wds, ps, x))
            c.q.filter(c.q.eq(c.q.lang(x), y))
        else:
            c.q.triples()((wds, ps, c.q.Literal(x, y)))

    # -- string --

    @M.register(
        [Statement(Item(e), Property(p)(String(x)))],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_string(self, c: C, e: V_URI, p: V_URI, x: VLiteral):
        self._p_string(c, p, x, self._start_Q(c, e, p, WIKIBASE.String))

    @M.register(
        [Statement(Lexeme(e), Property(p)(String(x)))],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_string(self, c: C, e: V_URI, p: V_URI, x: VLiteral):
        self._p_string(c, p, x, self._start_L(c, e, p, WIKIBASE.String))

    @M.register(
        [Statement(Property(e, d), Property(p)(String(x)))],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()})
    def p_property_string(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral
    ):
        self._p_string(c, p, x, self._start_P(c, e, d, p, WIKIBASE.String))

    def _p_string(self, c: C, p: V_URI, x: VLiteral, var3: Var3):
        _, ps, wds = var3
        c.q.triples()((wds, ps, x))

    # -- external id --

    @M.register(
        [Statement(Item(e), Property(p)(ExternalId(x)))],
        {e: CheckItem(),
         p: CheckProperty()})
    def p_item_external_id(self, c: C, e: V_URI, p: V_URI, x: VLiteral):
        self._p_string(c, p, x, self._start_Q(c, e, p, WIKIBASE.ExternalId))

    @M.register(
        [Statement(Lexeme(e), Property(p)(ExternalId(x)))],
        {e: CheckLexeme(),
         p: CheckProperty()})
    def p_lexeme_external_id(self, c: C, e: V_URI, p: V_URI, x: VLiteral):
        self._p_string(c, p, x, self._start_L(c, e, p, WIKIBASE.ExternalId))

    @M.register(
        [Statement(Property(e, d), Property(p)(ExternalId(x)))],
        {e: CheckProperty(),
         d: CheckDatatype(),
         p: CheckProperty()})
    def p_property_external_id(
            self,
            c: C,
            e: V_URI,
            d: V_URI,
            p: V_URI,
            x: VLiteral
    ):
        self._p_string(c, p, x, self._start_P(
            c, e, d, p, WIKIBASE.ExternalId))

    # -- quantity --

    @M.register(
        [Statement(Item(e), Property(p)(Quantity(x, y@Item, z, w)))],
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
            w: VLiteral
    ):
        self._p_quantity(
            c, p, x, y, z, w, self._start_Q(c, e, p, WIKIBASE.Quantity))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Quantity(x, y@Item, z, w)))],
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
            w: VLiteral
    ):
        self._p_quantity(
            c, p, x, y, z, w, self._start_L(c, e, p, WIKIBASE.Quantity))

    @M.register(
        [Statement(Property(e, d), Property(p)(Quantity(x, y@Item, z, w)))],
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
            w: VLiteral
    ):
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
            var3: Var3
    ) -> None:
        _, ps, wds = var3
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
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
        [Statement(Item(e), Property(p)(Time(x, y, z, w@Item)))],
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
            w: V_URI
    ):
        self._p_time(
            c, p, x, y, z, w, self._start_Q(c, e, p, WIKIBASE.Time))

    @M.register(
        [Statement(Lexeme(e), Property(p)(Time(x, y, z, w@Item)))],
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
            w: V_URI
    ):
        self._p_time(
            c, p, x, y, z, w, self._start_L(c, e, p, WIKIBASE.Time))

    @M.register(
        [Statement(Property(e, d), Property(p)(Time(x, y, z, w@Item)))],
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
            w: V_URI
    ):
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
            var3: Var3
    ):
        _, ps, wds = var3
        psv, wdv = c.fresh_qvars(2)
        c.q.triples()(
            (wds, ps, x),
            (p, WIKIBASE.statementValue, psv),
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
        [Statement(Item(e), Property(x, y).some_value())],
        {e: CheckItem(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_some_value(self, c: C, e: V_URI, x: V_URI, y: V_URI):
        self._p_some_value(c, self._start_Q(c, e, x, y))

    @M.register(
        [Statement(Lexeme(e), Property(x, y).some_value())],
        {e: CheckLexeme(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_lexeme_some_value(self, c: C, e: V_URI, x: V_URI, y: V_URI):
        self._p_some_value(c, self._start_L(c, e, x, y))

    @M.register(
        [Statement(Property(e, d), Property(x, y).some_value())],
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
            y: V_URI
    ):
        self._p_some_value(c, self._start_P(c, e, d, x, y))

    def _p_some_value(self, c: C, var3: Var3):
        _, ps, wds = var3
        some = c.fresh_qvar()
        c.q.triples()((wds, ps, some))
        if self.options.strict:
            c.q.filter(c.q.call(WIKIBASE.isSomeValue, some))
        else:
            c.q.filter(c.q.is_blank(some) | (
                c.q.is_uri(some) & c.q.strstarts(
                    c.q.str(some), str(Wikidata.WDGENID))))

    # -- no value --

    @M.register(
        [Statement(Item(e), Property(x, y).no_value())],
        {e: CheckItem(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_item_no_value(self, c: C, e: V_URI, x: V_URI, y: V_URI):
        self._p_no_value(c, x, y, self._start_Q(c, e, x, y))

    @M.register(
        [Statement(Lexeme(e), Property(x, y).no_value())],
        {e: CheckLexeme(),
         x: CheckProperty(),
         y: CheckDatatype()})
    def p_lexeme_no_value(self, c: C, e: V_URI, x: V_URI, y: V_URI):
        self._p_no_value(c, x, y, self._start_L(c, e, x, y))

    @M.register(
        [Statement(Property(e, d), Property(x, y).no_value())],
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
            y: V_URI
    ):
        self._p_no_value(c, x, y, self._start_P(c, e, d, x, y))

    def _p_no_value(self, c: C, x: V_URI, y: V_URI, var3: Var3):
        _, ps, wds = var3
        wdno = c.fresh_qvar()
        c.q.triples()(
            (x, WIKIBASE.novalue, wdno),
            (x, WIKIBASE.propertyType, y),
            (wds, RDF.type, wdno))
