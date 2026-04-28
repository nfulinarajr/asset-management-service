import pytest

from pathlib import Path

from asset_management_service.api.service import AssetManagementService
from asset_management_service.api.validation.pipelines.asset_pipeline import (
    build_default_asset_pipeline,
)
from asset_management_service.api.validation.pipelines.version_pipeline import (
    build_default_version_pipeline,
)
from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType, VersionStatus
from asset_management_service.models.version import Version
from asset_management_service.storage.sqlite_database import SQLiteDatabase


ASSET_TYPE = AssetType.CHARACTER
CHARACTER_NAME = "TestCharacterName"
DEPARTMENT = "Animation"
VERSION_STATUS = VersionStatus.ACTIVE


@pytest.fixture
def sqlite_database(tmp_path: Path):
    """
    Test fixture to provide a SQLiteDatabase instance for each test run.

    The SQLiteDatabase safely closes when no longer in use.

    Yields:
        SQLiteDatabase: The newly created SQLiteDatabase instance to test with.
    """

    data_store_path = tmp_path / "sqlite_database.db"

    yield data_store_path


@pytest.fixture
def asset_service(sqlite_database: Path) -> AssetManagementService:
    """Test fixture to provide an asset service instance for each test run.

    Args:
        sqlite_database (SQLiteDatabase): The sqlite database used for tests.

    Returns:
        AssetManagementService: The service to execute tests on.
    """

    return AssetManagementService(
        data_store_path=sqlite_database,
        asset_pipeline=build_default_asset_pipeline(),
        version_pipeline=build_default_version_pipeline(),
    )


def test_service_load_assets(asset_service: AssetManagementService):
    tests_directory = Path(__file__).parent
    sample_data = tests_directory / "sample_data.json"

    assert asset_service.load_assets(file_path=sample_data) is None


def test_service_add_asset(asset_service: AssetManagementService):
    assert asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))


def test_service_add_version(asset_service: AssetManagementService):
    asset = asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))
    version = Version(asset=asset.id, department=DEPARTMENT, status=VERSION_STATUS)

    assert asset_service.add_version(asset, version)


def test_service_list_assets(asset_service: AssetManagementService):
    assert len(asset_service.list_assets()) == 0

    asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))

    assert len(asset_service.list_assets()) == 1


def test_service_get_asset(asset_service: AssetManagementService):
    asset = asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))

    assert asset_service.get_asset(asset.name)


def test_service_get_version(asset_service: AssetManagementService):
    asset = asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))
    version = Version(asset=asset.id, department=DEPARTMENT, status=VERSION_STATUS)
    asset_service.add_version(asset, version)

    assert asset_service.get_version(asset.name, 1)


def test_service_list_versions(asset_service: AssetManagementService):
    asset = asset_service.add_asset(Asset(name=CHARACTER_NAME, asset_type=ASSET_TYPE))
    version_v1 = Version(asset=asset.id, department=DEPARTMENT, status=VERSION_STATUS)
    version_v2 = Version(asset=asset.id, department=DEPARTMENT, status=VERSION_STATUS)
    version_v3 = Version(asset=asset.id, department=DEPARTMENT, status=VERSION_STATUS)

    asset_service.add_version(asset, version_v1)

    assert len(asset_service.list_versions(asset.name)) == 1

    asset_service.add_version(asset, version_v2)

    assert len(asset_service.list_versions(asset.name)) == 2

    asset_service.add_version(asset, version_v3)

    assert len(asset_service.list_versions(asset.name)) == 3
