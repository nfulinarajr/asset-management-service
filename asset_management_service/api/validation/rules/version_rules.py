from asset_management_service.api.validation.errors import ValidationError
from asset_management_service.models.version import Version
from asset_management_service.models.enums import VersionStatus


class VersionDepartmentIsRequiredRule:
    """
    Validation rule to ensure department exists.
    """

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not version.department:
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Version must define a valid department",
                )
            )

        return validation_errors


class VersionDepartmentIsValidRule:
    """
    Validation rule to ensure the department data type is valid.
    """

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not isinstance(version.department, str):
            validation_errors.append(
                ValidationError(
                    field="department",
                    message="Version department must be of type str",
                )
            )

        return validation_errors


class VersionIsGreaterThanOneRule:
    """
    Validation rule to ensure version is greater than or equal to 1.
    """

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if version.version_number is not None and version.version_number < 1:
            validation_errors.append(
                ValidationError(
                    field="version_number",
                    message="Version must be greater than or equal to 1",
                )
            )

        return validation_errors


class VersionStatusIsKnownRule:
    """
    Validation rule to ensure version status exists."""

    def validate(self, version: Version) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        try:
            VersionStatus(version.status)
        except ValueError:
            validation_errors.append(
                ValidationError(
                    field="status",
                    message="Version status must be of type VersionStatus",
                )
            )

        return validation_errors
