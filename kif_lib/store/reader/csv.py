# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import csv
import io

from ...model import Entity, Property, Statement, TGraph, Value
from ...typing import Any, BinaryIO, IO, Iterable, override, TextIO
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
       kwargs: Other keyword arguments."""

    __slots__ = (
        '_cleanup',
        '_fieldnames',
        '_kwargs',
    )

    #: File handles that need to be closed.
    _cleanup: list[IO]

    #: Other keyword arguments.
    _kwargs: Any

    def __init__(
            self,
            store_name: str,
            *args: Reader.Args,
            location: str | None = None,
            file: BinaryIO | TextIO | None = None,
            data: bytes | str | None = None,
            graph: TGraph | None = None,
            parse: Reader.ParseFunction | None = None,
            **kwargs: Any
    ) -> None:
        assert store_name == self.store_name
        self._cleanup = []
        self._kwargs = kwargs
        super().__init__(
            store_name, *args,
            location=location, file=file, data=data, graph=graph,
            parse=parse)

    @override
    def _close(self) -> None:
        for fp in self._cleanup:
            fp.close()

    @override
    def _parse(self, input: dict[str, Any]) -> Iterable[Statement]:
        yield Property.from_repr(input['property'])(
            Entity.from_repr(input['subject']),
            Value.from_repr(input['value']))

    @override
    def _read(self, input: CSV_Reader.Input) -> Iterable[dict[str, Any]]:
        fp: TextIO
        if isinstance(input, self.LocationInput):
            fp = open(input.location, encoding='utf-8')
            self._cleanup.append(fp)
        elif isinstance(input, self.FileInput):
            if isinstance(input.file, TextIO):
                fp = input.file
            else:
                fp = io.TextIOWrapper(input.file, encoding='utf-8')
        elif isinstance(input, self.DataInput):
            if isinstance(input.data, bytes):
                fp = io.StringIO(input.data.decode('utf-8'))
            else:
                fp = io.StringIO(input.data)
        else:
            raise self._should_not_get_here()
        yield from csv.DictReader(fp, **self._kwargs)
