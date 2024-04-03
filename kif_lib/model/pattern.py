# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .kif_object import KIF_Object


class Template(KIF_Object):
    """Abstract base class for templates."""


class Variable(KIF_Object):
    """Base class for variables.

    Parameters:
        name: String.
    """

    def __init__(self, name: str):
        super().__init__(name)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_str(arg, i)
        else:
            raise self._should_not_get_here()


class Pattern(KIF_Object):
    """Abstract base class for patterns."""
