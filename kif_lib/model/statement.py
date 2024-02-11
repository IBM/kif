# Copyright (C) 2023-2024 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from .kif_object import KIF_Object
from .snak import Snak
from .value import Entity


class Statement(KIF_Object):
    """Entity-snak pair.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    def __init__(self, subject: Entity, snak: Snak):
        return super().__init__(subject, snak)

    def _preprocess_arg(self, arg, i):
        if i == 1:
            return self._preprocess_arg_entity(arg, i)
        elif i == 2:
            return self._preprocess_arg_snak(arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def subject(self) -> Entity:
        """The subject of statement."""
        return self.get_subject()

    def get_subject(self) -> Entity:
        """Gets the subject of statement.

        Returns:
           Subject.
        """
        return self.args[0]

    @property
    def snak(self) -> Snak:
        """The snak of statement."""
        return self.get_snak()

    def get_snak(self) -> Snak:
        """Gets the snak of statement.

        Returns:
           Snak.
        """
        return self.args[1]
