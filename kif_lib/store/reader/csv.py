# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import contextlib
import dataclasses

from ...model import Entity, Filter, Property, Statement, Value
from ...typing import (
    Any,
    Generator,
    Iterable,
    Iterator,
    ModuleType,
    override,
    TextIO,
)
from .reader import Reader


class CSV_Reader(
        Reader,
        store_name='csv-reader',
        store_description='CSV reader'
):
    """CSV reader.

    Parameters:
       store_name: Name of the store plugin to instantiate.
       args: Input sources.
       location: Relative or absolute IRI of the input source.
       file: File-like object to be used as input source.
       data: Data to be used as input source.
       graph: KIF graph to used as input source.
       parse: Input parsing function.
       kwargs: Other keyword arguments.
    """

    @dataclasses.dataclass
    class DataFrame(Reader.Source):
        """Data frame source."""

        data_frame: Any

    @classmethod
    def _pandas(cls) -> ModuleType:
        try:
            import pandas
            return pandas
        except ImportError as err:
            raise ImportError(
                f'{__name__} requires https://pandas.pydata.org') from err

    @override
    def _check_unknown_arg(self, arg: Any) -> Reader.Source:
        if isinstance(arg, self._pandas().DataFrame):
            return self.DataFrame(arg)
        else:
            return super()._check_unknown_arg(arg)

    @contextlib.contextmanager
    def _load_data_frame(
            self,
            df: Any
    ) -> Generator[Iterable[Any], None, None]:
        assert isinstance(df, self._pandas().DataFrame)
        yield map(lambda t: t[1].to_dict(), df.iterrows())

    @override
    def _load(self, file: TextIO) -> Iterator[dict[str, Any]]:
        import csv
        return csv.DictReader(file, **self._kwargs)

    @override
    def _filter_parse_unknown_arg(
            self,
            filter: Filter,
            options: Reader.Options,
            arg: Reader.Source
    ) -> Iterator[Statement]:
        if isinstance(arg, self.DataFrame):
            yield from self._filter_parse(
                filter, options, self._load_data_frame, arg.data_frame)
        else:
            yield from super()._filter_parse_unknown_arg(
                filter, options, arg)

    @override
    def _parse(self, input: dict[str, Any]) -> Iterable[Statement]:
        yield Property.from_repr(input['property'])(
            Entity.from_repr(input['subject']),
            Value.from_repr(input['value']))
