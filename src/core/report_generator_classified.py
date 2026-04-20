
import sys
import tempfile
from collections import OrderedDict
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from entity.report_generation_set import ReportSet
from l10n.l10n import classified_translations as t
from utils.io_tools import image_to_uri, read_tiff_fast


def _group_by_category(report_set: ReportSet, translations: dict) -> dict:
    known_order = [
        (1, translations["block_artifact"]),
        (2, translations["color_difference"]),
        (3, translations["water_mask"]),
        (4, translations["line_artifact"]),
    ]
    groups = OrderedDict((label, []) for _, label in known_order)
    known_type_labels = dict(known_order)

    for img in report_set.anomaly_images:
        key = img.user_classification or known_type_labels.get(img.anomaly_type, str(img.anomaly_type))
        if key not in groups:
            groups[key] = []
        groups[key].append(img)

    return groups


def create_report_classified(report_set: ReportSet) -> str:
    """
    Creates a report based on report_set from frontend.

    :param report_set: the set of anomaly data to create a report based on.
    :return: the gRPC response from the report generator.
    """
    _BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent.parent
    _TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
    _REPORT_DIR = _BASE_DIR / "reports"
    _REPORT_DIR.mkdir(exist_ok=True)

    locale_t = t[report_set.locale]

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

        anomaly_groups = _group_by_category(report_set, locale_t)

        html = HTML(string=report.render(
            anomaly_groups=anomaly_groups,
            total_images=len(report_set.anomaly_images),
            threshold=report_set.confidence_threshold,
            meta=report_set.project_meta_data,
            t=locale_t,
            ),
            base_url=str(_TEMPLATE_DIR)
        )

        html.write_pdf(_REPORT_DIR / report_name, stylesheets=[css])

    return str(_REPORT_DIR / report_name)
