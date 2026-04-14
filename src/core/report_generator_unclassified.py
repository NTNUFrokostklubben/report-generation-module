import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from entity.report_generation_set import ReportSet
from l10n.l10n import unclassified_translations as t

def create_report_unclassified(report_set: ReportSet):
    """
       Creates a report based report_set from frontend.
       :param report_set: the set of anomaly data to create a report based on.
       :return: the gRPC response from the report generator.
       """
    _BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent.parent
    _TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
    _REPORT_DIR = _REPORT_DIR = _BASE_DIR / "reports"
    _REPORT_DIR.mkdir(exist_ok=True)


    environment = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)))
    report = environment.get_template("unclassified_report.html")


    html = HTML(string=report.render(
        artifact_images = [i for i in report_set.anomaly_images if i.anomaly_type == 1],
        color_diff_images = [i for i in report_set.anomaly_images if i.anomaly_type == 2],
        water_mask_images = [i for i in report_set.anomaly_images if i.anomaly_type == 3],
        line_artifact_images = [i for i in report_set.anomaly_images if i.anomaly_type == 4],
        total_images=len(report_set.anomaly_images),
        threshold=report_set.confidence_threshold,
        meta=report_set.project_meta_data,
        t=t[report_set.locale]
    )
        , base_url=str(_TEMPLATE_DIR))
    css = CSS(str(_TEMPLATE_DIR / "unclassified_report.css"))
    report_name = (report_set.project_meta_data.project_name.replace(" ", "_")+"_unclassified-report.pdf")
    html.write_pdf(_REPORT_DIR / report_name, stylesheets=[css])

    response = str(_REPORT_DIR / report_name)

    return response
