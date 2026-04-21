from dataclasses import dataclass
from typing import Optional

from asset_management_service.models.enums import VersionStatus


@dataclass(slots=True)
class Version:
    """A single iteration describing a specific asset state.

    Version uniqueness is defined by its referenced asset foreign key, department, and
    version number. Only a single version can be created with this specific combination.
    Versions increment linearly by integer values.
    """

    asset: int
    department: str
    version: Optional[int] = None
    status: Optional[VersionStatus] = VersionStatus.INACTIVE
