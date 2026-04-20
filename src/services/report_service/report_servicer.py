
import  skavl_proto.report_pb2_grpc as rpc2
import skavl_proto.report_pb2 as rp2
from core.report_generator import ReportGenerator
from entity import anomaly_set
from entity.anomaly_set import AnomalySet
from entity.project_meta_data import ProjectMetaData
from entity.report_generation_set import ReportSet
from skavl_proto.report_pb2 import ReportGenerationRequest, ReportGenerationResponse


def create_report_set(request: ReportGenerationRequest) -> ReportSet:
    """
    Create a report set from the given RPC request and return it.
    :param request: the RPC request containing the data to create the report set from.
    :return: the created report set.
    """

    metadata = ProjectMetaData(project_name=request.project_metadata.project_name,
                               sosi_file_path=request.project_metadata.sosi_file_path,
                               image_folder_path=request.project_metadata.image_folder_path,
                               sosi_water_mask_path=request.project_metadata.sosi_water_mask_path
                               if request.project_metadata.HasField("sosi_water_mask_path") else None)
    anomaly_images = []
    for image_set in request.anomaly_sets:
        anomaly_images.append(AnomalySet(
            image_name=image_set.image_name,
            anomaly_confidence=image_set.anomaly_confidence,
            anomaly_type=image_set.anomaly_type,
            line_number=image_set.line_number,
            image_number=image_set.image_number,
            tiff_coordinate=(image_set.geotiff_coordinate.easting, image_set.geotiff_coordinate.northing),
            image_uri=None,
            user_classification=image_set.user_classification if image_set.HasField("user_classification") else None,
        ))

    report_set = ReportSet(project_meta_data=metadata,
                           anomaly_images=anomaly_images,
                           confidence_threshold=request.confidence_threshold,
                           locale=request.locale)
    return report_set


class ReportServicer(rpc2.ReportServiceServicer):
    """
    Represents a service for creating reports.
    Contains the gRPC methods for creating both classified and unclassified reports.
    """
    _report_gen = None
    def __init__(self):
        self._report_gen = ReportGenerator()

    def GenerateReportUnclassified(self, request:ReportGenerationRequest, context)->ReportGenerationResponse:
        """
        Create a report with unclassified anomaly images over a certain confidence threshold. Unclassified in this context
        means no human has look at the images and determined the anomaly type,
         but the report will still contain the confidence score for each image.

        :param request: the RPC request containing the data to create the report from.
        :param context: the RPC context, contains standard rpc methods.
        :return:
        """

        report_set = create_report_set(request)
        response = rp2.ReportGenerationResponse()
        response.report_url = self._report_gen.create_report_unclassified(report_set)
        return response

    def GenerateReportClassified(self, request:ReportGenerationRequest, context)->ReportGenerationResponse:
        """
         Create a report with classified anomaly images over a certain confidence threshold. Classified in this context
        means a human has look at the images and determined the anomaly type.

        :param request:
        :param context:
        :return:
        """
        report_set = create_report_set(request)
        response = rp2.ReportGenerationResponse()
        response.report_url = self._report_gen.create_report_classified(report_set)
        return response
