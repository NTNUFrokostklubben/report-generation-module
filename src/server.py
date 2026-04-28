from concurrent import futures
from pathlib import Path

import grpc
import skavl_proto.report_pb2_grpc as rpg2
import time

from services.report_service.report_servicer import ReportServicer


def serve():
    """
    Create and start gRPC server and serve it.
    """
    Path("reports").mkdir(exist_ok=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpg2.add_ReportServiceServicer_to_server(ReportServicer(), server)
    server.add_insecure_port("0.0.0.0:50053")
    server.start()
    print("gRPC server listening on 0.0.0.0:50053")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()