import unittest
from ocw_oer_export.utilities import text_cleanup


class DescriptionCleanupTests(unittest.TestCase):
    """Test suite for verifying the functionality of the description cleanup process."""

    def test_markdown_bold_removal(self):
        """Test that markdown bold syntax is removed."""
        sample_text = r"**2\. Adherence to guidelines (10% total grade):**"
        cleaned_text = text_cleanup(sample_text)
        self.assertEqual(cleaned_text, "2. Adherence to guidelines (10% total grade):")

    def test_markdown_header_removal(self):
        """Test that markdown header syntax is removed."""
        sample_text = "### Other Notes"
        cleaned_text = text_cleanup(sample_text)
        self.assertEqual(cleaned_text, "Other Notes")

    def test_custom_markup_removal(self):
        """Test that OCW Studio's custom markup is removed."""
        sample_text = (
            "{{< tableopen >}}{{< theadopen >}}{{< tropen >}}"
            "{{< thopen >}}Points{{< thclose >}}{{< thopen >}}"
            " Assessment{{< thclose >}}{{< trclose >}}{{< theadclose >}}"
            "{{< tableclose >}}"
        )
        cleaned_text = text_cleanup(sample_text)
        self.assertEqual(cleaned_text, "Points Assessment")

    def test_newline_normalization(self):
        """Test that extra newlines are removed and only single newlines remain."""

        sample_text = "CHINESE COURSES\n\n\n\nCOURSE SITES\n\n\nChinese I (Fall 2014)"
        cleaned_text = text_cleanup(sample_text)
        expected_description = "CHINESE COURSES\nCOURSE SITES\nChinese I (Fall 2014)"
        self.assertEqual(cleaned_text, expected_description)

    def test_empty_curly_brackets_removal(self):
        """Test the removal of content within curly brackets and subsequent empty lines."""
        sample_text = "CHINESE COURSES\n{{}}\n{{}}\nCOURSE SITES"
        cleaned_text = text_cleanup(sample_text)
        expected_description = "CHINESE COURSES\nCOURSE SITES"
        self.assertEqual(cleaned_text, expected_description)
