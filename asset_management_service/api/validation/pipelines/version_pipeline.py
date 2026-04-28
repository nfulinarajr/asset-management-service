from asset_management_service.api.validation.rules.version_rules import (
    VersionDepartmentIsRequiredRule,
    VersionDepartmentIsValidRule,
    VersionIsGreaterThanOneRule,
    VersionStatusIsKnownRule,
)
from asset_management_service.api.validation.core import ValidationPipeline
from asset_management_service.models.version import Version


def build_default_version_pipeline() -> ValidationPipeline[Version]:
    """
    Build a default version validation pipeline.

    Returns:
        ValidationPipeline[Version]: A collection of all version validation rules.
    """

    return ValidationPipeline[Version](
        rules=[
            VersionDepartmentIsRequiredRule(),
            VersionDepartmentIsValidRule(),
            VersionIsGreaterThanOneRule(),
            VersionStatusIsKnownRule(),
        ]
    )
