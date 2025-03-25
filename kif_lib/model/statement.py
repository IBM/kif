# Copyright (C) 2023-2025 IBM Corp.
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from .. import itertools
from ..typing import (
    Any,
    ClassVar,
    Location,
    override,
    Self,
    TypeAlias,
    TypedDict,
    Union,
)
from .rank import NormalRank, Rank, RankVariable, TRank, VRank, VTRank
from .set import (
    QualifierRecord,
    QualifierRecordVariable,
    ReferenceRecordSet,
    ReferenceRecordSetVariable,
    TQualifierRecord,
    TReferenceRecordSet,
    VQualifierRecord,
    VReferenceRecordSet,
    VTQualifierRecord,
    VTReferenceRecordSet,
)
from .snak import (
    Snak,
    SnakTemplate,
    SnakVariable,
    TSnak,
    ValueSnak,
    VSnak,
    VTSnak,
)
from .term import ClosedTerm, Template, Variable
from .value import (
    Entity,
    EntityTemplate,
    EntityVariable,
    TEntity,
    TProperty,
    TValue,
    VEntity,
    VTEntity,
)

TStatement: TypeAlias =\
    Union['Statement',
          tuple[TEntity, TSnak],
          tuple[TEntity, TProperty, TValue]]
VStatement: TypeAlias =\
    Union['StatementTemplate', 'StatementVariable', 'Statement']
VTStatement: TypeAlias = Union[Variable, VStatement, TStatement]

TAnnotatedStatement: TypeAlias =\
    Union['AnnotatedStatement',
          tuple[TStatement, TQualifierRecord, TReferenceRecordSet, TRank]]
VAnnotatedStatement: TypeAlias =\
    Union['AnnotatedStatementTemplate', 'AnnotatedStatementVariable',
          'AnnotatedStatement']
VTAnnotatedStatement: TypeAlias =\
    Union[Variable, VAnnotatedStatement, TAnnotatedStatement]


class _Annotation(TypedDict, total=False):
    """Statement annotation."""

    qualifiers: VTQualifierRecord | None
    references: VTReferenceRecordSet | None
    rank: VTRank | None
    replace: bool


class StatementTemplate(Template):
    """Statement template.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    object_class: ClassVar[type[Statement]]  # pyright: ignore

    def __init__(self, subject: VTEntity, snak: VTSnak) -> None:
        super().__init__(subject, snak)

    def __matmul__(self, other: _Annotation) -> AnnotatedStatementTemplate:
        return self.annotate(**other)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # entity
            if isinstance(arg, Template):
                return EntityTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return EntityVariable.check(arg, type(self), None, i)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        elif i == 2:            # snak
            if isinstance(arg, Template):
                return SnakTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return SnakVariable.check(arg, type(self), None, i)
            else:
                return Statement._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def subject(self) -> VEntity:
        """The subject of statement template."""
        return self.get_subject()

    def get_subject(self) -> VEntity:
        """Gets the subject of statement template.

        Returns:
           Entity, entity template, or entity variable.
        """
        return self.args[0]

    @property
    def snak(self) -> VSnak:
        """The snak of statement template."""
        return self.get_snak()

    def get_snak(self) -> VSnak:
        """Gets the snak of statement template.

        Returns:
           Snak, snak template, or snak variable.
        """
        return self.args[1]

    @property
    def claim(self) -> tuple[VEntity, VSnak]:
        """The claim of statement template."""
        return self.get_claim()

    def get_claim(self) -> tuple[VEntity, VSnak]:
        """Gets the claim of statement template.

        Returns:
           Statement template claim: subject, snak.
        """
        return self.subject, self.snak

    def annotate(
            self,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None,
            replace: bool = False
    ) -> AnnotatedStatementTemplate:
        """Annotates statement template.

        Parameters:
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.
           replace: Whether to replace existing annotations.

        Returns:
           Annotated statement template.
        """
        return AnnotatedStatementTemplate(
            self.subject, self.snak, qualifiers, references, rank)

    def unannotate(self) -> Statement | StatementTemplate:
        """Unannotates statement template.

        Returns:
           Unannotated statement or template.
        """
        return Statement(*self.claim)


class StatementVariable(Variable):
    """Statement variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[Statement]]  # pyright: ignore


class Statement(
        ClosedTerm,
        template_class=StatementTemplate,
        variable_class=StatementVariable
):
    """Statement.

    Parameters:
       subject: Entity.
       snak: Snak.
    """

    template_class: ClassVar[type[StatementTemplate]]  # pyright: ignore
    variable_class: ClassVar[type[StatementVariable]]  # pyright: ignore

    # Type alias for "annotation dictionary".
    Annotation: TypeAlias = _Annotation

    # Type alias for "annotation triple".
    AnnotationTriple: TypeAlias =\
        tuple[QualifierRecord, ReferenceRecordSet, Rank]

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, tuple) and len(arg) >= 2:
            fn = function or cls.check
            if len(arg) == 2:
                return cls(
                    Entity.check(arg[0], fn, name, position),
                    Snak.check(arg[1], fn, name, position))
            else:
                return cls(
                    Entity.check(arg[0], fn, name, position),
                    ValueSnak.check((arg[1], arg[2]), fn, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(self, subject: VTEntity, snak: VTSnak) -> None:
        super().__init__(subject, snak)

    def __matmul__(self, other: _Annotation) -> AnnotatedStatement:
        return self.annotate(**other)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Entity.check(arg, type(self_), None, i)
        elif i == 2:
            return Snak.check(arg, type(self_), None, i)
        else:
            raise self_._should_not_get_here()

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

    @property
    def claim(self) -> tuple[Entity, Snak]:
        """The claim of statement."""
        return self.get_claim()

    def get_claim(self) -> tuple[Entity, Snak]:
        """Gets the claim of statement.

        Returns:
           Statement claim: subject, snak.
        """
        return self.subject, self.snak

    def annotate(
            self,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None,
            replace: bool = False
    ) -> AnnotatedStatement:
        """Annotates statement.

        Parameters:
           qualifiers: Qualifier record.
           references: Reference record set.
           rank: Rank.
           replace: Whether to replace existing annotations.

        Returns:
           Annotated statement.
        """
        return AnnotatedStatement(
            self.subject, self.snak, qualifiers, references, rank)

    def unannotate(self) -> Statement:
        """Unannotates statement.

        Returns:
           Unannotated statement.
        """
        return Statement(*self.claim)


class AnnotatedStatementTemplate(StatementTemplate):
    """Annotated statement template.

    Parameters:
       entity: Entity.
       snak: Snak.
       qualifiers: Qualifier record.
       references: Reference record set.
       rank: Rank.
    """

    object_class: ClassVar[type[AnnotatedStatement]]  # pyright: ignore

    def __init__(
            self,
            entity: VTEntity,
            snak: VTSnak,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> None:
        super(Template, self).__init__(
            entity, snak, qualifiers, references, rank)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        if i == 1:              # entity
            if isinstance(arg, Template):
                return EntityTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return EntityVariable.check(arg, type(self), None, i)
            else:
                return AnnotatedStatement._static_preprocess_arg(self, arg, i)
        elif i == 2:            # snak
            if isinstance(arg, Template):
                return SnakTemplate.check(arg, type(self), None, i)
            elif isinstance(arg, Variable):
                return SnakVariable.check(arg, type(self), None, i)
            else:
                return AnnotatedStatement._static_preprocess_arg(self, arg, i)
        elif i == 3:            # qualifiers
            if isinstance(arg, Variable):
                return QualifierRecordVariable.check(arg, type(self), None, i)
            else:
                return AnnotatedStatement._static_preprocess_arg(self, arg, i)
        elif i == 4:            # references
            if isinstance(arg, Variable):
                return ReferenceRecordSetVariable.check(
                    arg, type(self), None, i)
            else:
                return AnnotatedStatement._static_preprocess_arg(self, arg, i)
        elif i == 5:            # rank
            if isinstance(arg, Variable):
                return RankVariable.check(arg, type(self), None, i)
            else:
                return AnnotatedStatement._static_preprocess_arg(self, arg, i)
        else:
            raise self._should_not_get_here()

    @property
    def qualifiers(self) -> VQualifierRecord:
        """The qualifiers of annotated statement template."""
        return self.get_qualifiers()

    def get_qualifiers(self) -> VQualifierRecord:
        """Gets the qualifiers of annotated statement template.

        Returns:
           Qualifier record or qualifier record variable.
        """
        return self.args[2]

    @property
    def references(self) -> VReferenceRecordSet:
        """The references of annotated statement template."""
        return self.get_references()

    def get_references(self) -> VReferenceRecordSet:
        """Gets the references of annotated statement template.

        Returns:
           Reference record set or reference record set variable.
        """
        return self.args[3]

    @property
    def rank(self) -> VRank:
        """The rank of annotated statement template."""
        return self.get_rank()

    def get_rank(self) -> VRank:
        """Gets the rank of annotated statement template.

        Returns:
           Rank or rank variable.
        """
        return self.args[4]

    @override
    def annotate(
            self,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None,
            replace: bool = False
    ) -> AnnotatedStatementTemplate:
        if qualifiers is None:
            qualifiers = self.qualifiers
        elif not replace:
            qualifiers = itertools.chain(qualifiers, self.qualifiers)
        if references is None:
            references = self.references
        elif not replace:
            references = itertools.chain(references, self.references)
        if rank is None:
            rank = self.rank
        return AnnotatedStatementTemplate(
            self.subject, self.snak, qualifiers, references, rank)


class AnnotatedStatementVariable(StatementVariable):
    """Annotated statement variable.

    Parameters:
       name: Name.
    """

    object_class: ClassVar[type[AnnotatedStatement]]  # pyright: ignore


class AnnotatedStatement(
        Statement,
        template_class=AnnotatedStatementTemplate,
        variable_class=AnnotatedStatementVariable
):
    """Annotated statement.

    Parameters:
       entity: Entity.
       snak: Snak.
       qualifiers: Qualifier record.
       references: Reference record set.
       rank: Rank.
    """

    template_class: ClassVar[type[  # pyright: ignore
        AnnotatedStatementTemplate]]

    variable_class: ClassVar[type[  # pyright: ignore
        AnnotatedStatementVariable]]

    @classmethod
    @override
    def check(
            cls,
            arg: Any,
            function: Location | None = None,
            name: str | None = None,
            position: int | None = None
    ) -> Self:
        if isinstance(arg, cls):
            return arg
        elif isinstance(arg, Statement):
            return cls(*arg)
        elif isinstance(arg, tuple) and len(arg) >= 2:
            return cls(*Statement.check(
                arg, function or cls.check, name, position))
        else:
            raise cls._check_error(arg, function, name, position)

    def __init__(
            self,
            subject: VTEntity,
            snak: VTSnak,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None
    ) -> None:
        super(ClosedTerm, self).__init__(
            subject, snak, qualifiers, references, rank)

    @override
    def _preprocess_arg(self, arg: Any, i: int) -> Any:
        return self._static_preprocess_arg(self, arg, i)

    @staticmethod
    def _static_preprocess_arg(self_, arg: Any, i: int) -> Any:
        if i == 1:
            return Entity.check(arg, type(self_), None, i)
        elif i == 2:
            return Snak.check(arg, type(self_), None, i)
        elif i == 3:
            return QualifierRecord.check_optional(
                arg, QualifierRecord(), type(self_), None, i)
        elif i == 4:
            return ReferenceRecordSet.check_optional(
                arg, ReferenceRecordSet(), type(self_), None, i)
        elif i == 5:
            return Rank.check_optional(
                arg, NormalRank(), type(self_), None, i)
        else:
            raise self_._should_not_get_here()

    @property
    def qualifiers(self) -> QualifierRecord:
        """The qualifiers of annotated statement."""
        return self.get_qualifiers()

    def get_qualifiers(self) -> QualifierRecord:
        """Gets the qualifiers of annotated statement.

        Returns:
           Qualifier record.
        """
        return self.args[2]

    @property
    def references(self) -> ReferenceRecordSet:
        """The references of annotated statement."""
        return self.get_references()

    def get_references(self) -> ReferenceRecordSet:
        """Gets the references of annotated statement.

        Returns:
           Reference record set.
        """
        return self.args[3]

    @property
    def rank(self) -> Rank:
        """The rank of annotated statement."""
        return self.get_rank()

    def get_rank(self) -> Rank:
        """Gets the rank of annotated statement.

        Returns:
           Rank.
        """
        return self.args[4]

    @override
    def annotate(
            self,
            qualifiers: VTQualifierRecord | None = None,
            references: VTReferenceRecordSet | None = None,
            rank: VTRank | None = None,
            replace: bool = False
    ) -> AnnotatedStatement:
        if qualifiers is None:
            qualifiers = self.qualifiers
        elif not replace:
            qualifiers = itertools.chain(qualifiers, self.qualifiers)
        if references is None:
            references = self.references
        elif not replace:
            references = itertools.chain(references, self.references)
        if rank is None:
            rank = self.rank
        return AnnotatedStatement(
            self.subject, self.snak, qualifiers, references, rank)
