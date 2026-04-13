
import  skavl_proto.report_pb2_grpc as rpc2
from core import create_report_unclassified
from core.report_generator_classified import create_report_classified
from entity.project_meta_data import ProjectMetaData
from entity.report_generation_set import ReportSet
from skavl_proto.report_pb2 import ReportGenerationRequest, ReportGenerationResponse


def create_report_set(request: ReportGenerationRequest) -> ReportSet:
    metadata = ProjectMetaData(project_name=request.project_metadata.project_name,
                               sosi_file_path=request.project_metadata.sosi_file_path,
                               image_folder_path=request.project_metadata.image_folder_path,
                               sosi_water_mask_path=request.project_metadata.sosi_water_mask_path
                               if request.project_metadata.HasField("sosi_water_mask_path") else None)
    anomaly_images = []
    for image_set in request.anomaly_sets:
        anomaly_images.append(image_set)

    report_set = ReportSet(project_meta_data=metadata,
                           anomaly_images=anomaly_images, confidence_threshold=request.confidence_threshold)
    return report_set


class ReportServicer(rpc2.ReportServiceServicer):

    def GenerateReportUnclassified(self, request:ReportGenerationRequest, context)->ReportGenerationResponse:
        report_set = create_report_set(request)
        return create_report_unclassified(report_set)

    def GenerateReportClassified(self, request:ReportGenerationRequest, context)->ReportGenerationResponse:
        report_set = create_report_set(request)
        return create_report_classified(report_set)
