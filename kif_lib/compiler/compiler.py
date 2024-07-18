# Copyright (C) 2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

import abc

from ..model.kif_object import KIF_Object


class Compiler(abc.ABC):
    """Abstract base class for compilers."""

    class Error(KIF_Object.Error):
        """Base class for compiler errors."""

    class Results(abc.ABC):
        """Abstract base class for compiler results."""

    def _cannot_compile_error(self, obj) -> 'Compiler.Error':
        return self.Error(f'cannot compile {obj}')

    def _should_not_get_here(self):
        return KIF_Object._should_not_get_here()

    @abc.abstractmethod
    def compile(self) -> 'Compiler.Results':
        """Compiles pattern.

        Parameter:
           pat: Pattern.

        Returns:
           The compiled results.

        Raises:
           `CompilerError`: Compiler error.
        """
        raise NotImplementedError
