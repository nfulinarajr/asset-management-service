from dataclasses import dataclass
from typing import Optional

from asset_management_service.models.enums import AssetType


@dataclass(slots=True)
class Asset:
    """A named, versioned, and structured container for a resource.

    Asset uniqueness is defined by its name and type. Multiple assets with the same name
    and type are not allowed. However, multiple assets with the same name and different
    types, or different names and the same type, are valid. Each asset should have at
    least one version associated with it with no duplicate versions.
    """

    name: str
    asset_type: AssetType
    id: Optional[int] = None
