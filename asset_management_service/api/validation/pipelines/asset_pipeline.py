from asset_management_service.api.validation.core import ValidationPipeline
from asset_management_service.api.validation.rules.asset_rules import (
    AssetNameIsRequiredRule,
    AssetNameIsValidRule,
    AssetTypeIsRequiredRule,
    AssetTypeIsValidRule,
)
from asset_management_service.models.asset import Asset


def build_default_asset_pipeline() -> ValidationPipeline[Asset]:
    """
    Build a default asset validation pipeline.

    Returns:
        ValidationPipeline[Asset]: A collection of all asset validation rules.
    """

    return ValidationPipeline[Asset](
        rules=[
            AssetNameIsRequiredRule(),
            AssetNameIsValidRule(),
            AssetTypeIsRequiredRule(),
            AssetTypeIsValidRule(),
        ]
    )
