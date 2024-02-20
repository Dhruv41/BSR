import unittest
from Analysis import Analysis

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = Analysis("test_config.yml")

    def test_load_data(self):
        
        self.analysis.load_data()
        self.assertEqual(self.analysis.client_ID, 'test_client_id')
        self.assertEqual(self.analysis.client_key, 'test_client_secret')

    def test_get_access_token(self):
        self.analysis.access_token = None
        self.analysis.get_access_token()
        self.assertIsNotNone(self.analysis.access_token)

    def test_search_for_artist(self):
        result = self.analysis.search_for_artist('artist_name')
        self.assertIn('artist_id', result['artists']['items'][0]['id'])
        self.assertIn('artist_name', result['artists']['items'][0]['name'])

    def test_get_top_tracks(self):
        self.analysis.artist_id = ['artist_id']
        self.analysis.get_top_tracks()
        self.assertTrue(len(self.analysis.top_tracks_id) > 0)
        self.assertTrue(len(self.analysis.tracks_audio_valence) > 0)
        self.assertTrue(len(self.analysis.tracks_audio_danceability) > 0)
        self.assertTrue(len(self.analysis.tracks_audio_energy) > 0)


    def test_plot_data(self):
        fig = self.analysis.plot_data(save_path='test.png')
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()

