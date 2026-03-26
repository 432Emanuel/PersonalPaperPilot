"""
Rule-based document classifier.
"""



class DocumentClassifier:
    """Classifies documents into categories based on keyword matching."""

    # Category keywords (case-insensitive matching)
    KEYWORDS = {
        "Jobcenter": [
            "jobcenter", "bürgergeld", "bedarfsgemeinschaft",
            "bewilligungszeitraum", "leistungsbescheid", "kundennummer", "bg-nummer"
        ],
        "Wohnen/Nebenkosten": [
            "heizkosten", "nebenkosten", "betriebskosten",
            "warmwasser", "kaltwasser", "abwasser", "hausgeld", "heizung"
        ],
        "Wasser": [
            "wasserrechnung", "wasserversorgung", "trinkwasser",
            "abwasserzweckverband", "wasserzähler", "verbrauchsabrechnung wasser", "schmutzwasser"
        ],
        "Schornsteinfeger": [
            "schornsteinfeger", "feuerstätte", "kehrung",
            "emissionsmessung", "feuerstättenschau", "abgasanlage"
        ],
        "Versicherung": [
            "versicherung", "police", "versicherungsnummer",
            "beitrag", "haftpflicht", "gebäudeversicherung"
        ],
        "Rechnung": [
            "rechnung", "gesamtbetrag", "zahlbar bis",
            "brutto", "netto", "betrag", "rechnung nr", "rechnungsnummer"
        ],
    }

    DEFAULT_CATEGORY = "Sonstiges"

    @classmethod
    def classify(cls, text: str) -> str:
        """
        Classify document based on extracted text using keyword scoring.

        Args:
            text: OCR-extracted text from document

        Returns:
            Category name as string
        """
        if not text:
            return cls.DEFAULT_CATEGORY

        text_lower = text.lower()

        # Score each category by counting keyword matches
        scores = {}
        for category, keywords in cls.KEYWORDS.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            if score > 0:
                scores[category] = score

        # Return category with highest score, or default if no matches
        if not scores:
            return cls.DEFAULT_CATEGORY

        # Get category with maximum score
        return max(scores.items(), key=lambda x: x[1])[0]
