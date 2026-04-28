import pytest
import sqlite3

from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType, VersionStatus
from asset_management_service.models.version import Version
from asset_management_service.storage.sqlite_database import SQLiteDatabase


CHARACTER_NAME = "TestCharacterName"
DEPARTMENT = "Animation"


@pytest.fixture
def sqlite_database():
    """
    Text fixture to provide a SQLiteDatabase instance for each test run.

    The SQLiteDatabase safely closes when no longer in use.

    Yields:
        SQLiteDatabase: The newly created SQLiteDatabase instance to test with.
    """

    database = SQLiteDatabase()

    try:
        yield database
    finally:
        database.close()


def test_empty_database(sqlite_database: SQLiteDatabase):
    assets = sqlite_database.list_assets()

    assert assets == []


def test_add_asset(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    assert added_asset.id is not None
    assert added_asset.name == CHARACTER_NAME
    assert added_asset.asset_type == AssetType.CHARACTER


def test_add_version(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    version = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        version_number=1,
        status=VersionStatus.ACTIVE,
    )
    added_version = sqlite_database.add_version(asset=added_asset, version=version)

    assert added_version is not None
    assert added_version.asset == added_asset.id
    assert added_version.department == DEPARTMENT
    assert added_version.version_number == 1
    assert added_version.status == VersionStatus.ACTIVE


def test_add_version_without_asset_id(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)

    version = Version(
        asset=asset.id,
        department=DEPARTMENT,
        version_number=1,
        status=VersionStatus.ACTIVE,
    )

    # Attempt to add the version to the database. The expectation is a thrown exception
    # due to the asset not yet persisting.
    with pytest.raises(ValueError):
        sqlite_database.add_version(asset=asset, version=version)


def test_get_asset(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    sqlite_database.add_asset(asset)

    found_asset = sqlite_database.get_asset(name=CHARACTER_NAME)

    assert found_asset is not None


def test_get_asset_does_not_exist(sqlite_database: SQLiteDatabase):
    assert not sqlite_database.get_asset(name="DoesNotExist")


def test_get_version(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    version_v1 = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        version_number=1,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_version(asset=added_asset, version=version_v1)

    version_v2 = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        status=VersionStatus.ACTIVE,
    )
    sqlite_database.add_version(asset=added_asset, version=version_v2)

    found_asset = sqlite_database.get_version(asset_id=added_asset.id, version_number=2)

    assert found_asset is not None
    assert found_asset.department == DEPARTMENT
    assert found_asset.version_number == 2
    assert found_asset.status == VersionStatus.ACTIVE


def test_list_assets(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    version_v1 = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_version(asset=added_asset, version=version_v1)

    all_assets = sqlite_database.list_assets()

    assert len(all_assets) == 1


def test_list_versions(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    added_asset = sqlite_database.add_asset(asset)

    version_v1 = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_version(asset=added_asset, version=version_v1)

    version_v2 = Version(
        asset=added_asset.id,
        department=DEPARTMENT,
        status=VersionStatus.ACTIVE,
    )
    sqlite_database.add_version(asset=added_asset, version=version_v2)

    another_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.PROP)
    another_added_asset = sqlite_database.add_asset(another_asset)

    another_version_v1 = Version(
        asset=another_added_asset.id,
        department=DEPARTMENT,
        status=VersionStatus.INACTIVE,
    )
    sqlite_database.add_version(asset=another_added_asset, version=another_version_v1)

    all_versions = sqlite_database.list_versions(asset_id=added_asset.id)

    assert len(all_versions) == 2


def test_duplicate_assets(sqlite_database: SQLiteDatabase):
    original_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    duplicated_asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)

    sqlite_database.add_asset(original_asset)

    # Attempt to add the duplicate asset to the database. The expectation is a thrown
    # exception due to asset name and type defining uniqueness.
    with pytest.raises(sqlite3.IntegrityError):
        sqlite_database.add_asset(duplicated_asset)


def test_duplicate_versions(sqlite_database: SQLiteDatabase):
    asset = Asset(name=CHARACTER_NAME, asset_type=AssetType.CHARACTER)
    sqlite_database.add_asset(asset=asset)

    version_v1 = Version(
        asset=asset.id,
        department=DEPARTMENT,
        status=VersionStatus.ACTIVE,
    )

    version_v2 = Version(
        asset=asset.id,
        department=DEPARTMENT,
        version_number=1,
        status=VersionStatus.ACTIVE,
    )

    sqlite_database.add_version(asset=asset, version=version_v1)

    # Attempt to add the duplicate asset to the database. The expectation is a thrown
    # exception due to asset id, department, and version number defining uniqueness.
    with pytest.raises(sqlite3.IntegrityError):
        sqlite_database.add_version(asset=asset, version=version_v2)
