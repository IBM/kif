# Copyright (C) 2023 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .kif_object import KIF_Object
from .snak import Snak
from .value import Entity


class Statement(KIF_Object):
    """Entity-snak pair.

    Parameters:
       arg1: Entity.
       arg2: Snak.
    """

    def __init__(self, arg1: Entity, arg2: Snak):
        return super().__init__(arg1, arg2)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_entity(arg, i)
        elif i == 2:
            return self._preprocess_arg_snak(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def subject(self) -> Entity:
        """Statement subject."""
        return self.get_subject()

    def get_subject(self) -> Entity:
        """Gets statement subject.

        Returns:
           Statement subject.
        """
        return self.args[0]

    @property
    def snak(self) -> Snak:
        """Statement snak."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets statement snak.

        Returns:
           Statement snak.
        """
        return self.args[1]
