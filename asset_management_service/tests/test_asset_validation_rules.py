from asset_management_service.api.validation.rules.asset_rules import (
    AssetNameIsRequiredRule,
    AssetNameIsValidRule,
    AssetTypeIsRequiredRule,
    AssetTypeIsValidRule,
)
from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType


ASSET_NAME = "TestAssetName"
ASSET_TYPE = AssetType.CHARACTER


def test_asset_name_is_required_rule():
    asset = Asset(name=ASSET_NAME, asset_type=ASSET_TYPE)

    rule = AssetNameIsRequiredRule()

    validation_errors = rule.validate(asset)

    assert validation_errors == []

    asset.name = None

    validation_errors = rule.validate(asset)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "name"


def test_asset_name_is_correct_type_rule():
    asset = Asset(name=ASSET_NAME, asset_type=ASSET_TYPE)

    rule = AssetNameIsValidRule()

    validation_errors = rule.validate(asset)

    assert validation_errors == []

    asset.name = 1

    validation_errors = rule.validate(asset)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "name"


def test_asset_type_is_required_rule():
    asset = Asset(name=ASSET_NAME, asset_type=ASSET_TYPE)

    rule = AssetTypeIsRequiredRule()

    validation_errors = rule.validate(asset)

    assert validation_errors == []

    asset.asset_type = None

    validation_errors = rule.validate(asset)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "type"


def test_asset_type_is_correct_type_rule():
    asset = Asset(name=ASSET_NAME, asset_type=ASSET_TYPE)

    rule = AssetTypeIsValidRule()

    validation_errors = rule.validate(asset)

    assert validation_errors == []

    asset.asset_type = 1

    validation_errors = rule.validate(asset)

    assert len(validation_errors) == 1
    assert validation_errors[0].field == "type"
