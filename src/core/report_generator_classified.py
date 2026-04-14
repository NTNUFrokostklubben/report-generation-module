import sys
import tempfile
from pathlib import Path
import skavl_proto.report_pb2 as rp2

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from entity.report_generation_set import ReportSet
from l10n.l10n import classified_translations as t
from utils.io_tools import image_to_uri, read_tiff_fast

def create_report_classified(report_set: ReportSet) -> str:
    """
    Creates a report based on report_set from frontend.

    :param report_set: the set of anomaly data to create a report based on.
    :return: the gRPC response from the report generator.
    """
    _BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent.parent
    _TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
    _REPORT_DIR =  _REPORT_DIR = _BASE_DIR / "reports"
    _REPORT_DIR.mkdir(exist_ok=True)

    environment = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)))
    report = environment.get_template("classified_report.html")

    css = CSS(str(_TEMPLATE_DIR / "classified_report.css"))
    report_name = (report_set.project_meta_data.project_name.replace(" ", "_") + "_classified-report.pdf")

    with tempfile.TemporaryDirectory() as tmp_dir:
        for image in report_set.anomaly_images:
            arr = read_tiff_fast(
                (Path(report_set.project_meta_data.image_folder_path) / image.image_name).with_suffix(".tif"),
                level=5)
            image.image_uri = image_to_uri(arr, tmp_dir, image.image_name)

        html = HTML(string=report.render(
            artifact_images=[i for i in report_set.anomaly_images if i.anomaly_type == 1],
            color_diff_images=[i for i in report_set.anomaly_images if i.anomaly_type == 2],
            water_mask_images=[i for i in report_set.anomaly_images if i.anomaly_type == 3],
            line_artifact_images=[i for i in report_set.anomaly_images if i.anomaly_type == 4],
            total_images=len(report_set.anomaly_images),
            threshold=report_set.confidence_threshold,
            meta=report_set.project_meta_data,
            t=t[report_set.locale]
            ),
            base_url=str(_TEMPLATE_DIR)
        )

        html.write_pdf(_REPORT_DIR / report_name, stylesheets=[css])


    response = str(_REPORT_DIR / report_name)

    return response
