import os
import sys
import pathlib
import importlib
import unittest
from unittest.mock import patch, MagicMock

# Ensure the project root is on sys.path so `import backend...` works when
# tests are executed from the `backend/` directory.
ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class TestSearchJobs(unittest.TestCase):
    def setUp(self):
        # Ensure we import fresh each test after manipulating env
        if 'backend.job_search' in importlib.sys.modules:
            importlib.reload(importlib.import_module('backend.job_search'))

    @patch('backend.job_search.requests.get')
    def test_search_jobs_with_api_key_calls_api(self, mock_get):
        # Prepare fake response
        fake_resp = MagicMock()
        fake_resp.status_code = 200
        fake_resp.json.return_value = {
            'data': [
                {
                    'job_title': 'Test Job',
                    'job_id': '123',
                    'employer_name': 'ACME',
                    'job_description': 'Do stuff',
                    'job_city': 'Remote',
                    'job_apply_link': 'http://apply',
                    'job_highlights': {
                        'Qualifications': ['Python', 'Testing'],
                        'Responsibilities': ['Build tests']
                    }
                }
            ]
        }
        mock_get.return_value = fake_resp

        # Ensure key present for this test
        os.environ['RAPIDAPI_KEY'] = 'FAKEKEY'
        importlib.reload(importlib.import_module('backend.job_search'))
        from backend.job_search import search_jobs

        res = search_jobs('test')
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['title'], 'Test Job')

    def test_search_jobs_without_key_returns_empty(self):
        # Remove key
        if 'RAPIDAPI_KEY' in os.environ:
            del os.environ['RAPIDAPI_KEY']
        # reload module so it picks up env change
        importlib.reload(importlib.import_module('backend.job_search'))
        from backend.job_search import search_jobs

        res = search_jobs('anything')
        self.assertEqual(res, [])


if __name__ == '__main__':
    unittest.main()
