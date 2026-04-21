from enum import Enum


class AssetType(Enum):
    """
    Represents all valid asset types.

    Inherits:
        Enum
    """

    CHARACTER = "character"
    DRESSING = "dressing"
    ENVIRONMENT = "environment"
    FX = "fx"
    PROP = "prop"
    SET = "set"
    VEHICLE = "vehicle"


class VersionStatus(Enum):
    """
    Represents all valid version statuses.

    Inherits:
        Enum
    """

    ACTIVE = "active"
    INACTIVE = "inactive"
