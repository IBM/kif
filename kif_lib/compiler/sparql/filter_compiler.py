# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum
import functools

from ... import itertools
from ...model import (
    AndFingerprint,
    AnnotatedStatement,
    AnnotatedStatementTemplate,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    Datatype,
    EdgePath,
    Entity,
    EntityTemplate,
    EntityVariable,
    ExternalId,
    Filter,
    Fingerprint,
    FullFingerprint,
    IRI,
    NoValueSnak,
    OrFingerprint,
    PathFingerprint,
    Pattern,
    Property,
    Quantity,
    Rank,
    SequencePath,
    Snak,
    SnakFingerprint,
    SnakTemplate,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    String,
    SubtypeProperty,
    Term,
    Text,
    Theta,
    Time,
    TypeProperty,
    Value,
    ValueFingerprint,
    ValueSnak,
    ValueSnakTemplate,
    Variable,
    VariablePattern,
    VEntity,
    VProperty,
    VStatement,
    VValue,
)
from ...typing import (
    Any,
    Callable,
    cast,
    Final,
    Iterable,
    Iterator,
    Mapping,
    override,
    Self,
    Sequence,
    TypedDict,
    TypeVar,
)
from .builder import Query
from .compiler import SPARQL_Compiler
from .mapping import SPARQL_Mapping
from .results import SPARQL_ResultsBinding, SPARQL_ResultsTerm
from .substitution import Substitution

T = TypeVar('T')


class SPARQL_FilterCompiler(SPARQL_Compiler):
    """SPARQL filter compiler """

    class Phase(enum.Enum):
        """Compilation phases."""

        #: Compiler is ready.
        READY = enum.auto()

        #: Compiling filter.
        COMPILING_FILTER = enum.auto()

        #: Compiling fingerprint.
        COMPILING_FINGERPRINT = enum.auto()

        #: Compiler is done.
        DONE = enum.auto()

    #: Alias of :attr:`READY`.
    READY: Final[Phase] = Phase.READY

    #: Alias of :attr:`State.COMPILING_FILTER`.
    COMPILING_FILTER: Final[Phase] = Phase.COMPILING_FILTER

    #: Alias of :attr:`State.COMPILING_FINGERPRINT`.
    COMPILING_FINGERPRINT: Final[Phase] = Phase.COMPILING_FINGERPRINT

    #: Alias of :attr:`DONE`.
    DONE: Final[Phase] = Phase.DONE

    class Frame(TypedDict):
        """Compilation frame (context)."""

        #: The compilation phase of frame.
        phase: SPARQL_FilterCompiler.Phase

        #: The entry of frame.
        entry: SPARQL_Mapping.Entry | None

        #: The substitution of frame.
        substitution: Substitution | None

        #: The target patterns of frame.
        targets: Sequence[SPARQL_Mapping.EntryPattern] | None

    __slots__ = (
        '_filter',
        '_mapping',
        '_pattern',
        '_entry_id_qvar',
        '_entry_subst',
        '_entry_targets',
        '_frame',
    )

    #: The source filter.
    _filter: Filter

    # The SPARQL mapping.
    _mapping: SPARQL_Mapping

    #: The source pattern.
    _pattern: Pattern

    #: The query variable holding the index of the matched entry.
    _entry_id_qvar: Query.Variable

    #: The compiled substitutions for a given entry (identified by index).
    _entry_subst: dict[SPARQL_Mapping.EntryId, Substitution]

    #: The compiled targets for a given entry (identified by index).
    _entry_targets: dict[SPARQL_Mapping.EntryId, Sequence[
        SPARQL_Mapping.EntryPattern]]

    #: The frame stack.
    _frame: list[Frame]

    def __init__(
            self,
            filter: Filter,
            mapping: SPARQL_Mapping,
            *args: Any,
            **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self._filter = filter.normalize()
        self._mapping = mapping
        self._pattern = Pattern.check(Variable('_', Statement))
        self._frame = []
        self.push_frame(self.READY)
        self._entry_id_qvar = self.fresh_qvar()
        self._entry_subst = {}
        self._entry_targets = {}

    @property
    def filter(self) -> Filter:
        """The (normalized) source filter."""
        return self.get_filter()

    def get_filter(self) -> Filter:
        """Gets the (normalized) source filter.

        Returns:
           Filter.
        """
        return self._filter

    @property
    def mapping(self) -> SPARQL_Mapping:
        """The SPARQL mapping."""
        return self.get_mapping()

    def get_mapping(self) -> SPARQL_Mapping:
        """Gets the SPARQL mapping.

        Returns:
           SPARQL mapping.
        """
        return self._mapping

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

# -- Frame -----------------------------------------------------------------

    @property
    def frame(self) -> Frame:
        """The current frame."""
        return self.get_frame()

    def get_frame(self) -> Frame:
        """Gets the current frame.

        Returns:
           Frame.
        """
        assert self._frame
        return self._frame[-1]

    def push_frame(
            self,
            phase: SPARQL_FilterCompiler.Phase,
            entry: SPARQL_Mapping.Entry | None = None,
            theta: Substitution | None = None,
            targets: Sequence[SPARQL_Mapping.EntryPattern] | None = None
    ) -> Frame:
        """Pushes a new compilation frame making it the current frame.

        phase: Compilation phase.
        entry: Mapping entry.
        theta: Substitution.
        targets: Mapping entry patterns.

        Returns:
           The pushed frame.
        """
        return self._push_frame(self.mapping.frame_pushed(self, {
            'phase': phase,
            'entry': entry,
            'substitution': theta,
            'targets': targets,
        }))

    def _push_frame(self, frame: Frame) -> Frame:
        self._frame.append(frame)
        return frame

    def pop_frame(self) -> Frame:
        """Pops the current compilation frame.

        Returns:
           The popped frame.
        """
        return self.mapping.frame_popped(self, self._pop_frame())

    def _pop_frame(self) -> Frame:
        assert self._frame
        return self._frame.pop()

    @property
    def phase(self) -> SPARQL_FilterCompiler.Phase:
        """The compilation phase associated with the current frame."""
        return self.get_phase()

    def get_phase(self) -> SPARQL_FilterCompiler.Phase:
        """Gets the compilation phase associated with the current frame.

        Return:
           Compilation phase.
        """
        return self.frame['phase']

    def is_ready(self) -> bool:
        """Tests whether compiler is in "ready" phase.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self.phase == self.READY

    def is_compiling_filter(self) -> bool:
        """Tests whether compiler is in "compiling filter" phase.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self.phase == self.COMPILING_FILTER

    def is_compiling_fingerprint(self) -> bool:
        """Tests whether compiler is in "compiling fingerprint" phase.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self.phase == self.COMPILING_FINGERPRINT

    def is_done(self) -> bool:
        """Tests whether compiler is in "done" phase.

        Returns:
           ``True`` if successful; ``False`` otherwise.
        """
        return self.phase == self.DONE

    @property
    def entry(self) -> SPARQL_Mapping.Entry:
        """The entry associated with current frame."""
        return self.get_entry()

    def get_entry(self) -> SPARQL_Mapping.Entry:
        """Gets the entry associated with current frame.

        Returns:
           SPARQL mapping entry.
        """
        assert self.frame['entry'] is not None
        return self.frame['entry']

    @property
    def theta(self) -> Substitution:
        """The substitution associated with the current frame."""
        return self.get_theta()

    def get_theta(self) -> Substitution:
        """Gets the substitution associated with the current frame.

        Returns:
           Substitution.
        """
        assert self.frame['substitution'] is not None
        return self.frame['substitution']

    def theta_add(self, variable: Variable, value: T) -> T:
        """Adds variable-value pair to the current substitution.

        Parameters:
           variable: Variable.
           value: Value.

        Returns:
           Value.
        """
        if self.debug:
            self.q.comments()(
                f'{variable} := {Substitution._dump_value(value)}')
        return self.theta.add(variable, value)

    def theta_add_as_qvar(self, variable: Variable) -> Query.Variable:
        """Adds variable-query variable to the current substitution.

        Parameters:
           variable: Variable.

        Returns:
           Query variable.
        """
        return self.theta_add(variable, self.as_qvar(variable))

    def theta_add_default(
            self,
            variable: Variable,
            value: Term | None
    ) -> Variable:
        """Sets default value for variable in the current substitution.

        Parameters:
           variable: Variable.
           value: Value.

        Returns:
           Variable.
        """
        return self.theta.add_default(variable, value)

    @property
    def targets(self) -> Sequence[SPARQL_Mapping.EntryPattern]:
        """The target patterns associated with current frame."""
        return self.get_targets()

    def get_targets(self) -> Sequence[SPARQL_Mapping.EntryPattern]:
        """Gets the target patterns associated with current frame.

        Returns:
           Sequence of SPARQL mapping entry patterns.
        """
        assert self.frame['targets'] is not None
        return self.frame['targets']

# -- Compilation -----------------------------------------------------------

    @override
    def compile(self) -> Self:
        if not self.is_done():
            assert self.is_ready(), self.phase
            self._push_filter()
            assert self.is_done(), self.phase
        return self

    def _push_filter(self) -> None:
        if self.filter.is_nonempty():
            self._push_patterns(list(self.mapping.preamble(
                self, self._filter_to_patterns(self.filter))))
        else:
            self.frame['phase'] = self.DONE

    def _push_patterns(
            self,
            patterns: Sequence[SPARQL_Mapping.EntryPattern]
    ) -> None:
        it_match_funcs = (
            (entry, functools.partial(
                entry.match_and_preprocess, self.mapping, self,
                term2arg=self._term2arg)) for entry in sorted(
                    self.mapping,
                    key=SPARQL_Mapping._mk_entry.get_priority,
                    reverse=True))
        it_patterns = (
            pat.generalize(rename=self._fresh_name_generator())
            for pat in patterns)
        matches = filter(
            lambda t: t[1] and t[1][0], (  # filter out empty targets
                (e, f(p)) for (e, f), p in itertools.product(
                    it_match_funcs, it_patterns)))
        for batch in filter(bool, itertools.divide(self.omega, matches)):
            query = self.push_query()
            query_entries = cast(
                set[SPARQL_Mapping.Entry],
                query.set_user_data('entries', set()))
            query_targets = cast(
                list[SPARQL_Mapping.EntryPattern],
                query.set_user_data('targets', []))
            with self.q.union() as cup:
                for entry, m in batch:
                    assert m is not None
                    targets, theta, kwargs = m
                    for target in targets:
                        if self._filter_match(entry, target):
                            status = self._push_filter_push_entry(
                                self.filter, entry, (target,),
                                theta, kwargs)
                            if status:  # not skipped?
                                query_entries.add(entry)
                                query_targets.append(target)
            if not cup.children:
                self.pop_query()  # empty query, discard
        self.frame['phase'] = self.DONE
        self.mapping.postamble(self)

    def _filter_match(
            self,
            entry: SPARQL_Mapping.Entry,
            target: SPARQL_Mapping.EntryPattern
    ) -> bool:
        return not any(f(entry, target) for f in (
            self._filter_property_is_full_and_target_property_is_blacklisted,
            self._filter_property_mask_does_not_match_target_property,
            self._filter_rank_mask_does_not_match_target_rank))

    def _filter_rank_mask_does_not_match_target_rank(
            self,
            entry: SPARQL_Mapping.Entry,
            target: SPARQL_Mapping.EntryPattern
    ) -> bool:
        if isinstance(target, (StatementTemplate, Statement)):
            if entry.annotations is not None:
                rank = entry.annotations.get('rank', None)
                if rank is not None and isinstance(rank, Rank):
                    return not self.filter.rank_mask.match(rank)
        elif isinstance(target, (
                AnnotatedStatementTemplate, AnnotatedStatement)):
            if isinstance(target.rank, Rank):
                return not self.filter.rank_mask.match(target.rank)
        return False

    def _filter_property_mask_does_not_match_target_property(
            self,
            entry: SPARQL_Mapping.Entry,
            target: SPARQL_Mapping.EntryPattern
    ) -> bool:
        if (isinstance(target, (Statement, StatementTemplate))
                and isinstance(target.snak, (Snak, SnakTemplate))):
            if isinstance(target.snak.property, Property):
                return not self.filter.property_mask.match(
                    target.snak.property)
            else:
                ###
                # FIXME: We're assuming that if target property is a
                # template or a variable, then it comes form an entry
                # matching a real (non-pseudo) property.  This assumption is
                # too strict.
                ###
                return not self.filter.property_mask & self.filter.REAL
        return False

    def _filter_property_is_full_and_target_property_is_blacklisted(
            self,
            entry: SPARQL_Mapping.Entry,
            target: SPARQL_Mapping.EntryPattern,
            blacklist: frozenset[Property] = frozenset({
                TypeProperty(), SubtypeProperty()})
    ) -> bool:
        return (
            self.filter.property.is_full()
            and isinstance(target, (Statement, StatementTemplate))
            and isinstance(target.snak, (Snak, SnakTemplate))
            and isinstance(target.snak.property, Property)
            and target.snak.property in blacklist)

    def _fresh_name_generator(self) -> Callable[[str], Iterator[str]]:
        return (lambda _: map(
            lambda _: self.fresh_qvar(), itertools.repeat(None)))

    def _term2arg(self, term: Term) -> Term | Query.VTerm:
        if isinstance(term, self._primitive_var_classes):
            return self.as_qvar(cast(Variable, term))
        elif isinstance(term, Value):
            return self._as_simple_value(term)
        else:
            return term

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

    def _push_filter_push_entry(
            self,
            filter: Filter,
            entry: SPARQL_Mapping.Entry,
            targets: Sequence[SPARQL_Mapping.EntryPattern],
            theta: Theta,
            kwargs: Mapping[str, SPARQL_Mapping.EntryCallbackArg]
    ) -> bool:
        assert targets
        self.push_frame(
            phase=self.COMPILING_FILTER,
            entry=entry,
            theta=Substitution(),
            targets=targets)
        for var, val in entry.default_map.items():
            self.theta_add_default(var, val)
        try:
            with self.q.group():
                if self.debug:
                    self.q.comments()(*map(str, targets))
                self.q.bind(entry.id, self._entry_id_qvar)
                for var, val in theta.items():
                    assert var.name in kwargs
                    arg = kwargs[var.name]
                    if isinstance(arg, Query.Variable):
                        self.theta_add(var, arg)
                    elif isinstance(
                            arg, (Query.URI, Query.Literal)):
                        self.theta_add(var, val)
                entry.callback(self.mapping, self, **kwargs)
                self._push_fps(entry, filter, targets)
        except self.mapping.Skip:
            return False
        else:
            self._entry_subst[entry.id] = self.theta
            if entry.id not in self._entry_targets:
                self._entry_targets[entry.id] = []
            self._entry_targets[entry.id].extend(targets)  # type: ignore
            return True
        finally:
            self.pop_frame()

    def _push_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            filter: Filter,
            targets: Iterable[VStatement]
    ) -> None:
        push = functools.partial(self._do_push_fps, entry, targets)
        if isinstance(filter.subject, (
                CompoundFingerprint, PathFingerprint, SnakFingerprint)):
            push(filter.subject, self._push_fps_extract_subject)
        if isinstance(filter.property, (
                CompoundFingerprint, PathFingerprint, SnakFingerprint)):
            push(filter.property, self._push_fps_extract_property)
        if isinstance(filter.value, (
                CompoundFingerprint, PathFingerprint, SnakFingerprint)):
            push(filter.value, self._push_fps_extract_value)

    def _push_fps_extract_subject(
            self,
            stmt: Statement | StatementTemplate
    ) -> VEntity:
        return stmt.subject

    def _push_fps_extract_property(
            self,
            stmt: Statement | StatementTemplate
    ) -> VProperty:
        if isinstance(stmt.snak, (Snak, SnakTemplate)):
            return stmt.snak.property
        else:
            raise SPARQL_Mapping.Skip

    def _push_fps_extract_value(
            self,
            stmt: Statement | StatementTemplate
    ) -> VValue:
        if isinstance(stmt.snak, (ValueSnak, ValueSnakTemplate)):
            return stmt.snak.value
        else:
            raise SPARQL_Mapping.Skip

    def _do_push_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            targets: Iterable[VStatement],
            fp: CompoundFingerprint | PathFingerprint | SnakFingerprint,
            extract: Callable[[Statement | StatementTemplate], VValue]
    ) -> None:
        with self.q.union() as cup:
            for target in targets:
                assert isinstance(target, (Statement, StatementTemplate))
                try:
                    self._push_fp(entry, fp, extract(target))
                except SPARQL_Mapping.Skip:
                    continue
            if not cup.children:
                raise SPARQL_Mapping.Skip

    def _push_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: Fingerprint,
            value: VValue
    ) -> None:
        if isinstance(value, Value) and not fp.match(value):
            raise SPARQL_Mapping.Skip
        if isinstance(fp, CompoundFingerprint):
            with self.q.group():
                if self.debug:
                    self.q.comments()(f'{value} =~ {fp}')
                self._push_compound_fp(entry, fp, value)
        elif isinstance(fp, PathFingerprint):
            if isinstance(value, (Entity, EntityTemplate, EntityVariable)):
                with self.q.group():
                    if self.debug:
                        self.q.comments()(f'{value} =~ {fp}')
                    self._push_path_fp(entry, fp, value)
            else:
                raise SPARQL_Mapping.Skip
        elif isinstance(fp, SnakFingerprint):
            if isinstance(value, (Entity, EntityTemplate, EntityVariable)):
                with self.q.group():
                    if self.debug:
                        self.q.comments()(f'{value} =~ {fp}')
                    self._push_snak_fp(entry, fp, value)
            else:
                raise SPARQL_Mapping.Skip
        elif isinstance(fp, FullFingerprint):
            pass                # nothing to do
        else:
            raise self._should_not_get_here()

    def _push_compound_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: CompoundFingerprint,
            value: VValue
    ) -> None:
        atoms, comps = map(list, itertools.partition(
            lambda x: isinstance(x, CompoundFingerprint), fp.args))
        snaks, values = map(list, itertools.partition(
            lambda x: isinstance(x, ValueFingerprint), atoms))
        if isinstance(fp, AndFingerprint):
            for child in itertools.chain(snaks, comps):
                self._push_fp(entry, child, value)
            if values:
                try:
                    with self.q.group():
                        self._push_value_fps(entry, values, value)
                except SPARQL_Mapping.Skip:
                    pass
        elif isinstance(fp, OrFingerprint):
            with self.q.union() as cup:
                if isinstance(value, (Entity, EntityTemplate, EntityVariable)):
                    for snak_fp in snaks:
                        ###
                        # TODO: Aggregate snaks with the same property.
                        ###
                        try:
                            with self.q.group():
                                self._push_snak_fp(entry, snak_fp, value)
                        except SPARQL_Mapping.Skip:
                            continue
                for child in comps:
                    try:
                        with self.q.group():
                            self._push_fp(entry, child, value)
                    except SPARQL_Mapping.Skip:
                        continue
                if values:
                    try:
                        with self.q.group():
                            self._push_value_fps(entry, values, value)
                    except SPARQL_Mapping.Skip:
                        pass
                if not cup.children:
                    raise SPARQL_Mapping.Skip
        else:
            raise self._should_not_get_here()

    def _push_path_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: PathFingerprint,
            entity: VEntity
    ) -> None:
        if isinstance(fp.path, EdgePath):
            self._push_snak_fp(
                entry, SnakFingerprint(fp.path.property(fp.value)), entity)
        elif isinstance(fp.path, SequencePath):
            push = functools.partial(self._push_snak_fp_tail, entry)
            source: VEntity = entity
            for p in fp.path[:-1]:
                if p.property.range is not None:
                    var: Variable = self.fresh_var(
                        p.property.range.value_class.variable_class)
                else:
                    var = self.fresh_entity_var()
                assert isinstance(var, EntityVariable), var
                push(source, p.property(source, var))
                source = var
            push(source, fp.path[-1].property(source, fp.value))
        else:
            raise self._should_not_get_here()

    def _push_snak_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: SnakFingerprint,
            entity: VEntity
    ) -> None:
        if isinstance(fp, ConverseSnakFingerprint):
            assert isinstance(fp.snak, ValueSnak)
            assert isinstance(fp.snak.value, Entity)
            try:
                stmt = fp.snak.property(fp.snak.value, entity)
            except (TypeError, ValueError) as err:
                raise self.mapping.Skip from err
        else:
            stmt = Statement(entity, fp.snak)
        return self._push_snak_fp_tail(entry, entity, stmt)

    def _push_snak_fp_tail(
            self,
            entry: SPARQL_Mapping.Entry,
            entity: VEntity,
            stmt: Statement | StatementTemplate
    ) -> None:
        stmt = stmt.generalize(rename=self._fresh_name_generator())
        with self.q.union() as cup:
            for target_entry in self.mapping:
                target_entry = target_entry.rename(
                    rename=self._fresh_name_generator())
                matches = target_entry.match_and_preprocess(
                    self.mapping, self, stmt, self._term2arg)
                if not matches:
                    continue  # nothing to do
                targets, _, kwargs = matches
                if not targets:
                    continue
                assert targets
                if kwargs:
                    ###
                    # HACK: Here we monkey-patch `kwargs` so that the stmt
                    # variable (from snak fingerprint) is replaced by the
                    # correct target variable (from filter).  Is this the
                    # best way to do this?
                    ###
                    assert len(targets) == 1
                    src = next(targets[0]._iterate_variables()).name
                    assert isinstance(kwargs[src], Query.Variable)
                    tgt = next(entity._iterate_variables()).name
                    kwargs[src] = Query.Variable(tgt)  # type: ignore
                if (isinstance(stmt.snak, ValueSnakTemplate)
                        and isinstance(stmt.snak.value, EntityVariable)):
                    ###
                    # HACK: Here we monkey-patch `kwargs` so that the
                    # source/target variables of property chains are matched
                    # correctly.  Is this the best way to to this?
                    ###
                    src = stmt.snak.value.name
                    target = next(iter(targets))
                    assert isinstance(target, StatementTemplate)
                    assert isinstance(target.snak, ValueSnakTemplate)
                    assert len(target.snak.value.variables) == 1
                    tgt = next(iter(target.snak.value.variables)).name
                    kwargs[tgt] = Query.Variable(src)  # type: ignore
                self.push_frame(
                    phase=self.COMPILING_FINGERPRINT,
                    entry=target_entry,
                    theta=Substitution(),
                    targets=targets)
                try:
                    with self.q.group():
                        target_entry.callback(self.mapping, self, **kwargs)
                except self.mapping.Skip:
                    continue
                finally:
                    self.pop_frame()
            if not cup.children:
                raise self.mapping.Skip

    def _push_value_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            fps: Sequence[ValueFingerprint],
            value: VValue,
            use_values_clause: bool = True
    ) -> None:
        assert bool(fps)
        if isinstance(value, Value):
            return              # nothing to do
        thetas: list[Theta] = [
            x for x in map(lambda v: value.match(
                ValueFingerprint.get_value(v).generalize(
                    rename=self._fresh_name_generator())), fps)
            if x is not None]
        if not thetas:
            raise SPARQL_Mapping.Skip
        lines = []
        for theta in thetas:
            pairs: list[tuple[
                Query.Variable, Query.Literal | Query.URI | None]] = []
            for var, val in theta.items():
                if var not in entry.variables:
                    continue    # unknown variable, skip
                qvar = self.as_qvar(var)
                if val is None or isinstance(val, Variable):  # not bound?
                    val = entry.default_map.get(var)
                qval: Query.VTerm | None
                if val is None:
                    qval = None
                elif isinstance(val, Datatype):
                    qval = val._to_rdflib()
                elif isinstance(val, Value):
                    qval = self._as_simple_value(val)
                else:
                    raise self._should_not_get_here()
                try:
                    pp_qval = entry.preprocess(self.mapping, self, var, qval)
                except SPARQL_Mapping.Skip:
                    pairs = []
                    break       # skip line
                assert (pp_qval is None
                        or isinstance(pp_qval, (Query.Literal, Query.URI)))
                pairs.append((qvar, pp_qval))
            if pairs:
                lines.append(dict(pairs))
        if not lines:
            raise SPARQL_Mapping.Skip
        assert lines
        vars = list(sorted(lines[0].keys()))
        vals = map(lambda line: tuple(map(lambda k: line[k], vars)), lines)
        self.q.values(*vars)(*vals)

    class Projection(enum.Flag):
        """Statement projection mask."""

        #: Mask for projection on subject.
        SUBJECT = enum.auto()

        #: Mask for projection on property.
        PROPERTY = enum.auto()

        #: Mask for projection on value.
        VALUE = enum.auto()

        #: Mask for projection on subject, property, and value.
        ALL = SUBJECT | PROPERTY | VALUE

    def build_query(
            self,
            query: SPARQL_FilterCompiler.Query,
            projection: Projection | None = None,
            distinct: bool | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> SPARQL_FilterCompiler.Query:
        """Constructs a filter query.

        Parameters:
           query: Query.
           projection: Projection mask.
           distinct: Whether to enable the distinct modifier.
           limit: Limit.
           offset: Offset.

        Returns:
           Filter query.
        """
        assert self.frame['phase'] == self.DONE
        return self.mapping.build_query(
            self, query, projection, distinct, limit, offset)

    def build_results(
            self
    ) -> Callable[[SPARQL_ResultsBinding], Iterable[Theta] | None]:
        """Constructs a compilation result builder.

        Returns:
           A function to convert a binding in SPARQL results into variable
           instantiations (thetas).
        """
        return self.mapping.build_results(self).push

    def _binding_to_thetas(
            self,
            binding: SPARQL_ResultsBinding
    ) -> Iterator[Theta]:
        assert str(self._entry_id_qvar) in binding
        id = int(binding[str(self._entry_id_qvar)]['value'])
        entry = self._mapping[id]
        for var in entry.postprocess_map:
            if var.name in binding:
                try:
                    term = entry.postprocess(
                        self.mapping, self, var,
                        self._sparql_results_term_to_query_term(
                            binding[var.name]))
                except SPARQL_Mapping.Skip:
                    return
                else:
                    assert isinstance(term, (Query.Literal, Query.URI))
                    assert isinstance(binding, dict)
                    binding[var.name] =\
                        self._query_term_to_sparql_results_term(term)
        assert isinstance(self.pattern, VariablePattern)
        assert isinstance(self.pattern.variable, StatementVariable)
        theta = self._entry_subst[id].instantiate(binding)
        for target in self._entry_targets[id]:
            yield {self.pattern.variable: target.instantiate(theta)}

    def _sparql_results_term_to_query_term(
            self,
            t: SPARQL_ResultsTerm
    ) -> Query.Term:
        assert 'type' in t
        if t['type'] == 'uri':
            return Query.URI(t['value'])
        elif t['type'] == 'literal':
            return Query.Literal(
                t['value'],
                datatype=t.get('datatype'), lang=t.get('xml:lang'))
        elif t['type'] == 'bnode':
            return Query.BNode(t['value'])
        else:
            raise self._should_not_get_here()

    def _query_term_to_sparql_results_term(
            self,
            term: Query.Term
    ) -> SPARQL_ResultsTerm:
        if isinstance(term, Query.URI):
            return {'type': 'uri', 'value': str(term)}
        elif isinstance(term, Query.Literal):
            if term.datatype is not None and term.language is not None:
                return {
                    'type': 'literal',
                    'value': str(term),
                    'datatype': term.datatype,
                    'xml:lang': term.language,
                }
            elif term.datatype is not None:
                return {
                    'type': 'literal',
                    'value': str(term),
                    'datatype': term.datatype,
                }
            elif term.language is not None:
                return {
                    'type': 'literal',
                    'value': str(term),
                    'xml:lang': term.language,
                }
            else:
                return {
                    'type': 'literal',
                    'value': str(term)
                }
        elif isinstance(term, Query.BNode):
            return {'type': 'bnode', 'value': str(term)}
        else:
            raise self._should_not_get_here()

    def _filter_to_patterns(
            self,
            filter: Filter
    ) -> Iterator[SPARQL_Mapping.EntryPattern]:
        if isinstance(filter.subject, ValueFingerprint):
            subjects: list[VEntity] = [cast(Entity, filter.subject.value)]
        else:
            subjects = []
            if filter.subject_mask & filter.ITEM:
                subjects.append(self.fresh_item_var())
            if filter.subject_mask & filter.PROPERTY:
                subjects.append(self.fresh_property_var())
            if filter.subject_mask & filter.LEXEME:
                subjects.append(self.fresh_lexeme_var())
        assert subjects
        if isinstance(filter.property, ValueFingerprint):
            property: VProperty = cast(Property, filter.property.value)
        else:
            property = self.fresh_property_var()
        if filter.snak_mask & filter.VALUE_SNAK:
            assert bool(filter.value_mask)
            value_mask = (
                filter.value_mask & filter.property.range_datatype_mask)

            def mk_pats(
                    value: VValue
            ) -> Iterator[SPARQL_Mapping.EntryPattern]:
                yield from map(
                    lambda subject: self._filter_to_patterns_tail(
                        Statement(subject, ValueSnak(property, value))),
                    subjects)
            if isinstance(filter.value, ValueFingerprint):
                yield from mk_pats(cast(Value, filter.value.value))
            else:
                if value_mask & filter.ITEM:
                    yield from mk_pats(self.fresh_item_var())
                if value_mask & filter.PROPERTY:
                    yield from mk_pats(self.fresh_property_var())
                if value_mask & filter.LEXEME:
                    yield from mk_pats(self.fresh_lexeme_var())
                if value_mask & filter.IRI:
                    yield from mk_pats(self.fresh_iri_var())
                if value_mask & filter.TEXT:
                    if filter.language is None:
                        yield from mk_pats(self.fresh_text_var())
                    else:
                        yield from mk_pats(Text(
                            self.fresh_string_var(), filter.language))
                if value_mask & filter.STRING:
                    yield from mk_pats(self.fresh_string_var())
                elif value_mask & filter.EXTERNAL_ID:
                    yield from mk_pats(self.fresh_external_id_var())
                if value_mask & filter.QUANTITY:
                    yield from mk_pats(self.fresh_quantity_var())
                if value_mask & filter.TIME:
                    yield from mk_pats(self.fresh_time_var())
        if filter.snak_mask & filter.SOME_VALUE_SNAK:
            yield from map(lambda subject: self._filter_to_patterns_tail(
                Statement(subject, SomeValueSnak(property))), subjects)
        if filter.snak_mask & filter.NO_VALUE_SNAK:
            yield from map(lambda subject: self._filter_to_patterns_tail(
                Statement(subject, NoValueSnak(property))), subjects)

    def _filter_to_patterns_tail(
            self,
            stmt: StatementTemplate | Statement
    ) -> SPARQL_Mapping.EntryPattern:
        if self.filter.annotated:
            return stmt.annotate(
                qualifiers=self.fresh_qualifier_record_var(),
                references=self.fresh_reference_record_set_var(),
                rank=self.fresh_rank_var())
        else:
            return stmt
