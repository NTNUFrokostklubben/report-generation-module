common_translations = {
    "en": {
        "project": "project",
        "confidence_threshold": "Confidence threshold",
        "anomalous_images": "Anomalous images",
        "block_artifact": "Block Artifact",
        "color_difference": "Color Difference",
        "water_mask": "Water Mask",
        "line_artifact": "Line Artifact",
        "confidence": "confidence",
    },
    "no": {
        "project": "prosjekt",
        "confidence_threshold": "Konfiansegrense",
        "anomalous_images": "Avvikende bilder",
        "block_artifact": "Blokkartefakt",
        "color_difference": "Fargeforskjell",
        "water_mask": "Vannmaske",
        "line_artifact": "Linjeartefakt",
        "confidence": "konfianse",
    },
}

classified_translations = {
    "en": {**common_translations["en"], "title": "Classified Anomaly Report",
           "num_images": "Number of anomalous images"},
    "no": {**common_translations["no"], "title": "Klassifisert avviksrapport",
           "num_images": "Antall avvikende bilder"},
}

unclassified_translations = {
    "en": {**common_translations["en"], "title": "Unclassified Anomaly Report",
           "num_images": "Number of images analysed"},
    "no": {**common_translations["no"], "title": "Uklassifisert avviksrapport",
           "num_images": "Antall analyserte bilder"},
}