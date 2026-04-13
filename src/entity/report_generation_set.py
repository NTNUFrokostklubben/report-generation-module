from dataclasses import dataclass

from entity.anomaly_set import AnomalySet
from entity.project_meta_data import ProjectMetaData


@dataclass
class ReportSet:
    """
    Represents a report set. Contains all data sent from frontend, for use in creating reports.
    """
    project_meta_data: ProjectMetaData
    anomaly_images: list[AnomalySet]
    confidence_threshold: float