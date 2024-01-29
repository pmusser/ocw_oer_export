import unittest
from ocw_oer_export.utilities import normalize_keywords


class KeywordsNormalizationTests(unittest.TestCase):
    """Test suite for verifying the correct normalization of keywords."""

    def test_formatting_of_keywords(self):
        """
        Test that formatting, including apostrophes, capitalization,
        and spacing, is handled correctly.
        """
        sample_text = "TCP's and UDPs,UDP,U.S.A,RNA,DNA, chemical industry"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords, "TCP's and UDPs|UDP|U.S.A|RNA|DNA|Chemical Industry"
        )

    def test_single_commas_keywords(self):
        """Test that keywords separated using single commas are normalized correctly."""
        sample_text = "novel, short story, the city in literature,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_double_commas_keywords(self):
        """Test that keywords separated using double commas are normalized correctly."""
        sample_text = "novel,, short story,, the city in literature,,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_single_newlines_keywords(self):
        """Test that keywords separated using single newlines are normalized correctly."""
        sample_text = "novel\nshort story\nthe city in literature\nnarrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_double_newlines_keywords(self):
        """Test that keywords separated using double newlines are normalized correctly."""
        sample_text = (
            "novel\n\nshort story\n\nthe city in literature\n\nnarrative voice"
        )
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )

    def test_semicolons_keywords(self):
        """Test that keywords separated using semicolons are normalized correctly."""
        sample_text = "novel; short story, the city in literature,narrative voice"
        normalized_keywords = normalize_keywords(sample_text)
        self.assertEqual(
            normalized_keywords,
            "Novel|Short Story|The City in Literature|Narrative Voice",
        )
