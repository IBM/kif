# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import enum
import itertools
import keyword
import re
import string
import typing as ty


class Str2Id:
    """Converts arbitrary string to a Python-like identifier."""

    _NONE = object()

    class Preprocess(enum.Flag):
        OPERATORS = enum.auto()
        UTC = enum.auto()
        ALL = OPERATORS | UTC

    _dash: str = '-–—‑'

    _punctuation: str = string.punctuation.translate(str.maketrans(
        dict(zip('_+-/=%&', itertools.repeat('')))))  # type: ignore

    _punctuation_extra: str = '‘’¡'

    _subscript_digit_tr: dict[str, str] =\
        dict(zip('₀₁₂₃₄₅₆₇₈₉', map(str, range(10))))

    _superscript_digit_tr: dict[str, str] =\
        dict(zip('⁰¹²³⁴⁵⁶⁷⁸⁹', map(str, range(10))))

    _symbol_name_tr: dict[str, str] = {
        '%': 'percent',
        '&': 'and',
        '+': 'plus',
        '/': '_',
        '=': 'equals',
        '°': 'degree',
        '±': 'plus-minus',
        '×': 'times',
        '∆': 'Delta',
        '−': 'minus',
    }

    _vulgar_fraction_name_tr: dict[str, str] = {
        '½': 'one-half',
        '⅓': 'one-third',
        '¼': 'one-quarter',
        '⅕': 'one-fifth',
        '⅙': 'one-sixth',
        '⅐': 'one-seventh',
        '⅛': 'one-eighth',
        '⅑': 'one-ninth',
        '⅒': 'one-tenth',
    }

    _whitespace: str = string.whitespace + ' '

    __slots__ = (
        'preprocess',
        'tr',
    )

    #: Preprocess flags.
    preprocess: Str2Id.Preprocess

    #: Translation table.
    tr: ty.Any

    def __init__(
            self,
            preprocess: Preprocess | None = None,
            dash: str | None = None,
            punctuation: str | None = None,
            punctuation_extra: str | None = None,
            subscript_digit_tr: dict[str, str] | None = None,
            superscript_digit_tr: dict[str, str] | None = None,
            symbol_name_tr: dict[str, str] | None = None,
            vulgar_fraction_name_tr: dict[str, str] | None = None,
            whitespace: str | None = None,
    ) -> None:
        if dash is None:
            dash = self._dash
        if punctuation is None:
            punctuation = self._punctuation
        if punctuation_extra is None:
            punctuation_extra = self._punctuation_extra
        if subscript_digit_tr is None:
            subscript_digit_tr = self._subscript_digit_tr
        if superscript_digit_tr is None:
            superscript_digit_tr = self._superscript_digit_tr
        if symbol_name_tr is None:
            symbol_name_tr = self._symbol_name_tr
        if vulgar_fraction_name_tr is None:
            vulgar_fraction_name_tr = self._vulgar_fraction_name_tr
        if whitespace is None:
            whitespace = self._whitespace

        def it():
            # replace by name
            yield from map(self._normalize_kv, itertools.chain(
                symbol_name_tr.items(), vulgar_fraction_name_tr.items()))
            # replace by digit
            yield from itertools.chain(
                subscript_digit_tr.items(), superscript_digit_tr.items())
            # replace by underscore
            yield from zip(itertools.chain(
                dash, whitespace), itertools.repeat('_'))
            # delete
            yield from zip(itertools.chain(
                punctuation, punctuation_extra), itertools.repeat(''))
        self.preprocess =\
            self.Preprocess.ALL if preprocess is None else preprocess
        self.tr = str.maketrans(dict(it()))

    @classmethod
    def _normalize_kv(cls, t: tuple[str, str]) -> tuple[str, str]:
        return (t[0], '_' + t[1].replace('-', '_') + '_')

    def __call__(
            self,
            s: str,
            default: str | object = _NONE,
            _re: re.Pattern[str] = re.compile(r'_+')
    ) -> str:
        t = s
        if self.preprocess & self.Preprocess.OPERATORS:
            t = self._preprocess_operators(s)
        t = t.translate(self.tr)
        t = _re.sub('_', t).strip('_')
        if t[0].isdigit():
            t = '_' + t
        if keyword.iskeyword(t):
            t = t + '_'
        if str.isidentifier(t):
            return t
        elif default != self._NONE:
            assert isinstance(default, str), default
            return default
        else:
            raise ValueError(
                f'"{t}" obtained from "{s}" is not an identifier')

    def _preprocess_operators(
            self,
            s: str,
            _re: re.Pattern[str] = re.compile(r'(\d)([^\w])(\d)'),
    ) -> str:
        return _re.sub(r'\1_\2_\3', s)

    def _preprocess_utc(
            self,
            s: str,
            _re: re.Pattern[str] = re.compile(r'\b(UTC)([+±\-−])(\d+)'),
    ) -> str:
        return _re.sub(r'\1_\2_\3', s)
