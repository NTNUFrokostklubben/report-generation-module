from dataclasses import dataclass
from typing import Optional


@dataclass
class ProjectMetaData:
    """
    Represents a project metadata. Contains all metadata about the project.
    """
    project_name: str
    sosi_file_path: str
    image_folder_path: str
    sosi_water_mask_path: Optional[str] = None