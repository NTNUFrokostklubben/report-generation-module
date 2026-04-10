from hashlib import algorithms_available
from pathlib import Path
from turtledemo.tree import tree

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


def main():
    anomaly_image = "HX-14365_073_001_14822"
    conf = 0.3*100
    analysed_images = 1000
    threshold = 0.5*100
    project_name ="NORDMØRE 2025 HX-14365"
    _TEMPLATE_DIR = Path(__file__).parent.parent / "templates"

    environment = Environment(loader=FileSystemLoader(str(_TEMPLATE_DIR)))
    report = environment.get_template("unclassified_report.html")

    html = HTML(string=report.render(anomaly_image=anomaly_image, confidence=conf,
                                     total_images=analysed_images, threshold=threshold, project_name=project_name)
                , base_url=str(_TEMPLATE_DIR))
    css = CSS(str(_TEMPLATE_DIR / "unclassified_report.css"))
    html.write_pdf('report.pdf', stylesheets=[css])
