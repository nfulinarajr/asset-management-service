from asset_management_service.api.validation.pipelines.asset_pipeline import (
    build_default_asset_pipeline,
)
from asset_management_service.api.validation.pipelines.version_pipeline import (
    build_default_version_pipeline,
)
from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType
from asset_management_service.models.version import Version


def test_build_default_asset_pipeline():
    pipeline = build_default_asset_pipeline()

    # Ensure pipeline contains the four default rules:
    #     - AssetNameIsRequiredRule
    #     - AssetNameIsValidRule
    #     - AssetTypeIsRequiredRule
    #     - AssetTypeIsValidRule
    assert len(pipeline.rules) == 4

    asset = Asset(name="TestCharacterName", asset_type=AssetType.CHARACTER)

    validation_errors = pipeline.validate(asset)

    assert validation_errors == []

    asset.name = None
    asset.asset_type = 1

    validation_errors = pipeline.validate(asset)

    # Three errors are expected since the name being None will not exist and be an
    # invalid type. The remaining error will be refers to an invalid asset type.
    assert len(validation_errors) == 3

    fields = [error.field for error in validation_errors]
    assert "name" in fields
    assert "type" in fields

    assert fields.count("name") == 2
    assert fields.count("type") == 1


def test_build_default_version_pipeline():
    pipeline = build_default_version_pipeline()

    # Ensure pipeline contains the four default rules:
    #     - VersionDepartmentIsRequiredRule
    #     - VersionDepartmentIsValidRule
    #     - VersionIsGreaterThanOneRule
    #     - VersionStatusIsKnownRule
    assert len(pipeline.rules) == 4

    version = Version(asset=1, department="animation")

    validation_errors = pipeline.validate(version)

    assert validation_errors == []

    version.version_number = 0
    version.department = 1

    validation_errors = pipeline.validate(version)

    # Two errors are expected to reflect each updated property being an invalid type
    assert len(validation_errors) == 2

    fields = [error.field for error in validation_errors]
    assert "department" in fields
    assert "version_number" in fields

    assert fields.count("department") == 1
    assert fields.count("version_number") == 1
