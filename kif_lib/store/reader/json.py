# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from ...model import Statement
from ...typing import Any, Iterable, Iterator, override, TextIO
from .reader import Reader


class JSON_Reader(
        Reader,
        store_name='json-reader',
        store_description='JSON reader'
):
    """JSON reader.

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

    @override
    def _load(self, file: TextIO) -> Iterator[dict[str, Any]]:
        import json
        return json.load(file, **self._kwargs)

    @override
    def _parse(self, input: dict[str, Any]) -> Iterable[Statement]:
        yield Statement.from_ast(input, **self._kwargs)
