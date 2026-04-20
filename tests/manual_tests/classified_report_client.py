import os
import sys
import grpc
import skavl_proto.report_pb2 as report_pb2
import skavl_proto.report_pb2_grpc as report_pb2_grpc
import skavl_proto.anomaly_pb2 as anomaly_pb2

HOST = "localhost:50053"

def run():
    request = report_pb2.ReportGenerationRequest(
        project_metadata=anomaly_pb2.ProjectMetadata(
            project_name="NORDMØRE 2025 HX-14365",
            sosi_file_path="/data/nordmore.sos",
            image_folder_path=os.path.abspath(r"C:\Users\name\Skule\2026-vaar\IDATA2901-bachelor-thesis\testing-images"),
        ),
        anomaly_sets=[
            anomaly_pb2.AnomalySet(
                image_name="HX-14365_073_001_14822",
                anomaly_confidence=0.87,
                anomaly_type=anomaly_pb2.AnomalyTypes.COLOR_AVERAGE,
                line_number=73,
                image_number=14822,
                user_classification="test",
            ),
            anomaly_pb2.AnomalySet(
                image_name="HX-14365_073_002_14823",
                anomaly_confidence=0.87,
                anomaly_type=anomaly_pb2.AnomalyTypes.ARTIFACT,
                line_number=73,
                image_number=14823,
                user_classification="test2",
            )
        ],
        confidence_threshold=0.5,
        locale="no",
    )

    with grpc.insecure_channel(HOST) as channel:
        stub = report_pb2_grpc.ReportServiceStub(channel)
        try:
            response = stub.GenerateReportClassified(request, timeout=300)
            print(f"Report URL: {response.report_url}")
        except grpc.RpcError as e:
            print(f"RPC error [{e.code()}]: {e.details()}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    run()
