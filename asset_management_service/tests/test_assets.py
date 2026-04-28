import pytest

from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType


ASSET_NAME = "TestCharacterName"
ASSET_TYPE = AssetType.CHARACTER


def test_asset_creation_with_required_values():
    asset = Asset(name=ASSET_NAME, asset_type=ASSET_TYPE)

    assert asset.name == ASSET_NAME
    assert asset.asset_type == ASSET_TYPE


def test_asset_creation_with_missing_name():
    with pytest.raises(TypeError):
        Asset(asset_type=ASSET_TYPE)


def test_asset_creation_with_missing_type():
    with pytest.raises(TypeError):
        Asset(name=ASSET_NAME)
