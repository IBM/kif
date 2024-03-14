# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import re

from ..model import (
    AnnotationRecord,
    Datatype,
    Entity,
    FilterPattern,
    Fingerprint,
    IRI,
    KIF_Object,
    PlainDescriptor,
    PropertyDescriptor,
    Quantity,
    Rank,
    Snak,
    Statement,
    String,
    Text,
    Time,
    ValueSnak,
)
from ..model.kif_object import Decimal, Encoder, Object
from ..namespace import _DEFAULT_NSM
from ..typing import cast, Generator, Optional

SP = ' '                        # space
NL = '\n'                       # newline


class MarkdownEncoder(
        Encoder, format='markdown', description='Markdown encoder'):
    """Markdown encoder."""

    @property
    def wd(self):
        from .. import vocabulary
        return vocabulary.wd

    def iterencode(self, obj: Object) -> Generator[str, None, None]:
        if KIF_Object.test(obj):
            yield from self._iterencode(cast(KIF_Object, obj), 0)
        else:
            yield str(obj)      # pragma: no cover

    def _iterencode(
            self,
            obj: KIF_Object,
            indent: int
    ) -> Generator[str, None, None]:
        if obj.is_datatype():
            datatype = cast(Datatype, obj)
            yield self._encode_kif_object_name(datatype)
        elif obj.is_entity():
            entity = cast(Entity, obj)
            yield from self._iterencode_kif_object_start(entity)
            label = self.wd.get_entity_label(entity)
            if label:
                yield f'[{label}]({entity.iri.value})'
            else:
                yield from self._iterencode(entity.iri, indent)
            yield from self._iterencode_kif_object_end(entity)
        elif obj.is_iri():
            iri = cast(IRI, obj)
            try:
                yield f'[{_DEFAULT_NSM.curie(iri.value, False)}]({iri.value})'
            except KeyError:
                yield from self._iterencode_iri_fallback(iri)
            except ValueError:
                yield from self._iterencode_iri_fallback(iri)
        elif obj.is_text():
            text = cast(Text, obj)
            yield f'"{self._escape_md(text.value)}"@{text.language}'
        elif obj.is_string():
            s = cast(String, obj)
            yield f'"{self._escape_md(s.value)}"'
        elif obj.is_quantity():
            qtd = cast(Quantity, obj)
            yield from self._iterencode_kif_object_start(qtd)
            yield from self._iterencode_quantity(qtd)
            yield from self._iterencode_kif_object_end(qtd)
        elif obj.is_time():
            ###
            # TODO: Convert timezone and calendar model.
            ###
            time = cast(Time, obj)
            yield from self._iterencode_kif_object_start(time)
            if time.precision is None or time.precision.value <= 11:
                yield time.time.date().isoformat()
            else:
                yield time.time.replace().isoformat()
            yield from self._iterencode_kif_object_end(time)
        elif obj.is_snak():
            snak = cast(Snak, obj)
            yield from self._iterencode_kif_object_start(snak)
            yield from self._iterencode(snak.property, indent)
            if snak.is_value_snak():
                vsnak = cast(ValueSnak, snak)
                yield SP
                yield from self._iterencode(vsnak.value, indent)
            yield from self._iterencode_kif_object_end(snak)
        elif obj.is_statement():
            stmt = cast(Statement, obj)
            yield from self._iterencode_kif_object_start(obj)
            yield from self._iterencode(stmt.subject, indent)
            yield SP
            yield from self._iterencode(stmt.snak, indent)
            yield from self._iterencode_kif_object_end(obj)
        elif obj.is_annotation_record():
            annot = cast(AnnotationRecord, obj)
            yield from self._iterencode_kif_object_start(annot, '')
            sep = f'{NL}{2 * SP * indent}-{SP}'
            for name in ['qualifiers', 'references', 'rank']:
                yield sep
                yield from self._iterencode(
                    getattr(annot, name), indent + 1)
            yield ''
            yield from self._iterencode_kif_object_end(annot)
        elif obj.is_rank():
            rank = cast(Rank, obj)
            yield self._encode_kif_object_name(rank)
        elif obj.is_plain_descriptor():
            desc = cast(PlainDescriptor, obj)
            yield from self._iterencode_kif_object_start(desc, '')
            sep = f'{NL}{2 * SP * indent}-{SP}'
            yield sep
            if desc.label is not None:
                yield from self._iterencode(desc.label, indent + 1)
            else:
                yield '*no label*'
            yield sep
            if desc.aliases is not None and desc.aliases:
                yield from self._iterencode(desc.aliases, indent + 1)
            else:
                yield '*no aliases*'
            yield sep
            if desc.description is not None:
                yield from self._iterencode(desc.description, indent + 1)
            else:
                yield '*no description*'
            if obj.is_property_descriptor():
                yield sep
                desc = cast(PropertyDescriptor, obj)
                if desc.datatype is not None:
                    yield from self._iterencode(desc.datatype, indent + 1)
                else:
                    yield '*no datatype*'
            yield ''
            yield from self._iterencode_kif_object_end(desc)
        elif obj.is_fingerprint():
            fp = cast(Fingerprint, obj)
            if fp.value is not None:
                yield from self._iterencode_kif_object_start(fp)
                yield from self._iterencode(fp.value, indent)
            elif fp.snak_set is not None:
                yield from self._iterencode_kif_object_start(obj, '')
                yield SP
                yield from self._iterencode(fp.snak_set, indent + 1)
            else:
                raise obj._should_not_get_here()
            yield from self._iterencode_kif_object_end(fp)
        elif obj.is_filter_pattern():
            pat = cast(FilterPattern, obj)
            yield from self._iterencode_kif_object_start(pat, '')
            sep = f'{NL}{2 * SP * indent}-{SP}'
            for name in ['subject', 'property', 'value']:
                yield sep
                value = getattr(pat, name)
                if value is not None:
                    yield from self._iterencode(value, indent + 1)
                else:
                    if name == 'subject':
                        yield '*any entity*'
                    else:
                        yield f'*any {name}*'
            yield sep
            yield f'`{bin(pat.snak_mask.value)}`'
            yield ''
            yield from self._iterencode_kif_object_end(obj)
        elif obj.is_kif_object_set():
            yield from self._iterencode_kif_object_start(obj, '')
            if len(obj) > 0:
                for s in obj:
                    yield f'{NL}{2 * SP * indent}-{SP}'
                    yield from self._iterencode(s, indent + 1)
            yield from self._iterencode_kif_object_end(obj)
        else:
            yield str(obj)      # pragma: no cover

    def _encode_kif_object_name(
            self,
            obj: KIF_Object
    ) -> str:
        return f'**{obj.__class__.__qualname__}**'

    def _iterencode_kif_object_start(
            self,
            obj: KIF_Object,
            sep: str = SP
    ) -> Generator[str, None, None]:
        yield f'({self._encode_kif_object_name(obj)}{sep}'

    def _iterencode_kif_object_end(
            self,
            obj: KIF_Object
    ) -> Generator[str, None, None]:
        yield ')'

    def _iterencode_iri_fallback(
            self,
            iri: IRI,
            default_scheme: str = 'http'
    ) -> Generator[str, None, None]:
        from urllib.parse import urlparse
        val = iri.value
        if not urlparse(val).scheme:
            yield f'[{val}]({default_scheme}://{val})'
        else:
            yield f'[{val}]({val})'

    def _iterencode_quantity(
            self,
            qtd: Quantity
    ) -> Generator[str, None, None]:
        if qtd.lower_bound is not None or qtd.upper_bound is not None:
            val: Optional[str] = None
            if qtd.lower_bound is not None and qtd.upper_bound is not None:
                qt = Decimal(qtd.amount)
                lb = Decimal(qtd.lower_bound)
                ub = Decimal(qtd.upper_bound)
                if (ub + lb) / 2 == qt:
                    val = f'{qt} ±{ub - qt}'
            if not val:
                lbs = (str(qtd.lower_bound)
                       if qtd.lower_bound is not None else '-∞')
                ubs = (str(qtd.upper_bound)
                       if qtd.upper_bound is not None else '∞')
                val = f'{qtd.amount} [{lbs},{ubs}]'
        else:
            val = str(qtd.amount)
        if qtd.unit:
            unit = self.encode(qtd.unit)
            unit = f' {unit}'
        else:
            unit = ''
        yield f'{val}{unit}'

    def _escape_md(self, text: str, escape_chars=r'_*`[') -> str:
        return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)
