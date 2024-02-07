# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .kif_object import KIF_Object
from .snak import Snak
from .value import Entity


class Statement(KIF_Object):
    """Entity-snak pair.

    Parameters:
       entity: Entity.
       snak: Snak.
    """

    def __init__(self, entity: Entity, snak: Snak):
        return super().__init__(entity, snak)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_entity(arg, i)
        elif i == 2:
            return self._preprocess_arg_snak(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def subject(self) -> Entity:
        """The subject field of statement."""
        return self.get_subject()

    def get_subject(self) -> Entity:
        """Gets the subject field of statement.

        Returns:
           Subject.
        """
        return self.args[0]

    @property
    def snak(self) -> Snak:
        """The snak field of statement."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets the snak field of statement.

        Returns:
           Snak.
        """
        return self.args[1]
