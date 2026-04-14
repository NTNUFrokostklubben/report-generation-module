from enum import Enum

class AnalysisType(Enum):
    """
    Enum used to define the type of analysis to use.
    types:
    COLOR_AVERAGE, WATER_MASK, ARTIFACT
    """

    COLOR_AVERAGE = 1
    WATER_MASK = 2
    ARTIFACT = 3
    ARTIFACT_LINE = 3

