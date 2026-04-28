from dataclasses import dataclass


@dataclass(slots=True)
class ValidationError:
    """
    Custom validation error for validation rules.
    """

    field: str
    message: str
