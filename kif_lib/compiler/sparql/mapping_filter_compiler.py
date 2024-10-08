# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum

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
    Union,
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

    @override
    def _push_filter(self, filter: Filter) -> None:
        sources = list(self._filter_to_patterns(filter))
        self.mapping.preamble(self, sources)
        all_targets: list[SPARQL_Mapping.EntryPattern] = []
        with self.q.union():
            for source in sources:
                source = source.generalize(rename=self._fresh_name_generator())
                for entry in self.mapping:
                    matches = list(entry.match(source))
                    if not matches:
                        continue  # nothing to do
                    matched_target, matched_theta = zip(*matches)
                    assert len(matched_target) == len(matched_theta)
                    targets: list[SPARQL_Mapping.EntryPattern] = []
                    theta: dict[Variable, Term | None] = {}
                    kwargs: dict[str, SPARQL_Mapping.EntryCallbackArg] = {}
                    for i in range(len(matched_target)):
                        try:
                            it = list(  # consume, trigger exceptions early
                                self._push_filter_get_entry_callback_kwargs(
                                    entry, matched_theta[i]))
                            for var, val, arg in it:
                                if var.name in kwargs:
                                    assert theta[var] == val
                                    assert kwargs[var.name] == arg
                                else:
                                    theta[var] = val
                                    kwargs[var.name] = arg
                        except SPARQL_Mapping.Skip:
                            continue
                        else:
                            targets.append(matched_target[i])
                    if not targets:
                        continue  # nothing to do
                    self._push_frame({
                        'phase': self.COMPILING_FILTER,
                        'entry': entry,
                        'targets': targets,
                        'substitution': Substitution(),
                        'wds': self.wds,  # same as last wds
                    })
                    for var, val in entry.default_map.items():
                        self.theta_add_default(var, val)
                    self.q.stash_begin()
                    try:
                        with self.q.group():
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
                            self._push_filter_push_fps(entry, filter, targets)
                    except self.mapping.Skip:
                        self.q.stash_drop()
                    else:
                        self.q.stash_pop()
                        self._entry_subst[entry.id] = self.theta
                        self._entry_targets[entry.id] = targets
                        all_targets += targets
                    self._pop_frame()
        if not self._entry_subst:
            self._q = self.Query()  # empty query
        self.frame['phase'] = self.DONE
        self.mapping.postamble(self, all_targets)

    def _push_filter_get_entry_callback_kwargs(
            self,
            entry: SPARQL_Mapping.Entry,
            theta: Theta
    ) -> Iterator[tuple[Variable, Term | None, Term | Query.VTerm | None]]:
        for (var, val) in theta.items():
            arg: Term | Query.VTerm | None
            if isinstance(val, self._primitive_var_classes):
                arg = self.as_qvar(cast(Variable, val))
            elif isinstance(val, Value):
                arg = self._as_simple_value(val)
            else:
                arg = val       # keep it as is
            res = entry.preprocess(self.mapping, self, var, arg)
            yield var, val, res

    def _push_filter_push_fps(
            self,
            entry: SPARQL_Mapping.Entry,
            filter: Filter,
            targets: Iterable[VStatement]
    ) -> None:
        # subject
        if isinstance(filter.subject, (CompoundFingerprint, SnakFingerprint)):
            for target in targets:
                assert isinstance(target, (Statement, StatementTemplate))
                self._push_fp(entry, filter.subject, target.subject)
        # snak
        # assert isinstance(target.snak, (Snak, SnakTemplate))
        # if isinstance(filter.property, (CompoundFingerprint, SnakFingerprint)):
        #     self._push_fp(entry, filter.property, target.snak.property)
        # value
        # if (isinstance(target.snak, (ValueSnak, ValueSnakTemplate))
        #     and isinstance(filter.value, (
        #         CompoundFingerprint, SnakFingerprint))):
        #     self._push_fp(entry, filter.value, target.snak.value)

    def _push_fp(
            self,
            entry: SPARQL_Mapping.Entry,
            fp: Fingerprint,
            value: VValue
    ) -> None:
        if isinstance(value, Value) and not fp.match(value):
            raise SPARQL_Mapping.Skip  # fail
        if isinstance(fp, CompoundFingerprint):
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {type(fp).__qualname__}')
                self._push_compound_fp(entry, fp, value)
        elif isinstance(fp, SnakFingerprint):
            if not isinstance(value, (
                    Entity, EntityTemplate, EntityVariable)):
                raise SPARQL_Mapping.Skip  # fail
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {fp}')
                self._push_snak_fp(entry, fp, value)
        elif isinstance(fp, ValueFingerprint):
            with self.q.group():
                if self.has_flags(self.DEBUG):
                    self.q.comments()(f'{value} =~ {fp}')
                raise NotImplementedError
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
            ###
            # TODO: Handle failures.
            ###
            assert len(values) <= 1
            for child in itertools.chain(snaks, comps):
                self._push_fp(entry, child, value)
            if values:
                with self.q.group():
                    self._push_value_fps(entry, values, value)
        elif isinstance(fp, OrFingerprint):
            ###
            # TODO: Handle failures.
            ###
            with self.q.union():
                for child in itertools.chain(snaks, comps):
                    with self.q.group():
                        self._push_fp(entry, child, value)
                if values:
                    with self.q.group():
                        self._push_value_fps(entry, values, value)
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
            except (TypeError, ValueError):
                raise self.mapping.Skip  # fail
        else:
            source = Statement(entity, fp.snak)
        source = source.generalize(rename=self._fresh_name_generator())
        with self.q.union() as cup:
            for target_entry in self.mapping:
                target_entry = target_entry.rename(
                    rename=self._fresh_name_generator())
                matches = list(target_entry.match(source))
                if not matches:
                    continue
                matched_target, matched_theta = zip(*matches)
                assert len(matched_target) == len(matched_theta)
                targets: list[SPARQL_Mapping.EntryPattern] = []
                theta: dict[Variable, Term | None] = {}
                kwargs: dict[str, SPARQL_Mapping.EntryCallbackArg] = {}
                for i in range(len(matched_target)):
                    try:
                        it = list(  # consume, trigger exceptions early
                            self._push_filter_get_entry_callback_kwargs(
                                target_entry, matched_theta[i]))
                        for var, val, arg in it:
                            if var.name in kwargs:
                                assert theta[var] == val
                                assert kwargs[var.name] == arg
                            else:
                                theta[var] = val
                                kwargs[var.name] = arg
                    except SPARQL_Mapping.Skip:
                        continue
                    else:
                        targets.append(matched_target[i])
                assert targets
                ###
                # HACK: START
                ###
                assert len(targets) == 1
                src = next(targets[0]._iterate_variables()).name
                assert isinstance(kwargs[src], Query.Variable)
                tgt = next(entity._iterate_variables()).name
                kwargs[src] = Query.Variable(tgt)
                # print('src:', src)
                # print('tgt:', tgt)
                # print('kwargs:', kwargs)
                ###
                # HACK: END
                ###
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
                except self.mapping.Skip as err:
                    raise err   # fail
                finally:
                    self._pop_frame()
            if not cup.children:
                raise self.mapping.Skip  # fail

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
            raise SPARQL_Mapping.Skip  # fail
        lines = []
        for theta in thetas:
            pairs: list[tuple[
                Query.Variable, Query.Literal | Query.URI | None]] = []
            for var, val in theta.items():
                if var not in entry.pattern.variables:
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
            raise SPARQL_Mapping.Skip  # fail
        assert lines
        vars = list(sorted(lines[0].keys()))
        vals = map(lambda line: tuple(map(lambda k: line[k], vars)), lines)
        self.q.values(*vars)(*vals)

    def _push_value_fps_preprocess(
            self,
            entry: SPARQL_Mapping.Entry,
            variable: Variable,
            values: list[Value]
    ) -> Iterator[Query.Literal | Query.URI]:
        for value in values:
            try:
                yield cast(Union[Query.Literal, Query.URI],
                           entry.preprocess(
                               self.mapping, self, variable,
                               self._as_simple_value(value)))
            except SPARQL_Mapping.Skip:
                continue

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
            if isinstance(filter.value, ValueFingerprint):
                value: VValue = cast(Value, filter.value.value)
            elif filter.value_mask == filter.ITEM:
                value = self._fresh_item_variable()
            elif filter.value_mask == filter.PROPERTY:
                value = self._fresh_property_variable()
            elif filter.value_mask == filter.LEXEME:
                value = self._fresh_lexeme_variable()
            elif filter.value_mask == filter.DATA_VALUE:
                value = self._fresh_data_value_variable()
            elif filter.value_mask == filter.SHALLOW_DATA_VALUE:
                value = self._fresh_shallow_data_value_variable()
            elif filter.value_mask == filter.IRI:
                value = self._fresh_iri_variable()
            elif filter.value_mask == filter.TEXT:
                value = self._fresh_text_variable()
            elif filter.value_mask == filter.STRING:
                value = self._fresh_string_variable()
            elif filter.value_mask == filter.EXTERNAL_ID:
                value = self._fresh_external_id_variable()
            elif filter.value_mask == filter.DEEP_DATA_VALUE:
                value = self._fresh_deep_data_value_variable()
            elif filter.value_mask == filter.QUANTITY:
                value = self._fresh_quantity_variable()
            elif filter.value_mask == filter.TIME:
                value = self._fresh_time_variable()
            else:
                value = self._fresh_value_variable()
            yield Statement(subject, ValueSnak(property, value))
        if filter.snak_mask & filter.SOME_VALUE_SNAK:
            yield Statement(subject, SomeValueSnak(property))
        if filter.snak_mask & filter.NO_VALUE_SNAK:
            yield Statement(subject, NoValueSnak(property))
