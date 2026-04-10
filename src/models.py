from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UtmCoordinate:
    easting: float
    northing: float


@dataclass
class AnomalySet:
    """Per-image anomaly result. Mirrors AnomalySet in anomaly.proto."""
    image_name: str
    anomaly_confidence: float
    line_number: int
    image_number: int
    geotiff_coordinate: Optional[UtmCoordinate] = None


@dataclass
class ProjectMetadata:
    """Mirrors ProjectMetadata in anomaly.proto."""
    project_name: str
    sosi_file_path: str
    image_folder_path: str
    sosi_water_mask_path: Optional[str] = None


@dataclass
class AnomalyResponse:
    """Top-level input to the report generator. Mirrors AnomalyResponse in anomaly.proto."""
    project_metadata: ProjectMetadata
    last_processed_index: int
    anomaly_sets: list[AnomalySet] = field(default_factory=list)
