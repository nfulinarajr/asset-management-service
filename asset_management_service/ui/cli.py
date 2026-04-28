import argparse

from pathlib import Path
from typing import Optional

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


def get_asset_type_from_input() -> Optional[AssetType]:
    """
    Get the asset type from the user input

    Returns:
        AssetType | None: The asset type from valid user input, or None if not.
    """

    print_asset_types()

    user_input = input("\nPlease provide a type for your asset: ").strip().lower()

    try:
        if user_input.startswith(("1", "1.")):
            asset_type = AssetType("character")
        elif user_input.startswith(("2", "2.")):
            asset_type = AssetType("dressing")
        elif user_input.startswith(("3", "3.")):
            asset_type = AssetType("environment")
        elif user_input.startswith(("4", "4.")):
            asset_type = AssetType("fx")
        elif user_input.startswith(("5", "5.")):
            asset_type = AssetType("prop")
        elif user_input.startswith(("6", "6.")):
            asset_type = AssetType("set")
        elif user_input.startswith(("7", "7.")):
            asset_type = AssetType("vehicle")
        else:
            asset_type = AssetType(user_input)
    except ValueError as error:
        print("\n{} is not a valid asset type: {}".format(error))
        asset_type = None

    return asset_type


def get_version_status_from_input() -> Optional[VersionStatus]:
    """
    Get the version status from the user input.

    Returns:
        VersionStatus | None: The version status from valid user input, or None if not.
    """

    print_version_statuses()

    user_input = input("\nPlease provide a version status: ").strip().lower()

    try:
        if user_input.startswith(("1", "1.")):
            version_status = VersionStatus("active")
        elif user_input.startswith(("2", "2.")):
            version_status = VersionStatus("inactive")
        else:
            version_status = VersionStatus(user_input)
    except ValueError:
        print("\n{} is not a valid version status.".format(user_input))
        version_status = None

    return version_status


def print_asset_types():
    print("\n***********")
    print("Asset Types")
    print("***********")
    print("\n1. character")
    print("2. dressing")
    print("3. environment")
    print("4. fx")
    print("5. prop")
    print("6. set")
    print("7. vehicle")


def print_version_info(asset: Asset, version: Version):
    print("\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value))
    print("\nDepartment: {}".format(version.department))
    print("Version Number: {}".format(version.version_number))
    print("Status: {}".format(version.status.value))


def print_main_menu():
    print("\n************************")
    print("Asset Management Service")
    print("************************")
    print(
        "\nWelcome to the Asset Management Service!\n\nThis is a simple Asset and "
        "Version API\n\nWhat would you like to do?"
    )
    print("\n1. Load assets")
    print("2. Add asset")
    print("3. Add version")
    print("4. Get asset")
    print("5. Get version")
    print("6. List assets")
    print("7. List versions")
    print("8. Exit")


def print_version_statuses():
    print("\n****************")
    print("Version Statuses")
    print("****************")
    print("1. active")
    print("2. inactive")


def build_parser() -> argparse.ArgumentParser:
    """
    Parse arguments.

    Returns:
        argparse.ArgumentParser: The ArgumentParser object
    """

    parser = argparse.ArgumentParser(
        prog="Asset Management Service CLI",
        description="A simple asset and version management API",
    )

    parser.add_argument(
        "--data-store-path",
        type=Path,
        default=None,
        help="The data_store path (default: None)",
    )

    return parser


def create_asset_service(data_store_path: Path | None) -> AssetManagementService:
    """
    Create the asset service to interact with the data store.

    Args:
        data_store_path (Path): The data store location.

    Returns:
        AssetManagementService: The asset management service.
    """

    if data_store_path is None:
        database_directory = Path(__file__).parent
        sqlite_database = database_directory / "sqlite_database.db"
        data_store_path = Path(sqlite_database)

    asset_pipeline = build_default_asset_pipeline()
    version_pipeline = build_default_version_pipeline()

    asset_service = AssetManagementService(
        data_store_path, asset_pipeline, version_pipeline
    )
    return asset_service


def launch_menu_loop(asset_service: AssetManagementService):
    """
    The main CLI menu loop.

    Args:
        asset_service (AssetManagementService): The asset service to execute actions on.
    """

    while True:
        print_main_menu()

        choice = input("> ").strip().lower()

        if choice == "1":
            user_input = input("\nPlease provide a JSON file path to load: ").strip()

            # Handle empty submission
            if not user_input:
                print("\nNo file path was provided.")
                continue

            file_path = Path(user_input)

            # Check file path validity
            if not file_path.is_file() or not user_input.endswith(".json"):
                print("\n{} is not a valid JSON file.".format(file_path))
                continue

            try:
                asset_service.load_assets(file_path)
            except Exception as error:
                print("Error loading assets: {}".format(error))
        elif choice == "2":
            asset_name = (
                input("\nPlease provide a name for your asset: ").strip().lower()
            )

            asset_type = get_asset_type_from_input()

            if asset_type is None:
                print("Could not add {} due to invalid input.".format(asset_name))

            try:
                asset_service.add_asset(Asset(asset_name, asset_type))
            except Exception as error:
                print("\nError adding the asset: {}".format(error))
        elif choice == "3":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset_type = get_asset_type_from_input()
            department = input("Please provide a department: ").strip().lower()
            version_status = get_version_status_from_input()

            # Determine if an asset exists with the same name and create one if not
            asset = asset_service.get_asset(asset_name)

            if not asset:
                try:
                    asset = asset_service.add_asset(Asset(asset_name, asset_type))
                except Exception as error:
                    print("Error adding the asset: {}".format(error))
                    continue

            try:
                version = Version(asset.id, department, status=version_status)
                asset_service.add_version(asset, version)
            except Exception as error:
                print("Error adding the version: {}".format(error))
        elif choice == "4":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            try:
                asset = asset_service.get_asset(asset_name)

                if asset:
                    print(
                        "\nAsset Name: {} ({})".format(
                            asset.name, asset.asset_type.value
                        )
                    )
                else:
                    print("\nCould not find an asset for {}".format(asset_name))
            except Exception as error:
                print("Error getting asset: ".format(error))
        elif choice == "5":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset = asset_service.get_asset(asset_name)

            if not asset:
                print("\nCould not find an asset for {}".format(asset_name))
                continue

            version_number = (
                input("Please provide the version number: ").strip().lower()
            )

            try:
                version = asset_service.get_version(asset_name, version_number)

                if version:
                    print_version_info(asset, version)
                else:
                    print(
                        "\nCould not find version {} for {}".format(version, asset_name)
                    )
            except Exception as error:
                print("\nError getting version: {}".format(error))
        elif choice == "6":
            for asset in asset_service.list_assets():
                print(
                    "\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value)
                )
        elif choice == "7":
            asset_name = input("\nPlease provide the asset name: ").strip().lower()

            asset = asset_service.get_asset(asset_name)

            if not asset:
                print("\nCould not find an asset for {}".format(asset_name))
                continue

            print("\nAsset Name: {} ({})".format(asset.name, asset.asset_type.value))

            for version in asset_service.list_versions(asset_name):
                print("\nDepartment: {}".format(version.department))
                print("Version Number: {}".format(version.version_number))
                print("Status: {}".format(version.status.value))
        elif choice == "8":
            break
        else:
            print("\nInvalid option. Please try again.")


def launch_asset_service_cli(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    asset_service = create_asset_service(args.data_store_path)

    launch_menu_loop(asset_service)
