# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import dataclasses

from ...context import Section
from ...typing import Any, ClassVar, Iterable, Location
from .mapping.options import MappingOptions


@dataclasses.dataclass
class SPARQL_CompilerOptions(Section, name='sparql'):
    """SPARQL compiler options."""

    #: Mapping options.
    mapping: MappingOptions

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.mapping = MappingOptions()
        self._init_debug(kwargs)

    # -- debug --

    #: The default value for the debug option.
    DEFAULT_DEBUG: ClassVar[bool] = False

    _v_debug: ClassVar[tuple[Iterable[str], bool | None]] =\
        (('KIF_COMPILER_SPARQL_DEBUG',), DEFAULT_DEBUG)

    _debug: bool | None

    def _init_debug(self, kwargs: dict[str, Any]) -> None:
        self.debug = kwargs.get(
            '_debug', self.getenv_optional_bool(*self._v_debug))

    @property
    def debug(self) -> bool:
        """Whether to enable debugging mode."""
        return self.get_debug()

    @debug.setter
    def debug(self, debug: bool) -> None:
        self.set_debug(debug)

    def get_debug(self) -> bool:
        """Gets the debug flag.

        Returns:
           Debug flag.
        """
        assert self._debug is not None
        return self._debug

    def set_debug(
            self,
            debug: bool,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> None:
        """Sets the debug flag.

        Parameters:
           debug: Debug flag.
           function: Function or function name.
           name: Argument name.
           position: Argument position.
        """
        self._debug = bool(debug)
