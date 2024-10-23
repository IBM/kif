# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum
import functools

from ... import itertools
from ...model import (
    AndFingerprint,
    CompoundFingerprint,
    ConverseSnakFingerprint,
    Datatype,
    Entity,
    EntityTemplate,
    EntityVariable,
    Filter,
    Fingerprint,
    FullFingerprint,
    NoValueSnak,
    OrFingerprint,
    Property,
    Snak,
    SnakFingerprint,
    SnakTemplate,
    SomeValueSnak,
    Statement,
    StatementTemplate,
    StatementVariable,
    Term,
    Text,
    Theta,
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
    Callable,
    cast,
    Final,
    Iterable,
    Iterator,
    Mapping,
    override,
    Sequence,
    TypedDict,
    TypeVar,
)
from .builder import Query
from .filter_compiler import SPARQL_FilterCompiler
from .mapping import SPARQL_Mapping
from .substitution import Substitution

T = TypeVar('T')


class SPARQL_MappingFilterCompiler(SPARQL_FilterCompiler):
    """SPARQL Mapping - Filter Compiler """

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
        phase: SPARQL_MappingFilterCompiler.Phase

        #: The substitution of frame.
        substitution: Substitution

        #: The query variable holding the wds of frame.
        wds: Query.Variable

        #: The entry of frame.
        entry: SPARQL_Mapping.Entry | None

        #: The target patterns of frame.
        targets: Sequence[SPARQL_Mapping.EntryPattern] | None

    __slots__ = (
        '_mapping',
        '_entry_id_qvar',
        '_entry_subst',
        '_entry_targets',
        '_frame',
    )

    # The SPARQL mapping.
    _mapping: SPARQL_Mapping

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
            flags: SPARQL_FilterCompiler.Flags | None = None,
    ) -> None:
        super().__init__(filter, flags)
        self._mapping = mapping
        self._entry_id_qvar = self.q.fresh_var()
        self._entry_subst = {}
        self._entry_targets = {}
        self._frame = []
        self._push_frame({
            'phase': self.READY,
            'substitution': Substitution(),
            'wds': self._wds,
            'entry': None,
            'targets': None,
        })

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

    def _push_frame(self, frame: Frame) -> Frame:
        self._frame.append(frame)
        return frame

    def _pop_frame(self) -> Frame:
        assert self._frame
        return self._frame.pop()

    @property
    def phase(self) -> SPARQL_MappingFilterCompiler.Phase:
        """The compilation phase associated with the current frame."""
        return self.get_phase()

    def get_phase(self) -> SPARQL_MappingFilterCompiler.Phase:
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
    def theta(self) -> Substitution:
        """The substitution associated with the current frame."""
        return self.get_theta()

    def get_theta(self) -> Substitution:
        """Gets the substitution associated with the current frame.

        Returns:
           Substitution.
        """
        return self.frame['substitution']

    def theta_add(self, variable: Variable, value: T) -> T:
        """Adds variable-value pair to the current substitution.

        Parameters:
           variable: Variable.
           value: Value.

        Returns:
           Value.
        """
        if self.has_flags(self.DEBUG):
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
    def wds(self) -> Query.Variable:
        """The wds associated with the current frame."""
        return self.get_wds()

    def get_wds(self) -> Query.Variable:
        """Gets the wds associated with the current.

        Returns:
           Query variable.
        """
        return self.frame['wds']

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

    @override
    def _push_filter(self, filter: Filter) -> None:
        sources = list(self._filter_to_patterns(filter))
        self.mapping.preamble(self, sources)
        all_targets: list[SPARQL_Mapping.EntryPattern] = []
        with self.q.union():
            for source in sources:
                source = source.generalize(rename=self._fresh_name_generator())
                for entry in self.mapping:
                    matches = entry.match_and_preprocess(
                        self.mapping, self, source, self._term2arg)
                    if not matches:
                        continue  # nothing to do
                    targets, theta, kwargs = matches
                    if not targets:
                        continue  # nothing to do
                    push = functools.partial(
                        self._push_filter_push_entry,
                        filter, entry, theta=theta, kwargs=kwargs)
                    if True:
                        ###
                        # TODO: Add an option to split targets.
                        ###
                        for target in targets:
                            push((target,))
                    else:
                        push(targets)
                    all_targets += targets
        if not self._entry_subst:
            self._q = self.Query()  # empty query
        self.frame['phase'] = self.DONE
        self.mapping.postamble(self, all_targets)

    def _push_filter_push_entry(
            self,
            filter: Filter,
            entry: SPARQL_Mapping.Entry,
            targets: Sequence[SPARQL_Mapping.EntryPattern],
            theta: Theta,
            kwargs: Mapping[str, SPARQL_Mapping.EntryCallbackArg]
    ) -> None:
        assert targets
        self._push_frame({
            'phase': self.COMPILING_FILTER,
            'entry': entry,
            'targets': targets,
            'substitution': Substitution(),
            'wds': self.wds,  # same as last wds
        })
        for var, val in entry.default_map.items():
            self.theta_add_default(var, val)
        try:
            with self.q.group():
                if self.has_flags(self.DEBUG):
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
            pass
        else:
            self._entry_subst[entry.id] = self.theta
            if entry.id not in self._entry_targets:
                self._entry_targets[entry.id] = []
            self._entry_targets[entry.id].extend(targets)  # type: ignore
        finally:
            self._pop_frame()

    def _push_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            filter: Filter,
            targets: Iterable[VStatement]
    ) -> None:
        push = functools.partial(self._do_push_fps, entry, targets)
        if isinstance(filter.subject, (CompoundFingerprint, SnakFingerprint)):
            push(filter.subject, self._push_fps_extract_subject)
        if isinstance(filter.property, (CompoundFingerprint, SnakFingerprint)):
            push(filter.property, self._push_fps_extract_property)
        if isinstance(filter.value, (CompoundFingerprint, SnakFingerprint)):
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
            fp: CompoundFingerprint | SnakFingerprint,
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
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {fp}')
                self._push_compound_fp(entry, fp, value)
        elif isinstance(fp, SnakFingerprint):
            if isinstance(value, (Entity, EntityTemplate, EntityVariable)):
                with self.q.group():
                    if self.has_flags(self.DEBUG):
                        self.q.comments()(f'{value} =~ {fp}')
                    self._push_snak_fp(entry, fp, value)
            else:
                raise SPARQL_Mapping.Skip
        elif isinstance(fp, FullFingerprint):
            pass
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
            assert not values
            for child in itertools.chain(snaks, comps):
                self._push_fp(entry, child, value)
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
                source = fp.snak.property(fp.snak.value, entity)
            except (TypeError, ValueError) as err:
                raise self.mapping.Skip from err
        else:
            source = Statement(entity, fp.snak)
        source = source.generalize(rename=self._fresh_name_generator())
        with self.q.union() as cup:
            for target_entry in self.mapping:
                target_entry = target_entry.rename(
                    rename=self._fresh_name_generator())
                matches = target_entry.match_and_preprocess(
                    self.mapping, self, source, self._term2arg)
                if not matches:
                    continue  # nothing to do
                targets, _, kwargs = matches
                if not targets:
                    raise SPARQL_Mapping.Skip
                assert targets
                if kwargs:
                    ###
                    # HACK: Here we monkey-patch `kwargs` so that the source
                    # variable (from snak fingerprint) is replaced by the
                    # correct target variable (from filter).  Is this the
                    # best way to do this?
                    ###
                    assert len(targets) == 1
                    src = next(targets[0]._iterate_variables()).name
                    assert isinstance(kwargs[src], Query.Variable)
                    tgt = next(entity._iterate_variables()).name
                    kwargs[src] = Query.Variable(tgt)  # type: ignore
                self._push_frame({
                    'phase': self.COMPILING_FINGERPRINT,
                    'entry': target_entry,
                    'targets': targets,
                    'substitution': Substitution(),
                    'wds': self.fresh_qvar(),
                })
                try:
                    with self.q.group():
                        target_entry.callback(self.mapping, self, **kwargs)
                except self.mapping.Skip as skip:
                    raise skip
                finally:
                    self._pop_frame()
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

    def _binding_to_thetas(
            self,
            binding: Mapping[str, dict[str, str]]
    ) -> Iterator[Theta]:
        assert str(self._entry_id_qvar) in binding
        id = int(binding[str(self._entry_id_qvar)]['value'])
        entry = self._mapping[id]
        for var in entry.postprocess_map:
            if var.name in binding:
                try:
                    term = entry.postprocess(
                        self.mapping, self, var,
                        self._dict2term(binding[var.name]))
                except SPARQL_Mapping.Skip:
                    return
                else:
                    assert isinstance(term, (Query.Literal, Query.URI))
                    assert isinstance(binding, dict)
                    binding[var.name] = self._term2dict(term)
        assert isinstance(self.pattern, VariablePattern)
        assert isinstance(self.pattern.variable, StatementVariable)
        theta = self._entry_subst[id].instantiate(binding)
        for target in self._entry_targets[id]:
            yield {self.pattern.variable: target.instantiate(theta)}

    def _dict2term(self, t: dict[str, str]) -> Query.Term:
        assert 'type' in t
        if t['type'] == 'uri':
            return Query.URI(t['value'])
        elif t['type'] == 'literal':
            ###
            # TODO: Handle language and datatype.
            ###
            return Query.Literal(t['value'])
        else:
            raise NotImplementedError

    def _term2dict(self, term: Query.Term) -> dict[str, str]:
        if isinstance(term, Query.URI):
            return {'type': 'uri', 'value': str(term)}
        elif isinstance(term, Query.Literal):
            ###
            # TODO: Handle language and datatype.
            ###
            assert term.language is None
            assert term.datatype is None
            return {'type': 'literal', 'value': str(term)}
        else:
            raise NotImplementedError

    def _filter_to_patterns(
            self,
            filter: Filter
    ) -> Iterator[SPARQL_Mapping.EntryPattern]:
        if isinstance(filter.subject, ValueFingerprint):
            subject: VEntity = cast(Entity, filter.subject.value)
        elif filter.subject_mask == filter.ITEM:
            subject = self._fresh_item_variable()
        elif filter.subject_mask == filter.PROPERTY:
            subject = self._fresh_property_variable()
        elif filter.subject_mask == filter.LEXEME:
            subject = self._fresh_lexeme_variable()
        elif filter.subject_mask & filter.ENTITY:
            subject = self._fresh_entity_variable()
        else:
            raise self._should_not_get_here()
        if isinstance(filter.property, ValueFingerprint):
            property: VProperty = cast(Property, filter.property.value)
        else:
            property = self._fresh_property_variable()
        if filter.snak_mask & filter.VALUE_SNAK:
            assert bool(filter.value_mask)
            value_mask = (
                filter.value_mask & filter.property.range_datatype_mask)
            mk_pat = (lambda v: Statement(subject, ValueSnak(property, v)))
            if isinstance(filter.value, ValueFingerprint):
                yield mk_pat(cast(Value, filter.value.value))
            else:
                if value_mask & filter.ITEM:
                    yield mk_pat(self._fresh_item_variable())
                if value_mask & filter.PROPERTY:
                    yield mk_pat(self._fresh_property_variable())
                if value_mask & filter.LEXEME:
                    yield mk_pat(self._fresh_lexeme_variable())
                if value_mask & filter.IRI:
                    yield mk_pat(self._fresh_iri_variable())
                if value_mask & filter.TEXT:
                    if filter.language is None:
                        yield mk_pat(self._fresh_text_variable())
                    else:
                        yield mk_pat(Text(
                            self._fresh_string_variable(), filter.language))
                if value_mask & filter.STRING:
                    yield mk_pat(self._fresh_string_variable())
                if value_mask & filter.EXTERNAL_ID:
                    yield mk_pat(self._fresh_external_id_variable())
                if value_mask & filter.QUANTITY:
                    yield mk_pat(self._fresh_quantity_variable())
                if value_mask & filter.TIME:
                    yield mk_pat(self._fresh_time_variable())
        if filter.snak_mask & filter.SOME_VALUE_SNAK:
            yield Statement(subject, SomeValueSnak(property))
        if filter.snak_mask & filter.NO_VALUE_SNAK:
            yield Statement(subject, NoValueSnak(property))
