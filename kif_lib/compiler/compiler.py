# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from ..model.kif_object import KIF_Object
from ..typing import Self


class Compiler(abc.ABC):
    """Abstract base class for compilers."""

    class Error(KIF_Object.Error):
        """Base class for compiler errors."""

    def _cannot_compile_error(self, obj) -> Compiler.Error:
        return self.Error(f'cannot compile {obj}')

    def _should_not_get_here(self) -> KIF_Object.ShouldNotGetHere:
        return KIF_Object._should_not_get_here()

    @abc.abstractmethod
    def compile(self) -> Self:
        """Run compiler.

        Returns:
           The (finished) compiler.
        """
        raise NotImplementedError
