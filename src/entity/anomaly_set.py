from dataclasses import dataclass

from entity.enum.analysis_t import AnalysisType


@dataclass
class AnomalySet:
    """
    AnomalySet is a dataclass used to store the results of an analysis in a structured way.
    It contains the image name, the confidence level of the anomaly, the type of analysis, the line number,
     the image number and the tiff coordinate of the image.
    This class is used to store the results of the analysis in a structured way, so that it can be easily
     used for report generation and other purposes.

    """

    image_name :str
    anomaly_confidence:float
    anomaly_type: AnalysisType
    line_number: int
    image_number: int
    tiff_coordinate: tuple[float, float]