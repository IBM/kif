# Copyright (C) 2024-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc

from .. import error
from ..context import Context
from ..typing import Self


class Compiler(abc.ABC):
    """Abstract base class for compilers."""

    class Error(error.Error):
        """Base class for compiler errors."""

    #: Alias for :func:`error.missing_dependency`.
    _missing_dependency = error.missing_dependency  # type: ignore

    #: Alias for :func:`error.should_not_get_here`.
    _should_not_get_here = error.should_not_get_here  # type: ignore

    def _cannot_compile_error(self, obj) -> Compiler.Error:
        return self.Error(f'cannot compile {obj}')

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
