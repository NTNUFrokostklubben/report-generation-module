import argparse
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
    parser = argparse.ArgumentParser(
        prog="skavl-anomaly-detection-module",
        description="Anomaly detection in aerial images")

    parser.add_argument("-p", "--port", help="Port to start tiler server with", default=50053)
    parser.add_argument("-l", "--local", action="store_true",
                        help="""Determines if all or only local connections should be accepted. 
                                   If this argument is present, the servers IP will be 127.0.0.1, 
                                   if this argument is omitted, the ip will be set to 0.0.0.0 meaning accept all connections""")

    args = parser.parse_args()

    Path("reports").mkdir(exist_ok=True)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    rpg2.add_ReportServiceServicer_to_server(ReportServicer(), server)

    # Accepts connections only locally when running locally.
    server_port = getattr(args, "port")
    server_ip = ""
    if getattr(args, "local", False):
        server_ip = "127.0.0.1"
    else:
        server_ip = "0.0.0.0"
    server.add_insecure_port(f"{server_ip}:{server_port}")

    server.start()
    print(f"gRPC server listening on {server_ip}:{server_port}")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()