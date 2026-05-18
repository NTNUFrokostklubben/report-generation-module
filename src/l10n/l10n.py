"""
File for holding translations for the application. The translations are stored in dictionaries,
 where the keys are the language codes (e.g. "en" for English, "no" for Norwegian)
  and the values are dictionaries containing the translations for each key used in the application.
"""

_norwegian = {
    "project": "Prosjekt",
    "confidence_threshold": "Konfidensgrense",
    "anomalous_images": "Avvikende bilder",
    "undefined": "Udefinert",
    "block_artifact": "Blokkartefakt",
    "color_difference": "Fargeforskjell",
    "water_mask": "Vannmaske",
    "line_artifact": "Linjeartefakt",
    "confidence": "Konfidens",
}

common_translations = {
    "en": {
        "project": "Project",
        "confidence_threshold": "Confidence threshold",
        "anomalous_images": "Anomalous images",
        "undefined": "undefined",
        "block_artifact": "Block Artifact",
        "color_difference": "Color Difference",
        "water_mask": "Water Mask",
        "line_artifact": "Line Artifact",
        "confidence": "Confidence",
    },
    "no": _norwegian,
    "nb": _norwegian,
    "nn": _norwegian
}

_classified_no = {**_norwegian, "title": "Klassifisert avviksrapport",
                  "num_images": "Antall avvikende bilder"}

classified_translations = {
    "en": {**common_translations["en"], "title": "Classified Anomaly Report",
           "num_images": "Number of anomalous images"},
    "no": _classified_no,
    "nb": _classified_no,
    "nn": _classified_no
}

_unclassified_no = {**_norwegian, "title": "Uklassifisert avviksrapport",
                    "num_images": "Antall analyserte bilder"}

unclassified_translations = {
    "en": {**common_translations["en"], "title": "Unclassified Anomaly Report",
           "num_images": "Number of images analysed"},
    "no": _unclassified_no,
    "nb": _unclassified_no,
    "nn": _unclassified_no
}
