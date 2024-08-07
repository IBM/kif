# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc

from . import defaults
from .typing import Any, Self


@dc.dataclass
class Section:
    """Section in KIF options."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        def it():
            for field in dc.fields(cls):
                if field.name not in data:
                    continue
                if (isinstance(field.default_factory, type)
                        and issubclass(field.default_factory, Section)):
                    yield (field.name,
                           field.default_factory.from_dict(data[field.name]))
                else:
                    yield (field.name, data[field.name])
        return cls(**dict(it()))

    def to_dict(self) -> dict[str, Any]:
        return dc.asdict(self)


@dc.dataclass
class Options(Section):
    """KIF options."""

    @dc.dataclass
    class Model(Section):

        @dc.dataclass
        class Text(Section):

            _default_language: str

            def __init__(self, **kwargs):
                self.default_language = kwargs.get(
                    '_default_language',
                    defaults.KIF_MODEL_TEXT_DEFAULT_LANGUAGE)

            @property
            def default_language(self) -> str:
                return self._default_language

            @default_language.setter
            def default_language(self, lang: str):
                self._default_language = lang

        text: 'Options.Model.Text' = dc.field(default_factory=Text)

    model: 'Options.Model' = dc.field(default_factory=Model)
