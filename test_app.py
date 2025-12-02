import unittest
import importlib
import sys
import pathlib
from unittest.mock import patch

# Ensure repo root on path for imports
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import app as backend_app


class AppEndpointTests(unittest.TestCase):
    def setUp(self):
        self.app = backend_app.app.test_client()

    @patch('backend.app.search_jobs')
    def test_search_jobs_endpoint_returns_jobs(self, mock_search):
        # Provide a fake job list
        mock_search.return_value = [
            {
                'title': 'Fake Job',
                'id': 'fake-1',
                'company': 'TestCo',
                'summary': 'Doing things',
                'location': 'Remote',
                'url': 'http://example.com',
                'requirements': ['Python'],
                'nice_to_have': []
            }
        ]

        resp = self.app.post('/search_jobs', json={'query': 'python'})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        first = data[0]
        self.assertIn('Job Name', first)
        self.assertEqual(first['Job Name'], 'Fake Job')

    @patch('backend.app.search_jobs')
    def test_search_jobs_endpoint_handles_missing_query(self, mock_search):
        # Missing query should return 400
        resp = self.app.post('/search_jobs', json={})
        self.assertEqual(resp.status_code, 400)


if __name__ == '__main__':
    unittest.main()
