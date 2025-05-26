# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import dataclasses
import functools
import re
from typing import TYPE_CHECKING

from typing_extensions import overload

from .... import itertools
from ....context import Context
from ....model import (
    KIF_Object,
    QualifierRecord,
    Rank,
    ReferenceRecordSet,
    Statement,
    StatementTemplate,
    StatementVariable,
    Template,
    Term,
    Theta,
    TQualifierRecord,
    TRank,
    TReferenceRecordSet,
    Variable,
    VStatement,
    VTStatement,
)
from ....typing import (
    Any,
    Callable,
    cast,
    ClassVar,
    Iterable,
    Iterator,
    Mapping,
    MutableSequence,
    Optional,
    override,
    Protocol,
    Self,
    Sequence,
    Set,
    TypeAlias,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..filter_compiler import SPARQL_FilterCompiler as Compiler
    from ..results import SPARQL_ResultsBinding


@dataclasses.dataclass
class _Entry:
    """Entry in SPARQL mapping."""

    #: The id of entry.
    id: SPARQL_Mapping.EntryId

    #: The patterns of entry.
    patterns: Sequence[SPARQL_Mapping.EntryPattern]

    #: The callback-arg preprocessor map of entry.
    preprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap

    #: The callback-arg postprocessor map of entry.
    postprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap

    #: The callback-arg defaults map.
    default_map: SPARQL_Mapping.EntryCallbackArgDefaultMap

    #: Annotations to be added to statement patterns.
    annotations: Statement.Annotation | None

    #: The (compilation) callback of entry.
    callback: SPARQL_Mapping.EntryCallback

    def __init__(
            self,
            id: SPARQL_Mapping.EntryId,
            patterns: Iterable[SPARQL_Mapping.EntryPattern],
            preprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap,
            postprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap,
            default_map: SPARQL_Mapping.EntryCallbackArgDefaultMap,
            annotations: Statement.Annotation | None,
            callback: SPARQL_Mapping.EntryCallback
    ) -> None:
        self.id = id
        self.patterns = self._init_patterns(patterns, annotations)
        self.preprocess_map, self.postprocess_map, self.default_map =\
            self._init_entry_callback_arg_maps(
                preprocess_map, postprocess_map, default_map)
        self.annotations = annotations
        self.callback = callback

    def _init_patterns(
            self,
            patterns: Iterable[SPARQL_Mapping.EntryPattern],
            annotations: Statement.Annotation | None
    ) -> Sequence[SPARQL_Mapping.EntryPattern]:
        if annotations is None:
            return tuple(patterns)
        else:
            return tuple(self._init_patterns_with_annotations(
                patterns, annotations))

    def _init_patterns_with_annotations(
            self,
            patterns: Iterable[SPARQL_Mapping.EntryPattern],
            annotations: Statement.Annotation
    ) -> Iterable[SPARQL_Mapping.EntryPattern]:
        for pat in patterns:
            yield pat
            if isinstance(pat, (Statement, StatementTemplate)):
                yield pat.annotate(**annotations)

    def _init_entry_callback_arg_maps(
            self,
            pre: SPARQL_Mapping.EntryCallbackArgProcessorMap,
            post: SPARQL_Mapping.EntryCallbackArgProcessorMap,
            defs: SPARQL_Mapping.EntryCallbackArgDefaultMap
    ) -> tuple[
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallbackArgDefaultMap
    ]:
        vars = {v.name: v for v in self._get_variables(self)}
        return (
            {vars[v.name]: f for v, f in pre.items()},
            {vars[v.name]: f for v, f in post.items()},
            {vars[v.name]: f for v, f in defs.items()})

    def __hash__(self) -> int:
        return hash(self.patterns)

    def get_id(self) -> SPARQL_Mapping.EntryId:
        """Gets the id of entry.

        Returns:
           Entry id.
        """
        return self.id

    def get_patterns(self) -> Sequence[SPARQL_Mapping.EntryPattern]:
        """Gets the patterns of entry.

        Returns:
           Entry patterns.
        """
        return self.patterns

    @property
    def variables(self) -> Set[Variable]:
        """The set of all variables occurring in entry patterns."""
        return self.get_variables()

    def get_variables(self) -> Set[Variable]:
        """Gets the set of all variables occurring in entry patterns.

        Returns:
           Set of variables.
        """
        return self._get_variables_cached(self)

    @classmethod
    @functools.cache
    def _get_variables_cached(cls, entry: _Entry) -> Set[Variable]:
        return cls._get_variables(entry)

    @classmethod
    def _get_variables(cls, entry: _Entry) -> Set[Variable]:
        ###
        # IMPORTANT: Call this version when inside entry's constructor.
        ###
        return frozenset(itertools.chain(*map(
            Term.get_variables, entry.patterns)))

    def get_preprocess_map(
            self
    ) -> SPARQL_Mapping.EntryCallbackArgProcessorMap:
        """Gets the callback-arg preprocessor map of entry.

        Returns:
           Callback-arg processor map.
        """
        return self.preprocess_map

    def get_postprocess_map(
            self
    ) -> SPARQL_Mapping.EntryCallbackArgProcessorMap:
        """Gets the callback-arg postprocessor map of entry.

        Returns:
           Callback-arg processor map.
        """
        return self.postprocess_map

    def get_default_map(
            self
    ) -> SPARQL_Mapping.EntryCallbackArgDefaultMap:
        """Gets the callback-arg defaults map of entry.

        Returns:
           Callback-arg defaults map.
        """
        return self.default_map

    def get_callback(self) -> SPARQL_Mapping.EntryCallback:
        """Gets the callback of entry.

        Returns:
           Entry callback.
        """
        return self.callback

    def preprocess(
            self,
            mapping: SPARQL_Mapping,
            compiler: Compiler,
            var: Variable,
            arg: SPARQL_Mapping.EntryCallbackArg
    ) -> SPARQL_Mapping.EntryCallbackArg:
        """Preprocesses entry callback `arg` corresponding to `var`.

        Parameters:
           mapping: SPARQL mapping.
           compiler: SPARQL compiler.
           var: Variable.
           arg: Entry callback argument.

        Returns:
           The resulting value.
        """
        return self._process(
            mapping, compiler, var, arg, self.preprocess_map)

    def postprocess(
            self,
            mapping: SPARQL_Mapping,
            compiler: Compiler,
            var: Variable,
            arg: SPARQL_Mapping.EntryCallbackArg
    ) -> SPARQL_Mapping.EntryCallbackArg:
        """Post-processes entry callback `arg` corresponding to `var`.

        Parameters:
           mapping: SPARQL mapping.
           compiler: SPARQL compiler.
           var: Variable.
           arg: Entry callback argument.

        Returns:
           The resulting value.
        """
        return self._process(
            mapping, compiler, var, arg, self.postprocess_map)

    def _process(
            self,
            mapping: SPARQL_Mapping,
            compiler: Compiler,
            var: Variable,
            arg: SPARQL_Mapping.EntryCallbackArg,
            target: SPARQL_Mapping.EntryCallbackArgProcessorMap
    ) -> SPARQL_Mapping.EntryCallbackArg:
        assert var in self.variables
        if var in target:
            try:
                return target[var](mapping, compiler, arg)
            except mapping.Done as done:
                return cast(
                    SPARQL_Mapping.EntryCallbackArg, done.args[0])
        else:
            return arg

    def match(
            self,
            pattern: SPARQL_Mapping.EntryPattern
    ) -> Iterator[tuple[SPARQL_Mapping.EntryPattern, Theta]]:
        """Matches `pattern` against entry.

        If no matches are found, returns an empty iterator.

        Parameters:
           pattern: Statement, statement template, or statement variable.

        Returns:
           An iterator of pairs "(matched-pattern, theta)".
        """
        for pat in self.patterns:
            theta = pattern.match(pat)
            if theta is not None:
                target = cast(
                    SPARQL_Mapping.EntryPattern,
                    pattern.instantiate(theta))
                assert target is not None
                yield target, {
                    v: v.instantiate(theta)
                    for v in pat._iterate_variables()}

    def match_and_preprocess(
            self,
            mapping: SPARQL_Mapping,
            compiler: Compiler,
            pattern: SPARQL_Mapping.EntryPattern,
            term2arg: Callable[[Term], Term | Compiler.Query.VTerm]
    ) -> Optional[tuple[
        Sequence[SPARQL_Mapping.EntryPattern],
        Theta,
        Mapping[str, SPARQL_Mapping.EntryCallbackArg]
    ]]:
        """Matches `pattern` against entry, then computes and
        preprocesses the corresponding callback arguments.

        If no matches are found, returns a triple with three empty
        components.

        Parameters:
           mapping: SPARQL mapping.
           compiler: SPARQL compiler.
           pattern: Statement, statement template, or statement variable.
           term2arg: Function to convert a term to a callback argument.

        Returns:
           A triple "(matched-patterns, theta, kwargs)" if successful;
           ``None`` otherwise.
        """
        targets: list[SPARQL_Mapping.EntryPattern] = []
        theta: dict[Variable, Term | None] = {}
        kwargs: dict[str, SPARQL_Mapping.EntryCallbackArg] = {}
        matches = list(self.match(pattern))
        if not matches:
            return None
        matched_target, matched_theta = zip(*matches)
        assert len(matched_target) == len(matched_theta)
        for i in range(len(matched_target)):
            try:
                for var, val in matched_theta[i].items():
                    arg: Optional[Union[Term, Compiler.Query.VTerm]]
                    if val is None:
                        arg = val
                    else:
                        arg = term2arg(val)
                    arg = self.preprocess(mapping, compiler, var, arg)
                    if var.name in kwargs:
                        ###
                        # IMPORTANT: An assertion failure here usually means
                        # the entry patterns are incorrectly specified.
                        ###
                        assert theta[var] == val
                        assert kwargs[var.name] == arg
                    else:
                        theta[var] = val
                        kwargs[var.name] = arg
            except SPARQL_Mapping.Skip:
                continue
            else:
                targets.append(matched_target[i])
        return targets, theta, kwargs

    def rename(
            self,
            exclude: Iterable[Term | str] = (),
            rename: Callable[[str], Iterator[str]] | None = None
    ) -> Self:
        """Copies entry renaming its variables.

        Picks name variants not occurring in `exclude`.

        Uses `rename` (if given) to generate name variants.

        Parameters:
           exclude: Name exclusion list.
           rename: Name variant generator.

        Returns:
           A copy of entry with its variables renamed.
        """
        tr = {v: v.rename(exclude, rename) for v in self.variables}
        patterns = cast(Iterable[SPARQL_Mapping.EntryPattern], list(map(
            functools.partial(Term.instantiate, theta=tr), self.patterns)))
        pre = {tr[k]: v for k, v in self.preprocess_map.items()}
        post = {tr[k]: v for k, v in self.postprocess_map.items()}
        defs = {tr[k]: v for k, v in self.default_map.items()}
        annots = copy.copy(self.annotations)
        ###
        # IMPORTANT: We need to rename the parameters of the original
        # callback.
        ###
        inv_tr_name = {v.name: u.name for u, v in tr.items()}

        def callback(*args: Any, **kwargs: Any) -> None:
            return self.callback(*args, **{
                inv_tr_name[k]: v for k, v in kwargs.items()})
        return type(self)(self.id, patterns, pre, post, defs, annots, cast(
            SPARQL_Mapping.EntryCallback, callback))


class SPARQL_Mapping(Sequence[_Entry]):
    """SPARQL mapping."""

    #: The type of SPARQL mapping entries.
    Entry: TypeAlias = _Entry

    #: The type of entry ids.
    EntryId: TypeAlias = int

    #: The type of entry patterns.
    EntryPattern: TypeAlias = VStatement

    #: The type of things coercible to entry patterns.
    EntryTPattern: TypeAlias = VTStatement

    #: The type of entry callback argument.
    EntryCallbackArg: TypeAlias =\
        Optional[Union[Term, 'Compiler.Query.VTerm']]

    #: The type of entry callback-arg processor maps.
    EntryCallbackArgProcessorMap: TypeAlias =\
        Mapping[Variable, 'SPARQL_Mapping.EntryCallbackArgProcessor']

    #: The type of entry callback-arg default map.
    EntryCallbackArgDefaultMap: TypeAlias =\
        Mapping[Variable, Optional[Term]]

    class EntryCallbackArgProcessor:
        """Entry callback-arg processor."""

        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            return arg

        def or_(
                self,
                p: SPARQL_Mapping.EntryCallbackArgProcessor,
                *ps: SPARQL_Mapping.EntryCallbackArgProcessor
        ) -> SPARQL_Mapping.EntryCallbackArgProcessorChain:
            return self.chain(p, *ps, disjunctive=True)

        def __or__(
                self,
                other: SPARQL_Mapping.EntryCallbackArgProcessor
        ) -> SPARQL_Mapping.EntryCallbackArgProcessorChain:
            return self.or_(other)

        def chain(
                self,
                p: SPARQL_Mapping.EntryCallbackArgProcessor,
                *ps: SPARQL_Mapping.EntryCallbackArgProcessor,
                disjunctive: bool = False
        ) -> SPARQL_Mapping.EntryCallbackArgProcessorChain:
            return SPARQL_Mapping.EntryCallbackArgProcessorChain(
                self, p, *ps, disjunctive=disjunctive)

        def __rshift__(
                self,
                other: SPARQL_Mapping.EntryCallbackArgProcessor
        ) -> SPARQL_Mapping.EntryCallbackArgProcessorChain:
            return self.chain(other)

    class EntryCallbackArgProcessorAlias(Protocol):
        """The type of callback-arg processor aliases."""

        def __call__(
                self,
                *args: Any,
                **kwargs: Any
        ) -> SPARQL_Mapping.EntryCallbackArgProcessor:
            ...

    class EntryCallbackArgProcessorChain(EntryCallbackArgProcessor):
        """Entry callback-arg processor chain."""

        __slots__ = (
            '_chain',
            '_disjunctive',
        )

        _chain: Sequence[SPARQL_Mapping.EntryCallbackArgProcessor]
        _disjunctive: bool

        def __init__(
                self,
                p: SPARQL_Mapping.EntryCallbackArgProcessor,
                *ps: SPARQL_Mapping.EntryCallbackArgProcessor,
                disjunctive: bool = False
        ):
            self._chain = (p, *ps)
            self._disjunctive = disjunctive

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            n = 0
            for p in self._chain:
                try:
                    arg = p(m, c, arg)
                    n += 1
                except SPARQL_Mapping.Skip as skip:
                    if not self._disjunctive:
                        raise skip
            if n == 0:
                raise SPARQL_Mapping.Skip
            return arg

    class EntryCallback(Protocol):
        """The type of entry callbacks."""

        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                *args: SPARQL_Mapping.EntryCallbackArg
        ) -> None:
            ...

# -- Entry -----------------------------------------------------------------

    #: The registered entries indexed by id.
    _entries: ClassVar[Sequence[_Entry]]

    #: Entries to be registered by the next __init_subclass__() call.
    _scheduled_entries: ClassVar[MutableSequence[tuple[
        SPARQL_Mapping.EntryId,
        Iterable[SPARQL_Mapping.EntryPattern],
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallbackArgDefaultMap,
        Statement.Annotation | None,
        SPARQL_Mapping.EntryCallback
    ]]] = []

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._entries = [
            cls.Entry(id, pats, pre, post, defs, annots, f)
            for id, pats, pre, post, defs, annots, f
            in SPARQL_Mapping._scheduled_entries]
        SPARQL_Mapping._scheduled_entries = []

    @classmethod
    def register(
            cls,
            patterns: Iterable[SPARQL_Mapping.EntryTPattern],
            preprocess:
            SPARQL_Mapping.EntryCallbackArgProcessorMap | None = None,
            postprocess:
            SPARQL_Mapping.EntryCallbackArgProcessorMap | None = None,
            defaults:
            SPARQL_Mapping.EntryCallbackArgDefaultMap | None = None,
            qualifiers: TQualifierRecord | None = None,
            references: TReferenceRecordSet | None = None,
            rank: TRank | None = None
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           patterns: Statements, statement templates, or statement variables.
           preprocess: Callback-arg pre-processor map.
           postprocess: Callback-arg post-processor map.
           defaults: Callback-arg default map.
           qualifiers: Qualifiers to be added to statement patterns.
           references: References to be added to statement patterns.
           rank: Rank to be added to statement patterns.

        Returns:
           The wrapped callback.
        """
        pats: list[SPARQL_Mapping.EntryPattern] = []
        seen: dict[str, Variable] = {}
        for pat in patterns:
            xpat: Union[Statement, StatementTemplate, StatementVariable]
            if isinstance(pat, Template):
                xpat = StatementTemplate.check(
                    pat, cls.register, 'patterns', 1)
            elif isinstance(pat, Variable):
                xpat = StatementVariable.check(
                    pat, cls.register, 'patterns', 1)
            else:
                xpat = Statement.check(pat, cls.register, 'patterns', 1)
            pats.append(xpat)
            for var in xpat.variables:
                if var.name not in seen:
                    seen[var.name] = var
                elif seen[var.name] != var:
                    raise KIF_Object._arg_error(
                        f"incompatible occurrences of variable '{var.name}'",
                        cls.register, 'patterns', 1, ValueError)
        pre = KIF_Object._check_optional_arg_isinstance(
            preprocess, Mapping, {}, cls.register, 'preprocess', 2)
        assert pre is not None
        post = KIF_Object._check_optional_arg_isinstance(
            postprocess, Mapping, {}, cls.register, 'postprocess', 3)
        assert post is not None
        defs = KIF_Object._check_optional_arg_isinstance(
            defaults, Mapping, {}, cls.register, 'defaults', 4)
        assert defs is not None
        qualifiers = QualifierRecord.check_optional(
            qualifiers, None, cls.register, 'qualifiers', 5)
        references = ReferenceRecordSet.check_optional(
            references, None, cls.register, 'references', 6)
        rank = Rank.check_optional(
            rank, None, cls.register, 'rank', 7)
        if qualifiers is None and references is None and rank is None:
            annots: Optional[Statement.Annotation] = None
        else:
            annots = {
                'qualifiers': qualifiers,
                'references': references,
                'rank': rank,
            }
        ###
        # TODO: Rename variables in `patterns` to avoid conflicts.
        # (The input pattern might contain homonymous variables.)
        ###

        def wrapper(f):
            cls._scheduled_entries.append(
                (len(cls._scheduled_entries),
                 pats, pre, post, defs, annots, f))
            return f
        return wrapper

    class Signal(BaseException):
        """Base class for entry signals."""

    class Done(Signal):
        """The "done" signal."""

    class Skip(Signal):
        """The "skip" signal."""

# -- Entry callback-arg processors -----------------------------------------

    class CheckStr(EntryCallbackArgProcessor):
        """Checks str argument."""

        __slots__ = (
            'subclass',
            'optional',
            'coerce',
            'startswith',
            'endswith',
            'replace_prefix',
            'replace_suffix',
            'match',
            'sub',
            'tr',
        )

        #: Expected subclass.
        subclass: type[str]

        #: Whether arg is optional.
        optional: bool

        #: Target type to coerce arg to.
        coerce: type[str] | None

        #: Prefix to match.
        startswith: str | None

        #: Suffix to match.
        endswith: str | None

        #: Prefix to match plus replacement.
        replace_prefix: tuple[str, str] | None

        #: Suffix to match plus replacement.
        replace_suffix: tuple[str, str] | None

        #: Regex to match.
        match: re.Pattern | None

        #: Regex to match and template to substitute.
        sub: tuple[re.Pattern, str] | None

        #: Character translation table.
        tr: Mapping[str, str] | None

        def __init__(
                self,
                subclass: type[str] | None = None,
                optional: bool | None = None,
                coerce: type[str] | None = None,
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None,
                tr: Mapping[str, str] | None = None
        ) -> None:
            self.subclass = subclass or str
            self.optional = optional if optional is not None else False
            self.coerce = coerce
            self.startswith = startswith
            self.endswith = endswith
            self.replace_prefix = replace_prefix
            self.replace_suffix = replace_suffix
            if match is not None:
                self.match = re.compile(match)
            else:
                self.match = None
            if sub is not None:
                self.sub = (re.compile(sub[0]), sub[1])
            else:
                self.sub = None
            if tr is not None:
                self.tr = tr
            else:
                self.tr = None

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if (isinstance(arg, c.query.Variable)
                    or (arg is None and self.optional)):
                raise m.Done(arg)
            elif not isinstance(arg, str):
                raise m.Skip
            assert isinstance(arg, str)
            if not issubclass(type(arg), self.subclass):
                raise m.Skip
            if self.coerce is not None:
                arg = self.coerce(arg)  # type: ignore
            assert isinstance(arg, str)
            if self.startswith and not arg.startswith(self.startswith):
                raise m.Skip
            if self.endswith and not arg.endswith(self.endswith):
                raise m.Skip
            if self.replace_prefix is not None:
                old, new = self.replace_prefix
                arg = type(arg)(new + arg.removeprefix(old))
            if self.replace_suffix is not None:
                old, new = self.replace_suffix
                arg = type(arg)(arg.removesuffix(old) + new)
            if self.match is not None and not self.match.match(arg):
                raise m.Skip
            if self.sub is not None:
                match = self.sub[0].match(arg)
                if not match:
                    raise m.Skip
                else:
                    arg = type(arg)(match.expand(self.sub[1]))
            if self.tr is not None:
                arg = type(arg)(''.join(
                    map(lambda c: self.tr.get(c, c), arg)))  # type: ignore
            return arg

    class CheckLiteral(CheckStr):
        """Checks literal argument."""

        __slots__ = (
            'set_language',
            'set_datatype',
        )

        #: Language to set.
        set_language: str | None

        #: Datatypep to set.
        set_datatype: str | None

        def __init__(
                self,
                optional: bool | None = None,
                coerce: type[str] | None = None,
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None,
                tr: Mapping[str, str] | None = None,
                set_language: str | None = None,
                set_datatype: str | None = None
        ) -> None:
            from ..filter_compiler import SPARQL_FilterCompiler
            super().__init__(
                subclass=SPARQL_FilterCompiler.Query.Literal,
                optional=optional,
                coerce=coerce,
                startswith=startswith,
                endswith=endswith,
                replace_prefix=replace_prefix,
                replace_suffix=replace_suffix,
                match=match,
                sub=sub,
                tr=tr)
            self.set_language = set_language
            self.set_datatype = set_datatype

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            arg = super().__call__(m, c, arg)
            assert isinstance(arg, c.Query.Literal)
            if self.set_language is not None:
                arg = c.Query.Literal(arg, self.set_language)
            if self.set_datatype is not None:
                arg = c.Query.Literal(arg, datatype=self.set_datatype)
            return arg

    class CheckInt(CheckLiteral):
        """Checks int argument."""

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            arg = super().__call__(m, c, arg)
            assert isinstance(arg, c.Query.Literal)
            try:
                return c.Query.Literal(int(arg))
            except ValueError:
                raise m.Skip

    class CheckURI(CheckStr):
        """Check URI argument."""

        def __init__(
                self,
                optional: bool | None = None,
                coerce: type[str] | None = None,
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None,
                tr: Mapping[str, str] | None = None
        ) -> None:
            from ..filter_compiler import SPARQL_FilterCompiler
            super().__init__(
                subclass=SPARQL_FilterCompiler.Query.URI,
                optional=optional,
                coerce=coerce,
                startswith=startswith,
                replace_prefix=replace_prefix,
                replace_suffix=replace_suffix,
                endswith=endswith,
                match=match,
                sub=sub,
                tr=tr)

# -- Methods ---------------------------------------------------------------

    @property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Returns:
           Context.
        """
        return Context.top(context)

    @overload
    def __getitem__(self, k: int) -> _Entry:
        ...

    @overload
    def __getitem__(self, k: slice) -> Sequence[_Entry]:
        ...

    def __getitem__(self, k: Any) -> Any:
        return self._entries[k]

    def __len__(self) -> int:
        return len(self._entries)

    def frame_pushed(
            self,
            compiler: Compiler,
            frame: Compiler.Frame
    ) -> Compiler.Frame:
        """Called before a new compilation frame is pushed.

        Returns:
           The frame to be pushed.
        """
        return frame

    def frame_popped(
            self,
            compiler: Compiler,
            frame: Compiler.Frame
    ) -> Compiler.Frame:
        """Called the current compilation frame is popped.

        Returns:
           The popped frame.
        """
        return frame

    def preamble(
            self,
            compiler: Compiler,
            sources: Iterable[SPARQL_Mapping.EntryPattern]
    ) -> Iterable[SPARQL_Mapping.EntryPattern]:
        """Called before compilation starts.

        Parameters:
           compiler: SPARQL compiler.
           pattern: Source patterns.

        Returns:
           Source patterns.
        """
        return sources

    def preamble_entry(
            self,
            compiler: Compiler,
            entry: SPARQL_Mapping.Entry
    ) -> SPARQL_Mapping.Entry:
        """Called before entry compilation starts.

        Parameters:
           entry: Entry.

        Returns:
           Entry.
        """
        return entry

    def postamble(
            self,
            compiler: Compiler,
            targets: Iterable[SPARQL_Mapping.EntryPattern]
    ) -> None:
        """Called after compilation ends.

        Parameters:
           compiler: SPARQL compiler.
           targets: Target patterns.
        """

    def build_query(
            self,
            compiler: Compiler,
            distinct: bool | None = None,
            limit: int | None = None,
            offset: int | None = None
    ) -> Compiler.Query:
        """Constructs a filter query.

        Parameters:
           compiler: SPARQL compiler.
           distinct: Whether to enable the distinct modifier.
           limit: Limit.
           offset: Offset.

        Returns:
           Filter query.
        """
        return compiler.q.select(    # type: ignore
            distinct=distinct, limit=limit, offset=offset)

    def build_results(
            self,
            compiler: Compiler
    ) -> SPARQL_Mapping.ResultBuilder:
        """Constructs a compilation result builder.

        Parameters:
           compiler: SPARQL compiler.

        Returns:
           Result builder.
        """
        return self.ResultBuilder(self, compiler)

    class ResultBuilder:
        """Result builder for SPARQL mapping.

        Parameters:
           mapping: SPARQL mapping.
           compiler: SPARQL compiler.
        """

        #: The parent mapping.
        mapping: SPARQL_Mapping

        #: The SPARQL compiler.
        compiler: Compiler

        def __init__(
                self,
                mapping: SPARQL_Mapping,
                compiler: Compiler
        ) -> None:
            self.mapping = mapping
            self.compiler = compiler

        @property
        def c(self) -> Compiler:
            return self.compiler

        def push(self, binding: SPARQL_ResultsBinding) -> Iterator[Theta]:
            """Pushes SPARQL binding into result builder.

            Parameters:
               binding: SPARQL binding.

            Returns:
               An iterator of thetas.
            """
            if binding:
                return self.c._binding_to_thetas(binding)
            else:
                return iter(())


register = SPARQL_Mapping.register
