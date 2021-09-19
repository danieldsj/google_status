import unittest
import runpy
import google_status

class TestCase(unittest.TestCase):
    def test_regions(self):
        self.assertIn("asia-east1", google_status.known_regions)

    def test_zones(self):
        self.assertIn("asia-east1-a", google_status.known_zones)

    def test_get_incident_data(self):
        google_status.get_incident_data()
        with self.assertRaises(Exception) as context:
            google_status.get_incident_data(url="http://www.google.com")

    def test_get_region_from_zone(self):
        self.assertEqual(google_status.get_region_from_zone('asia-east1-a'), 'asia-east1')
        self.assertEqual(google_status.get_region_from_zone('pinapple'), None)

    def test_get_regions(self):
        self.assertEqual(google_status.get_regions('Blah asia-east1-a Blah'), ['asia-east1'])

    def test_get_zones(self):
        self.assertEqual(google_status.get_zones('Blah asia-east1-a Blah'), ['asia-east1-a'])

    def test_get_implied_zones(self):
        self.assertIn('asia-east1-a', google_status.get_implied_zones('Blah asia-east1 Blah'))
        self.assertIsInstance(list(google_status.get_implied_zones('Blah asia-east1 Blah')), list)

    def test_main_function(self):
        runpy.run_module("google_status")

if __name__ == '__main__':
    unittest.main()
