from asset_management_service.api.validation.errors import ValidationError
from asset_management_service.models.asset import Asset
from asset_management_service.models.enums import AssetType


class AssetNameIsRequiredRule:
    """
    Validation rule to ensure asset name exists.
    """

    def validate(self, asset: Asset) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not asset.name:
            validation_errors.append(
                ValidationError(field="name", message="Asset must define a valid name")
            )

        return validation_errors


class AssetNameIsValidRule:
    """
    Validation rule to ensure data type is correct.
    """

    def validate(self, asset: Asset) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not isinstance(asset.name, str):
            validation_errors.append(
                ValidationError(field="name", message="Asset name must be of type str")
            )

        return validation_errors


class AssetTypeIsRequiredRule:
    """
    Validation rule to ensure asset type exists.
    """

    def validate(self, asset: Asset) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not asset.asset_type:
            validation_errors.append(
                ValidationError(field="type", message="Asset must define a valid type")
            )

        return validation_errors


class AssetTypeIsValidRule:
    """
    Validation rule to ensure data type is correct.
    """

    def validate(self, asset: Asset) -> list[ValidationError]:
        validation_errors: list[ValidationError] = []

        if not isinstance(asset.asset_type, AssetType):
            validation_errors.append(
                ValidationError(
                    field="type", message="Asset type must be of type AssetType"
                )
            )

        return validation_errors
