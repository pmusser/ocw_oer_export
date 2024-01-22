import os
import unittest
from ocw_oer_export.create_csv import create_csv
from ocw_oer_export.data_handler import extract_data_from_file
from ocw_oer_export.utilities import delete_file


class CSVCreationTestCase(unittest.TestCase):
    """Test suite for verifying CSV creation from JSON data."""

    @classmethod
    def setUpClass(cls):
        """Class setup that runs once before all tests."""
        cls.test_dir = os.path.dirname(__file__)
        cls.expected_csv_path = os.path.join(cls.test_dir, "expected_courses.csv")
        cls.sample_json_path = os.path.join(cls.test_dir, "sample_courses.json")
        cls.generated_csv_path = os.path.join(cls.test_dir, "test_output.csv")

    def test_csv_creation_from_json(self):
        """Test the CSV generated from JSON matches the expected CSV content."""
        create_csv(
            source="json",
            input_file=self.sample_json_path,
            output_path=self.generated_csv_path,
        )
        generated_csv_data = extract_data_from_file(self.generated_csv_path)
        expected_csv_data = extract_data_from_file(self.expected_csv_path)

        self.assertEqual(
            generated_csv_data,
            expected_csv_data,
            "The generated CSV file does not match the expected CSV content.",
        )

    @classmethod
    def tearDownClass(cls):
        """Class teardown that runs once after all tests."""
        delete_file(cls.generated_csv_path)
