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
    Literal,
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

    #: The type of entry callback-arg preprocessor maps.
    EntryCallbackArgPreprocessorMap: TypeAlias =\
        Mapping[Variable, 'SPARQL_Mapping.EntryCallbackArgPreprocessor']

    class EntryCallbackArgPreprocessor:
        """Entry callback-arg preprocessor."""

        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            return arg

        def __rshift__(
                self,
                other: SPARQL_Mapping.EntryCallbackArgPreprocessor
        ) -> SPARQL_Mapping.EntryCallbackArgPreprocessorChain:
            return SPARQL_Mapping.EntryCallbackArgPreprocessorChain(
                self, other)

    class EntryCallbackArgPreprocessorChain(EntryCallbackArgPreprocessor):
        """Entry callback-arg preprocessor chain."""

        __slots__ = (
            '_chain',
        )

        _chain: Sequence[SPARQL_Mapping.EntryCallbackArgPreprocessor]

        def __init__(
                self,
                p1: SPARQL_Mapping.EntryCallbackArgPreprocessor,
                p2: SPARQL_Mapping.EntryCallbackArgPreprocessor,
                *ps: SPARQL_Mapping.EntryCallbackArgPreprocessor):
            self._chain = (p1, p2, *ps)

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

    @dataclasses.dataclass
    class Entry:
        """Entry in SPARQL mapping."""

        #: The pattern of entry.
        pattern: SPARQL_Mapping.EntryPattern

        #: The callback-arg preprocessor map of entry.
        preprocess_map: SPARQL_Mapping.EntryCallbackArgPreprocessorMap

        #: The (compilation) callback of entry.
        callback: SPARQL_Mapping.EntryCallback

        def __init__(
                self,
                pattern: SPARQL_Mapping.EntryPattern,
                preprocess_map: SPARQL_Mapping.EntryCallbackArgPreprocessorMap,
                callback: SPARQL_Mapping.EntryCallback
        ) -> None:
            self.pattern = pattern
            pattern_variables = {v.name: v for v in pattern.variables}
            self.preprocess_map = {}
            for v, f in preprocess_map.items():
                assert v.name in pattern_variables
                self.preprocess_map[pattern_variables[v.name]] = f
            self.callback = callback

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
        ) -> SPARQL_Mapping.EntryCallbackArgPreprocessorMap:
            """Gets the callback-arg preprocessor map of entry.

            Returns:
               Preprocessor map.
            """
            return self.preprocess_map

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
            assert var in self.pattern.variables
            if var not in self.preprocess_map:
                return arg
            else:
                return self.preprocess_map[var](mapping, compiler, arg)

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
            preproc = {tr[k]: v for k, v in self.preprocess_map.items()}
            callback = self.callback
            return self.__class__(pattern, preproc, callback)

    class Skip(BaseException):
        """Skip the current entry."""

    #: The registered entries indexed by id (digest of pattern).
    _entries: ClassVar[Mapping[
        SPARQL_Mapping.EntryId, SPARQL_Mapping.Entry]]

    #: Entries to be registered by the next __init_subclass__() call.
    _scheduled_entries: ClassVar[MutableSequence[tuple[
        SPARQL_Mapping.EntryPattern,
        SPARQL_Mapping.EntryCallbackArgPreprocessorMap,
        SPARQL_Mapping.EntryCallback,
    ]]] = []

    @classmethod
    def __init_subclass__(cls) -> None:
        cls._entries = {
            pat.digest: cls.Entry(pat, preproc, f)
            for pat, preproc, f in SPARQL_Mapping._scheduled_entries}
        SPARQL_Mapping._scheduled_entries = []

    class PatchLiteral(EntryCallbackArgPreprocessor):
        """Patches language tag or datatype of literal argument."""

        __slots__ = (
            '_language',
            '_datatype',
        )

        _language: str | Literal[False] | None
        _literal: str | Literal[False] | None

        def __init__(
                self,
                language: str | Literal[False] | None = None,
                datatype: str | Literal[False] | None = None
        ):
            self._language = language
            self._datatype = datatype

        @override
        def __call__(
                self,
                m: SPARQL_Mapping,
                c: SPARQL_Compiler,
                arg: SPARQL_Mapping.EntryCallbackArg
        ) -> SPARQL_Mapping.EntryCallbackArg:
            if isinstance(arg, c.Query.Literal):
                if self._language is False:
                    language: Optional[str] = None
                elif self._language is None:
                    language = arg.language
                else:
                    assert isinstance(self._language, str)
                    language = self._language
                if self._datatype is False:
                    datatype: Optional[str] = None
                elif self._datatype is None:
                    datatype = arg.datatype
                else:
                    assert isinstance(self._datatype, str)
                    datatype = self._datatype
                return c.literal(str(arg), language, datatype=datatype)
            else:
                return arg

    class CheckPrefix(EntryCallbackArgPreprocessor):
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

    class CheckRegex(EntryCallbackArgPreprocessor):
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

    @classmethod
    def register(
            cls,
            pattern: SPARQL_Mapping.EntryTPattern,
            preprocess: Optional[
                SPARQL_Mapping.EntryCallbackArgPreprocessorMap] = None,
    ) -> Callable[..., Any]:
        """Decorator used to register a new entry into mapping.

        Parameters:
           pattern: Statement, statement template, or statement variable.
           preprocess: Callback-arg preprocessor map.

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
        preproc = KIF_Object._check_optional_arg_isinstance(
            preprocess, Mapping, {}, cls.register, 'preprocess', 2)
        assert preproc is not None
        ###
        # TODO: Rename variables in `pat` to avoid conflicts.
        ###

        def wrapper(f):
            cls._scheduled_entries.append((pat, preproc, f))
            return f
        return wrapper

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
