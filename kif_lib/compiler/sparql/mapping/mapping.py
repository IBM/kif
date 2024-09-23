# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses
import re
from typing import TYPE_CHECKING

from ....model import (
    KIF_Object,
    Statement,
    StatementTemplate,
    StatementVariable,
    Template,
    Term,
    Theta,
    Variable,
    VStatement,
    VTStatement,
)
from ....namespace import Wikidata
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
    TypeAlias,
    Union,
)

if TYPE_CHECKING:  # pragma: no cover
    from ..compiler import SPARQL_Compiler


class SPARQL_Mapping(Mapping):
    """SPARQL mapping."""

    #: The type of entry ids.
    EntryId: TypeAlias = str

    #: The type of entry patterns.
    EntryPattern: TypeAlias = VStatement

    #: The type of things coercible to entry patterns.
    EntryTPattern: TypeAlias = VTStatement

    #: The type of entry callback argument.
    EntryCallbackArg: TypeAlias =\
        Optional[Union[Term, 'SPARQL_Compiler.Query.VTerm']]

    #: The type of entry callback-arg processor maps.
    EntryCallbackArgProcessorMap: TypeAlias =\
        Mapping[Variable, 'SPARQL_Mapping.EntryCallbackArgProcessor']

    class EntryCallbackArgProcessor:
        """Entry callback-arg processor."""

        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            return arg

        def __rshift__(
                self,
                other: SPARQL_Mapping.EntryCallbackArgProcessor
        ) -> SPARQL_Mapping.EntryCallbackArgProcessorChain:
            return SPARQL_Mapping.EntryCallbackArgProcessorChain(
                self, other)

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
            'chain',
        )

        chain: Sequence[SPARQL_Mapping.EntryCallbackArgProcessor]

        def __init__(
                self,
                p1: SPARQL_Mapping.EntryCallbackArgProcessor,
                *ps: SPARQL_Mapping.EntryCallbackArgProcessor):
            self._chain = (p1, *ps)

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            for p in self._chain:
                arg = p(m, c, arg)
            return arg

    class EntryCallback(Protocol):
        """The type of entry callbacks."""

        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                *args: SPARQL_Mapping.EntryCallbackArg
        ) -> None:
            ...

# -- Entry -----------------------------------------------------------------

    @dataclasses.dataclass
    class Entry:
        """Entry in SPARQL mapping."""

        #: The pattern of entry.
        pattern: SPARQL_Mapping.EntryPattern

        #: The callback-arg preprocessor map of entry.
        preprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap

        #: The callback-arg postprocessor map of entry.
        postprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap

        #: The (compilation) callback of entry.
        callback: SPARQL_Mapping.EntryCallback

        def __init__(
                self,
                pattern: SPARQL_Mapping.EntryPattern,
                preprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap,
                postprocess_map: SPARQL_Mapping.EntryCallbackArgProcessorMap,
                callback: SPARQL_Mapping.EntryCallback
        ) -> None:
            self.pattern = pattern
            self.preprocess_map, self.postprocess_map =\
                self._init_processor_maps(preprocess_map, postprocess_map)
            self.callback = callback

        def _init_processor_maps(
                self,
                pre: SPARQL_Mapping.EntryCallbackArgProcessorMap,
                post: SPARQL_Mapping.EntryCallbackArgProcessorMap
        ) -> tuple[
            SPARQL_Mapping.EntryCallbackArgProcessorMap,
            SPARQL_Mapping.EntryCallbackArgProcessorMap
        ]:
            vars = {v.name: v for v in self.pattern.variables}
            return (
                {vars[v.name]: f for v, f in pre.items()},
                {vars[v.name]: f for v, f in post.items()})

        @property
        def id(self) -> SPARQL_Mapping.EntryId:
            """The id of entry."""
            return self.get_id()

        def get_id(self) -> SPARQL_Mapping.EntryId:
            """Gets the id of entry.

            Returns:
               Entry id.
            """
            return self.pattern.digest

        def get_pattern(self) -> SPARQL_Mapping.EntryPattern:
            """Gets the pattern of entry.

            Returns:
               Entry pattern.
            """
            return self.pattern

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

        def get_callback(self) -> SPARQL_Mapping.EntryCallback:
            """Gets the callback of entry.

            Returns:
               Entry callback.
            """
            return self.callback

        def preprocess(
                self,
                mapping: SPARQL_Mapping,
                compiler: SPARQL_Compiler,
                var: Variable,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            """Preprocess entry callback `arg` corresponding to `var`.

            Parameters:
               arg: Entry callback argument.

            Returns:
               The resulting value.
            """
            return self._process(
                mapping, compiler, var, arg, self.preprocess_map)

        def postprocess(
                self,
                mapping: SPARQL_Mapping,
                compiler: SPARQL_Compiler,
                var: Variable,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            """Postprocess entry callback `arg` corresponding to `var`.

            Parameters:
               arg: Entry callback argument.

            Returns:
               The resulting value.
            """
            return self._process(
                mapping, compiler, var, arg, self.postprocess_map)

        def _process(
                self,
                mapping: SPARQL_Mapping,
                compiler: SPARQL_Compiler,
                var: Variable,
                arg: SPARQL_Mapping.EntryCallbackArg,
                target: SPARQL_Mapping.EntryCallbackArgProcessorMap
        ) -> SPARQL_Mapping.EntryCallbackArg:
            assert var in self.pattern.variables
            if var in target:
                try:
                    return target[var](mapping, compiler, arg)
                except mapping.Done as done:
                    return cast(
                        SPARQL_Mapping.EntryCallbackArg, done.args[0])
            else:
                return arg

        def rename(
                self,
                exclude: Iterable[Term | str] = (),
                generator: Callable[[str], Iterator[str]] | None = None
        ) -> Self:
            """Copies entry and rename its variables.

            Parameters:
               exclude: Exclusion list.
               generate: Name generator.

            Returns:
               A copy of entry with its variables renamed.
            """
            pattern = self.pattern.rename(exclude, generator)
            tr = dict(zip(
                self.pattern._iterate_variables(),
                pattern._iterate_variables()))
            pre = {tr[k]: v for k, v in self.preprocess_map.items()}
            post = {tr[k]: v for k, v in self.postprocess_map.items()}
            callback = self.callback
            return self.__class__(pattern, pre, post, callback)

    #: The registered entries indexed by id (digest of pattern).
    _entries: ClassVar[Mapping[
        SPARQL_Mapping.EntryId, SPARQL_Mapping.Entry]]

    #: Entries to be registered by the next __init_subclass__() call.
    _scheduled_entries: ClassVar[MutableSequence[tuple[
        SPARQL_Mapping.EntryPattern,
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallbackArgProcessorMap,
        SPARQL_Mapping.EntryCallback,
    ]]] = []

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._entries = {
            pat.digest: cls.Entry(pat, pre, post, f)
            for pat, pre, post, f in SPARQL_Mapping._scheduled_entries}
        SPARQL_Mapping._scheduled_entries = []

    @classmethod
    def register(
            cls,
            pattern: SPARQL_Mapping.EntryTPattern,
            preprocess:
            SPARQL_Mapping.EntryCallbackArgProcessorMap | None = None,
            postprocess:
            SPARQL_Mapping.EntryCallbackArgProcessorMap | None = None
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           pattern: Statement, statement template, or statement variable.
           preprocess: Callback-arg processor map.
           postprocess: Callback-arg processor map.

        Returns:
           The wrapped callback.
        """
        pat: SPARQL_Mapping.EntryPattern
        if isinstance(pattern, Template):
            pat = StatementTemplate.check(pattern, cls.register, 'pattern', 1)
        elif isinstance(pattern, Variable):
            pat = StatementVariable.check(pattern, cls.register, 'pattern', 1)
        else:
            pat = Statement.check(pattern, cls.register, 'pattern', 1)
        pre = KIF_Object._check_optional_arg_isinstance(
            preprocess, Mapping, {}, cls.register, 'preprocess', 2)
        assert pre is not None
        post = KIF_Object._check_optional_arg_isinstance(
            postprocess, Mapping, {}, cls.register, 'postprocess', 3)
        assert post is not None
        ###
        # TODO: Rename variables in `pat` to avoid conflicts.
        # (The input pattern might contain homonymous variables.)
        ###

        def wrapper(f):
            cls._scheduled_entries.append((pat, pre, post, f))
            return f
        return wrapper

    class Signal(BaseException):
        """Base class for entry signals."""

    class Skip(Signal):
        """The "skip" signal."""

    class Done(Signal):
        """The "done" signal."""

# -- Callback-Arg Processors -----------------------------------------------

    class CheckStr(EntryCallbackArgProcessor):
        """Checks str argument."""

        __slots__ = (
            'subclass',
            'startswith',
            'endswith',
            'match',
        )

        #: Expected subclass.
        subclass: type[str]

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

        def __init__(
                self,
                subclass: type[str] | None = None,
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None
        ) -> None:
            self.subclass = subclass or str
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

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if isinstance(arg, c.query.Variable):
                raise m.Done(arg)
            elif not isinstance(arg, str):
                raise m.Skip
            assert isinstance(arg, str)
            if not issubclass(type(arg), self.subclass):
                raise m.Skip
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
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None,
                set_language: str | None = None,
                set_datatype: str | None = None
        ) -> None:
            from ..compiler import SPARQL_Compiler
            super().__init__(
                subclass=SPARQL_Compiler.Query.Literal,
                startswith=startswith,
                endswith=endswith,
                replace_prefix=replace_prefix,
                replace_suffix=replace_suffix,
                match=match,
                sub=sub)
            self.set_language = set_language
            self.set_datatype = set_datatype

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            arg = super().__call__(m, c, arg)
            assert isinstance(arg, c.Query.Literal)
            if self.set_language is not None:
                arg = c.Query.Literal(arg, self.set_language)
            if self.set_datatype is not None:
                arg = c.Query.Literal(arg, datatype=self.set_datatype)
            return arg

    class CheckURI(CheckStr):
        """Check URI argument."""

        def __init__(
                self,
                startswith: str | None = None,
                endswith: str | None = None,
                replace_prefix: tuple[str, str] | None = None,
                replace_suffix: tuple[str, str] | None = None,
                match: str | re.Pattern | None = None,
                sub: tuple[str | re.Pattern, str] | None = None
        ) -> None:
            from ..compiler import SPARQL_Compiler
            super().__init__(
                subclass=SPARQL_Compiler.Query.URI,
                startswith=startswith,
                replace_prefix=replace_prefix,
                replace_suffix=replace_suffix,
                endswith=endswith,
                match=match,
                sub=sub)

    class CheckPrefix(EntryCallbackArgProcessor):
        """Checks whether argument has prefix."""

        __slots__ = (
            '_prefix',
        )

        _prefix: str

        def __init__(self, prefix: str) -> None:
            self._prefix = prefix

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if (isinstance(arg, (c.Query.Literal, c.Query.URI))
                    and not arg.startswith(self._prefix)):
                raise SPARQL_Mapping.Skip
            else:
                return arg

    class UpdatePrefix(CheckPrefix):
        """Updates argument prefix."""

        __slots__ = (
            '_new',
        )

        _update: str

        def __init__(self, old: str, new: str):
            super().__init__(old)
            self._new = new

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if isinstance(arg, (c.Query.Literal, c.Query.URI)):
                arg = super().__call__(m, c, arg)
                assert isinstance(arg, str)
                return type(arg)(self._new + arg.removeprefix(self._prefix))
            else:
                return arg

    class CheckRegex(EntryCallbackArgProcessor):
        """Check whether argument matches regex."""

        __slots__ = (
            '_regex',
        )

        _regex: re.Pattern

        def __init__(self, regex: str | re.Pattern) -> None:
            if isinstance(regex, str):
                self._regex = re.compile(regex)
            else:
                self._regex = regex

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if (isinstance(arg, (c.Query.Literal, c.Query.URI))
                    and not self._regex.match(arg)):
                raise SPARQL_Mapping.Skip
            else:
                return arg

    class CheckWikidataItem(CheckRegex):
        """Checks whether argument matches the URI of a Wikidata item."""

        def __init__(self):
            super().__init__(
                f'^{re.escape(Wikidata.WD)}Q[1-9][0-9]+$')

# -- Methods ---------------------------------------------------------------

    def __getitem__(
            self,
            k: SPARQL_Mapping.EntryId | SPARQL_Mapping.EntryPattern
    ) -> SPARQL_Mapping.Entry:
        if isinstance(k, KIF_Object):
            k = k.digest
        return self._entries[k]

    def __iter__(self) -> Iterator[SPARQL_Mapping.EntryPattern]:
        return iter(map(self.Entry.get_pattern, self._entries.values()))

    def __len__(self) -> int:
        return len(self._entries)

    def match(
            self,
            pattern: SPARQL_Mapping.EntryPattern,
            rename: Callable[[str], Iterator[str]] | None = None
    ) -> Iterator[tuple[
            SPARQL_Mapping.EntryPattern, Theta, SPARQL_Mapping.Entry]]:
        """Searches for entries matching `pattern`.

        If `rename` is given, renames entry using `rename` before computing
        the match.

        Parameters:
           pattern: Statement, statement template, or statement variable.
           rename: Name generator.

        Returns:
           An iterator of triples "(pattern, theta, entry)".
        """
        for _, entry in self._entries.items():
            if rename is not None:
                entry = entry.rename(generator=rename)
            theta = pattern.match(entry.pattern)
            if theta is None:
                continue
            target = pattern.instantiate(theta)
            assert target is not None
            yield (
                cast(SPARQL_Mapping.EntryPattern, target),
                {v: v.instantiate(theta)
                 for v in entry.pattern._iterate_variables()},
                entry)


register = SPARQL_Mapping.register
