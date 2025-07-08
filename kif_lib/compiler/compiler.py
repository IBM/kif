# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from ..context import Context
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

    @property
    def context(self) -> Context:
        """The current KIF context."""
        return self.get_context()

    def get_context(self, context: Context | None = None) -> Context:
        """Gets the current KIF context.

        If `context` is not ``None``, returns `context`.

        Parameters:
           context: Context.

        Returns:
           Context.
        """
        return Context.top(context)

    @abc.abstractmethod
    def compile(self) -> Self:
        """Run compiler.

        Returns:
           Compiler.
        """
        raise NotImplementedError
