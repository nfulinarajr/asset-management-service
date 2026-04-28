from dataclasses import dataclass
from typing import Generic, Protocol, Sequence, TypeVar

from asset_management_service.api.validation.errors import ValidationError


T = TypeVar("T")


class Rule(Protocol[T]):
    """
    Represents a validation rule for a subject of type T.

    Any implementation must provide validate(self, subject: T) -> list[ValidationError].
    If no validation errors are returned, an empty list indicates validation rules have
    passed.
    """

    def validate(self, subject: T) -> list[ValidationError]: ...


@dataclass(slots=True)
class ValidationPipeline(Generic[T]):
    """
    A validation pipeline that is fully extensible and composable.

    This pipeline accepts a Sequence of rules conforming to the Rule protocol, and
    applies them to a subject of type T, which can be an Asset, Version, etc.

    Args:
        rules (Sequence[Rule] | None): A container of validation rules that conform to
            the Rule protocol and validate objects of type T.
    """

    # Container for all rules that implement the Rule protocol
    rules: Sequence[Rule[T]]

    def __init__(self, rules: Sequence[Rule[T]] | None = None) -> None:
        # Ensure rules are immutable to maintain state after pipeline creation
        self.rules = tuple(rules) if rules is not None else tuple()

    def validate(self, subject: T) -> list[ValidationError]:
        """
        Validate a subject.

        Args:
            subject (T): An object to validate.

        Returns:
            list[ValidationError]: A list of validation errors encountered while
                applying all rules to the subject.
        """

        validation_errors: list[ValidationError] = []

        # Iterate all validation rules and collect any errors encountered
        for validation_rule in self.rules:
            validation_errors.extend(validation_rule.validate(subject))

        return validation_errors
