from asset_management_service.api.validation.rules.version_rules import (
    VersionDepartmentIsRequiredRule,
    VersionDepartmentIsValidRule,
    VersionIsGreaterThanOneRule,
    VersionStatusIsKnownRule,
)
from asset_management_service.models.version import Version


DEPARTMENT = "Animation"


def test_version_department_is_required_rule():
    version = Version(asset=1, department=DEPARTMENT)

    rule = VersionDepartmentIsRequiredRule()

    validation_errors = rule.validate(version)

    assert validation_errors == []

    version.department = None

    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_version_department_is_correct_type_rule():
    version = Version(asset=1, department=DEPARTMENT)

    rule = VersionDepartmentIsValidRule()

    validation_errors = rule.validate(version)

    assert validation_errors == []

    version.department = 1

    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "department"


def test_version_is_greater_than_one_rule():
    version = Version(asset=1, department=DEPARTMENT, version_number=1)

    rule = VersionIsGreaterThanOneRule()

    validation_errors = rule.validate(version)

    assert validation_errors == []

    version.version_number = 0

    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "version"


def test_version_status_is_known_rule():
    version = Version(asset=1, department=DEPARTMENT)

    rule = VersionStatusIsKnownRule()

    validation_errors = rule.validate(version)

    assert validation_errors == []

    version.status = "Foo"

    validation_errors = rule.validate(version)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "status"
