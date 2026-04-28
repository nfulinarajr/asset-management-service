import sqlite3

from typing import Optional

from asset_management_service.common import logger
from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType, VersionStatus
from asset_management_service.models.version import Version


LOGGER = logger.get_logger("SQLiteDatabase")


class SQLiteDatabase:
    """
    A SQLite persistence layer to store asset and version data.

    Args:
        path (str): The location of the data store. If one is not provided, an in-memory
            SQLite database will be created instead.
    """

    def __init__(self, path: str = ":memory:") -> None:
        # Open a connection to the SQLite database using the provided path
        self._connection = sqlite3.connect(path)

        # Update the connection so queried rows will behave more like dicts than tuples
        self._connection.row_factory = sqlite3.Row

        # Initialize the schema
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        LOGGER.debug("Initializing database schema")

        cursor = self._connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                UNIQUE(name, type)
            );

            CREATE TABLE IF NOT EXISTS versions (
                asset_id INTEGER NOT NULL,
                department TEXT NOT NULL,
                version_number INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY(asset_id) REFERENCES assets(asset_id),
                UNIQUE(asset_id, department, version_number)
            );
            """
        )

        self._connection.commit()

    def add_asset(self, asset: Asset) -> Asset:
        """
        Add an asset to the database.

        Args:
            asset (Asset): The asset to add.

        Returns:
            Asset: The newly added asset.
        """

        LOGGER.debug("Adding asset for {}".format(asset.name))

        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO assets (name, type) VALUES (?, ?)",
            (asset.name, asset.asset_type.value),
        )

        self._connection.commit()

        # Update the asset now that it has a reference id
        asset.id = cursor.lastrowid

        LOGGER.debug("{} has been added!".format(asset.name))

        return asset

    def add_version(self, asset: Asset, version: Version) -> Version:
        """
        Add a version to the database.

        Args:
            asset (Asset): The asset to reference.
            version (Version): The version to add.

        Returns:
            Version: The newly added version.
        """

        LOGGER.debug("Adding version for {}".format(asset.name))

        if asset.id is None:
            raise ValueError("Versions must be associated with a valid asset id.")

        version_number = version.version_number

        if version_number is None:
            # Ensure the version number exists and if not, increment the latest
            latest_version_number = self.get_last_version_number(asset.id)

            if latest_version_number:
                version_number = latest_version_number + 1
            else:
                version_number = 1

        cursor = self._connection.cursor()

        cursor.execute(
            """
            INSERT INTO
            versions (asset_id, department, version_number, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                asset.id,
                version.department,
                version_number,
                version.status.value,
            ),
        )

        self._connection.commit()

        LOGGER.debug("{} has been added!".format(asset.name))

        return Version(
            asset.id,
            version.department,
            version_number=version_number,
            status=version.status,
        )

    def get_asset(self, name: str) -> Optional[Asset]:
        """
        Get the asset corresponding to the provided asset name.

        Args:
            name (str): The name of the asset to get.

        Returns:
            Asset | None: The asset corresponding to the provided asset name, or None if
                not found.
        """

        LOGGER.debug("Getting asset for {}".format(name))

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM assets WHERE name = ?",
            (name,),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return Asset(
            row["name"],
            AssetType(row["type"]),
            id=row["asset_id"],
        )

    def get_version(self, asset_id: int, version_number: int) -> Optional[Version]:
        """
        Get the version corresponding to the provided asset id and version number.

        Args:
            asset_id (int): The asset id necessary to retrieve all associated versions.
            version_number (int): The specific version to get.

        Returns:
            Version | None: The version corresponding to the provided asset id and
                version number, or None if not found.
        """

        LOGGER.debug("Getting version for {}".format(asset_id))

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM versions WHERE asset_id = ? AND version_number = ?",
            (asset_id, version_number),
        )

        row = cursor.fetchone()

        if not row:
            return None

        return Version(
            asset_id,
            row["department"],
            version_number=row["version_number"],
            status=VersionStatus(row["status"]),
        )

    def get_last_version_number(self, asset_id: int) -> Optional[int]:
        """
        Get the last version number.

        Args:
            asset_id (int): The asset id necessary to retrieve the last version number.

        Returns:
            int: The last version number.
        """

        LOGGER.debug("Getting latest version for {}".format(asset_id))

        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT * FROM versions WHERE asset_id = ? "
            "ORDER BY version_number DESC LIMIT 1",
            (asset_id,),
        )

        row = cursor.fetchone()

        return row["version_number"] if row else None

    def list_assets(self) -> list[Asset]:
        """
        List all assets.

        Returns:
            list[Asset]: All asset entries within the database.
        """

        LOGGER.debug("Listing assets")

        cursor = self._connection.cursor()

        cursor.execute("SELECT * FROM assets ORDER BY name ASC, type ASC")

        assets = []
        for row in cursor.fetchall():
            assets.append(
                Asset(
                    row["name"],
                    AssetType(row["type"]),
                    id=row["asset_id"],
                )
            )

        return assets

    def list_versions(self, asset_id: int) -> list[Version]:
        """
        List all versions associated with a specific asset.

        Args:
            asset_id (int): The id necessary to retrieve all associated versions.

        Returns:
            list[Version]: All versions corresponding to an asset with the provided id.
        """

        LOGGER.debug("Listing versions for {}".format(asset_id))

        cursor = self._connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM versions
            WHERE asset_id = ?
            ORDER BY department, version_number, status
            """,
            (asset_id,),
        )

        versions = []
        for row in cursor.fetchall():
            versions.append(
                Version(
                    asset_id,
                    row["department"],
                    version_number=row["version_number"],
                    status=VersionStatus(row["status"]),
                )
            )

        return versions

    def close(self) -> None:
        """
        Safely close the connection.
        """

        self._connection.close()
