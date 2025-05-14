# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import csv

from ... import itertools
from ...model import Entity, Filter, Property, Statement, TGraph, Value
from ...typing import Any, BinaryIO, Iterable, Iterator, override, TextIO
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

    def __init__(
            self,
            store_name: str,
            *args: Reader.Args,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            parse: Reader.ParseFn | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        super().__init__(
            store_name, *args,
            location=location, file=file, data=data, graph=graph,
            parse=parse, **kwargs)

    @override
    def _parse(self, input: dict[str, Any]) -> Iterable[Statement]:
        yield Property.from_repr(input['property'])(
            Entity.from_repr(input['subject']),
            Value.from_repr(input['value']))

    @override
    def _filter_parse(
            self,
            filter: Filter,
            options: Reader.Options,
            file: TextIO
    ) -> Iterator[Statement]:
        return itertools.chain(*map(
            self._parse_fn, csv.DictReader(file, **self._kwargs)))
