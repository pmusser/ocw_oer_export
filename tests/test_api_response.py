import unittest
from ocw_oer_export.constants import API_URL
from ocw_oer_export.client import make_request


class APITestCase(unittest.TestCase):
    """Test suite for ensuring the MIT OpenCourseWare API response
    contains all necessary fields for OER template."""

    def test_api_fields(self):
        """Test that we have all the needed fields in the API.
        Fields required: title, url, description, topics, instructors, course_feature"""
        page_size = 1
        response = make_request(API_URL, page_size)

        # Ensure the request was successful
        self.assertEqual(response.status_code, 200)

        api_data = response.json().get("results", [])

        # Assert that only one item is returned
        self.assertEqual(len(api_data), 1)

        item = api_data[0]
        self.assertIn("title", item)
        self.assertIn("url", item)
        self.assertIn("description", item)
        self.assertIn("topics", item)
        self.assertIn("resource_content_tags", item)
        self.assertIn("instructors", item["runs"][0])
