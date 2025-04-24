# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import decimal
import re

from ..model import (
    AnnotatedStatement,
    ClosedTermSet,
    CompoundFingerprint,
    Datatype,
    Entity,
    Filter,
    Fingerprint,
    IRI,
    KIF_Object,
    Property,
    PseudoProperty,
    Quantity,
    Rank,
    Snak,
    SnakFingerprint,
    Statement,
    String,
    Template,
    Text,
    Time,
    ValueFingerprint,
    ValueSnak,
    Variable,
)
from ..model.kif_object import Encoder, Object
from ..typing import Iterator, override

SP = ' '                        # space
NL = '\n'                       # newline


class MarkdownEncoder(
        Encoder,
        format='markdown',
        description='Markdown encoder'
):
    """Markdown encoder."""

    @override
    def iterencode(self, input: Object) -> Iterator[str]:
        if isinstance(input, KIF_Object):
            yield from self._iterencode(input, 0)
        else:
            yield str(input)      # pragma: no cover

    def _iterencode(self, obj: KIF_Object, indent: int) -> Iterator[str]:
        if isinstance(obj, (Datatype, PseudoProperty)):
            yield self._encode_kif_object_name(obj)
        elif isinstance(obj, Entity):
            yield from self._iterencode_kif_object_start(obj)
            ###
            # FIXME: For now, ignore property datatype.
            ###
            if isinstance(obj, Property):
                obj = obj.replace(obj.iri, None)
            yield f'[{obj.display()}]({obj.iri.content})'
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, IRI):
            try:
                curie = obj.context.iris.curie(obj) or obj.content
                yield f'[{curie}]({obj.content})'
            except KeyError:
                yield from self._iterencode_iri_fallback(obj)
            except ValueError:
                yield from self._iterencode_iri_fallback(obj)
        elif isinstance(obj, Text):
            yield f'"{self._escape_md(obj.content)}"@{obj.language}'
        elif isinstance(obj, String):
            yield f'"{self._escape_md(obj.content)}"'
        elif isinstance(obj, Quantity):
            yield from self._iterencode_kif_object_start(obj)
            yield from self._iterencode_quantity(obj)
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Time):
            ###
            # TODO: Convert timezone and calendar model.
            ###
            yield from self._iterencode_kif_object_start(obj)
            if obj.precision is None or obj.precision.value <= 11:
                yield obj.time.date().isoformat()
            else:
                yield obj.time.replace().isoformat()
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Snak):
            yield from self._iterencode_kif_object_start(obj)
            yield from self._iterencode(obj.property, indent)
            if isinstance(obj, ValueSnak):
                vsnak = obj
                yield SP
                yield from self._iterencode(vsnak.value, indent)
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Statement):
            yield from self._iterencode_kif_object_start(obj)
            yield from self._iterencode(obj.subject, indent)
            yield SP
            yield from self._iterencode(obj.snak, indent)
            if isinstance(obj, AnnotatedStatement):
                sep = f'{NL}{2 * SP * indent}-{SP}'
                yield sep
                yield from self._iterencode(obj.qualifiers, indent + 1)
                yield sep
                yield from self._iterencode(obj.references, indent + 1)
                yield sep
                yield from self._iterencode(obj.rank, indent + 1)
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Template):
            yield from self._iterencode_kif_object_start(obj)
            for i, child in enumerate(obj.args, 1):
                if i > 1:
                    yield SP
                yield from self._iterencode(child, indent)
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Variable):
            yield from self._iterencode_variable(obj)
        elif isinstance(obj, Rank):
            yield self._encode_kif_object_name(obj)
        elif isinstance(obj, Fingerprint):
            yield from self._iterencode_kif_object_start(obj, '')
            if isinstance(obj, ValueFingerprint):
                yield SP
                yield from self._iterencode(obj.value, indent)
            elif isinstance(obj, SnakFingerprint):
                yield SP
                yield from self._iterencode(obj.snak, indent)
            elif isinstance(obj, CompoundFingerprint) and len(obj) > 0:
                for s in obj:
                    yield f'{NL}{2 * SP * indent}-{SP}'
                    yield from self._iterencode(s, indent + 1)
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, Filter):
            yield from self._iterencode_kif_object_start(obj, '')
            sep = f'{NL}{2 * SP * indent}-{SP}'
            for name in ['subject', 'property', 'value']:
                yield sep
                value = getattr(obj, name)
                yield from self._iterencode(value, indent + 1)
            yield sep
            yield f'**:snak_mask** `{obj.snak_mask}`'
            yield sep
            yield f'**:subject_mask** `{obj.subject_mask}`'
            yield sep
            yield f'**:property_mask** `{obj.property_mask}`'
            yield sep
            yield f'**:value_mask** `{obj.value_mask}`'
            yield sep
            yield f'**:rank_mask** `{obj.rank_mask}`'
            yield sep
            yield f'**:language** `{obj.language}`'
            yield sep
            yield f'**:annotated** `{obj.annotated}`'
            yield ''
            yield from self._iterencode_kif_object_end(obj)
        elif isinstance(obj, ClosedTermSet):
            yield from self._iterencode_kif_object_start(obj, '')
            if len(obj) > 0:
                for s in obj:
                    yield f'{NL}{2 * SP * indent}-{SP}'
                    yield from self._iterencode(s, indent + 1)
            yield from self._iterencode_kif_object_end(obj)
        else:
            yield str(obj)      # pragma: no cover

    def _encode_kif_object_name(self, obj: KIF_Object) -> str:
        return f'**{type(obj).__qualname__}**'

    def _iterencode_kif_object_start(
            self,
            obj: KIF_Object,
            sep: str = SP
    ) -> Iterator[str]:
        yield f'({self._encode_kif_object_name(obj)}{sep}'

    def _iterencode_kif_object_end(self, obj: KIF_Object) -> Iterator[str]:
        yield ')'

    def _iterencode_iri_fallback(
            self,
            iri: IRI,
            default_scheme: str = 'http'
    ) -> Iterator[str]:
        from urllib.parse import urlparse
        val = iri.content
        if not urlparse(val).scheme:
            yield f'[{val}]({default_scheme}://{val})'
        else:
            yield f'[{val}]({val})'

    def _iterencode_quantity(self, qt: Quantity) -> Iterator[str]:
        if qt.lower_bound is not None or qt.upper_bound is not None:
            val: str | None = None
            if qt.lower_bound is not None and qt.upper_bound is not None:
                n = decimal.Decimal(qt.amount)
                lb = decimal.Decimal(qt.lower_bound)
                ub = decimal.Decimal(qt.upper_bound)
                if (ub + lb) / 2 == n:
                    val = f'{n} ±{ub - n}'
            if not val:
                lbs = (str(qt.lower_bound)
                       if qt.lower_bound is not None else '-∞')
                ubs = (str(qt.upper_bound)
                       if qt.upper_bound is not None else '∞')
                val = f'{qt.amount} [{lbs},{ubs}]'
        else:
            val = str(qt.amount)
        if qt.unit:
            unit = self.encode(qt.unit)
            unit = f' {unit}'
        else:
            unit = ''
        yield f'{val}{unit}'

    def _iterencode_variable(
            self,
            obj: Variable,
            _re=re.compile(r'([_\w]+[^_])_?Variable$')
    ) -> Iterator[str]:
        if type(obj) is Variable:
            yield f'?{obj.name}'
        else:
            m = _re.match(type(obj).__qualname__)
            assert m is not None
            ty = m.group(1)
            yield f'(?{obj.name} : **{ty}**)'

    def _escape_md(self, text: str, escape_chars=r'_*`[') -> str:
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
