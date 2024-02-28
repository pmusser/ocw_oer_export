import unittest
from ocw_oer_export.config import API_URL
from ocw_oer_export.client import make_request


class APITestCase(unittest.TestCase):
    """Test suite for ensuring the MIT OpenCourseWare API response
    contains all necessary fields for OER template."""

    def test_api_fields(self):
        """
        Test that the API contains all the expected fields.

        Fields required: title, url, level, description, topics,
        instructors, semester, year, course_feature
        """
        page_size = 1
        response = make_request(API_URL, page_size)

        # Ensure the request was successful
        self.assertEqual(response.status_code, 200)

        api_data = response.json().get("results", [])

        # Assert that only one item is returned
        self.assertEqual(len(api_data), 1)

        course = api_data[0]
        course_runs = course["runs"][0]

        self.assertIn("title", course)
        self.assertIn("url", course)
        self.assertIn("level", course_runs)
        self.assertIn("description", course)
        self.assertIn("topics", course)
        self.assertIn("instructors", course_runs)
        self.assertIn("semester", course_runs)
        self.assertIn("year", course_runs)
        self.assertIn("course_feature", course)
