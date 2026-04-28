
import sys
import tempfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS
from entity.report_generation_set import ReportSet
from l10n.l10n import classified_translations as t_classified, unclassified_translations as t_unclassified
from utils.io_tools import image_to_uri, read_tiff_fast
from collections import OrderedDict
from entity.report_generation_set import ReportSet

class ReportGenerator:
    _BASE_DIR = None
    _TEMPLATE_DIR = None
    _REPORT_DIR = None
    env = None

    def __init__(self):
        self._BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent.parent
        self._TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
        self._REPORT_DIR = self._BASE_DIR / "reports"
        self._REPORT_DIR.mkdir(exist_ok=True)
        self.env = Environment(loader=FileSystemLoader(str(self._TEMPLATE_DIR)))

    def create_report_classified(self, report_set: ReportSet) -> str:
        """
        Creates a report based on report_set from frontend.

        :param report_set: the set of anomaly data to create a report based on.
        :return: the gRPC response from the report generator.
        """

        locale_t = t_classified[report_set.locale]
        report = self.env.get_template("classified_report.html")

        css = CSS(str(self._TEMPLATE_DIR / "classified_report.css"))
        report_name = (report_set.project_meta_data.project_name.replace(" ", "_") + "_classified-report.pdf")

        with tempfile.TemporaryDirectory() as tmp_dir:
            for image in report_set.anomaly_images:
                arr = read_tiff_fast(
                    (Path(report_set.project_meta_data.image_folder_path) / image.image_name).with_suffix(".tif"),
                    level=5)
                image.image_uri = image_to_uri(arr, tmp_dir, image.image_name)

            anomaly_groups = self._group_by_category(report_set, locale_t)

            html = HTML(string=report.render(
                anomaly_groups=anomaly_groups,
                total_images=len(report_set.anomaly_images),
                threshold=report_set.confidence_threshold,
                meta=report_set.project_meta_data,
                t=locale_t,
                ),
                base_url=str(self._TEMPLATE_DIR)
            )

            html.write_pdf(self._REPORT_DIR / report_name, stylesheets=[css])

        return str(self._REPORT_DIR / report_name)



    def create_report_unclassified(self, report_set: ReportSet):
        """
           Creates a report based report_set from frontend.
           :param report_set: the set of anomaly data to create a report based on.
           :return: the gRPC response from the report generator.
           """
        locale_t = t_unclassified[report_set.locale]
        report = self.env.get_template("unclassified_report.html")

        anomaly_groups = self._group_by_category(report_set, locale_t)

        html = HTML(string=report.render(
            anomaly_groups=anomaly_groups,
            total_images=len(report_set.anomaly_images),
            threshold=report_set.confidence_threshold,
            meta=report_set.project_meta_data,
            t=locale_t,
        ), base_url=str(self._TEMPLATE_DIR))
        css = CSS(str(self._TEMPLATE_DIR / "unclassified_report.css"))
        report_name = (report_set.project_meta_data.project_name.replace(" ", "_") + "_unclassified-report.pdf")
        html.write_pdf(self._REPORT_DIR / report_name, stylesheets=[css])

        return str(self._REPORT_DIR / report_name)


    def _group_by_category(self, report_set: ReportSet, translations: dict) -> dict:
        """
        Group reports by category, where first four are the defined types of anomalies
         and the rest are user classifications or unknown types.
        Args:
            report_set: the set of anomaly data to group.
            translations: the translations for the current locale, used to get the correct labels for the known types.

        Returns:
        a dictionary where the keys are the category labels and the values are lists of anomaly images
          belonging to that category.
        """
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