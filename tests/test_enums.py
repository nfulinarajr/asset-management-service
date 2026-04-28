import pytest

from asset_management_service.models.enums import AssetType, VersionStatus


INVALID_VALUE = "Foo"


def test_invalid_asset_type_value():
    with pytest.raises(ValueError):
        AssetType(INVALID_VALUE)


def test_invalid_version_status_value():
    with pytest.raises(ValueError):
        VersionStatus(INVALID_VALUE)
