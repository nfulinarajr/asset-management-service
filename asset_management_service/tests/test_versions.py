import pytest

from asset_management_service.models.enums import VersionStatus
from asset_management_service.models.version import Version


DEPARTMENT = "Animation"


def test_version_creation_with_required_and_default_values():
    version = Version(asset=1, department=DEPARTMENT)

    assert version.asset == 1
    assert version.department == DEPARTMENT
    assert version.version == None
    assert version.status == VersionStatus.INACTIVE


def test_version_creation_with_missing_asset():
    with pytest.raises(TypeError):
        Version(department=DEPARTMENT)


def test_version_creation_with_missing_department():
    with pytest.raises(TypeError):
        Version(asset=1)
