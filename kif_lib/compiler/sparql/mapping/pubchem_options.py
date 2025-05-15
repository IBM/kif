# Copyright (C) 2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ....context import Section
from ....typing import Any, ClassVar, Location


@dataclasses.dataclass
class PubChemMappingOptions(Section, name='pubchem'):
    """PubChem SPARQL mapping options."""

    def __init__(self, **kwargs: Any) -> None:
        self._init_normalize_casrn(kwargs)

    # -- normalize_casrn --

    #: The default value for the normalize CAS-RN option.
    DEFAULT_NORMALIZE_CASRN: ClassVar[bool] = False

    _v_normalize_casrn: ClassVar[tuple[str, bool]] =\
        ('KIF_COMPILER_SPARQL_MAPPING_PUBCHEM_NORMALIZE_CASRN',
         DEFAULT_NORMALIZE_CASRN)

    _normalize_casrn: bool

    def _init_normalize_casrn(self, kwargs: dict[str, Any]) -> None:
        self.normalize_casrn = kwargs.get(
            '_normalize_casrn', self.getenv_bool(*self._v_normalize_casrn))

    @property
    def normalize_casrn(self) -> bool:
        """Whether to normalize the returned CAS-RNs."""
        return self.get_normalize_casrn()

    @normalize_casrn.setter
    def normalize_casrn(self, normalize_casrn: bool) -> None:
        self.set_normalize_casrn(normalize_casrn)

    def get_normalize_casrn(self) -> bool:
        """Gets the normalize CAS-RN flag.

        Returns:
           Normalize CAS-RN flag.
        """
        return self._normalize_casrn

    def set_normalize_casrn(
            self,
            normalize_casrn: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the normalize CAS-RN flag.

        Parameters:
           normalize_casrn: Normalize CAS-RN flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._normalize_casrn = bool(normalize_casrn)
