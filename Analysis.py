import yaml
import requests
import base64
import logging
from typing import Any, Dict
import matplotlib.pyplot as plt
import argparse

class Analysis():
    """
        Initialize Analysis object.

        Parameters:
            analysis_config (str): Path to the analysis configuration file.
    """
    def __init__(self, analysis_config:str):
        self.analysis_config = analysis_config
        self.load_config()
        self.setup_logging()

    def setup_logging(self):
        """
        Setup logging configuration.
        """
        logging.basicConfig(level=logging.INFO)

    def load_config(self):
        """
        Load configuration files.
        """


        try:
            config_files = ['Configs/user_config.yml', 'Configs/job_file.yml', 'Configs/system_config.yml']
            config = {}
            for i in config_files:
                with open(i, 'r') as file:
                   data = yaml.safe_load(file)
                config.update(data)
        except FileNotFoundError:
            logging.error("User configuration file not found.")
            exit(1)
        except Exception as e:
            logging.error(f"Error loading user configuration: {e}")
            exit(1)

        self.client_ID = data['Client_id']
        self.client_key = data['Client_secret']

    def get_access_token(self):
        """
            Retrieve access token.
        """
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = {
            'Authorization': f'Basic {base64.b64encode((self.client_ID + ":" + self.client_key).encode()).decode()}'
        }
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_ID,
            'client_key': self.client_key
        }
        auth_response = requests.post(auth_url, data=auth_data, headers=auth_header)
        auth_response_data = auth_response.json()
        self.access_token = auth_response_data['access_token']

    def get_auth_header(self):
        """
        Get authorization header.
        """
        return {"Authorization": "Bearer " + self.access_token}

    def search_for_artist(self, artist_name):
        """
        Search for an artist.
        """
        url = 'https://api.spotify.com/v1/search'
        headers = self.get_auth_header()
        query = f"?q={artist_name}&type=artist&offset=0&limit=20"
        results = requests.get(url + query, headers=headers)
        return results

    def load_data(self):
        """
        Load data for configured artists.
        """
        self.get_access_token()
        self.artist_id = []
        self.artist_name = []
        for i in self.config['Artists']:
            artist = self.search_for_artist(i)
            self.artist_id.append(artist.json()['artists']['items'][0]['id'])
            self.artist_name.append(artist.json()['artists']['items'][0]['name'])

    def get_top_tracks(self):
        """
        Retrieve top tracks for configured artists.
        """
        self.top_tracks = []
        self.top_tracks_id = []
        self.top_tracks_release_date = []
        self.top_tracks_artist_id = []
        self.top_tracks_album_name = []
        self.top_tracks_artist_album_id = []
        self.top_tracks_artist_popularity = []
        self.tracks_audio_valence = []
        self.tracks_audio_danceability = []
        self.tracks_audio_energy = []

        for artist_id in self.artist_id:
            URL = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
            headers = self.get_auth_header()
            result = requests.get(URL, headers=headers, params={'include_groups': 'album', 'limit': 50})
            end_results = result.json()['tracks']
            for track in end_results:
                self.top_tracks.append(track['name'])
                self.top_tracks_release_date.append(track['album']['release_date'])
                self.top_tracks_id.append(track['id'])
                self.top_tracks_artist_id.append(track['artists'][0]['id'])
                self.top_tracks_album_name.append(track['album']['name'])
                self.top_tracks_artist_album_id.append(track['album']['id'])
                self.top_tracks_artist_popularity.append(track['popularity'])

                audio_features = self.get_audio_features(track['id'])
                self.tracks_audio_valence.append(audio_features.get('valence'))
                self.tracks_audio_danceability.append(audio_features.get('danceability'))
                self.tracks_audio_energy.append(audio_features.get('energy'))

    def get_audio_features(self, track_id):
        """
            Retrieve audio features for a track.
        """
        URL = f'https://api.spotify.com/v1/audio-features/{track_id}'
        headers = self.get_auth_header()
        result = requests.get(URL, headers=headers)
        return result.json()

    def compute_analysis(self) -> Dict[str, Any]:
        """ Compute analysis metrics."""
        analysis_output = {
            'mean_valence': self.df_tracks_data['audio_valence'].mean(),
            'max_danceability': self.df_tracks_data['audio_danceability'].max(),
            # Add more analysis metrics as needed
        }
        return analysis_output

    def notify_done(self, message: str) -> None:
        """Notify completion"""
        print(f"Notification: {message}")

    def plot_data(self, save_path: str = None) -> plt.Figure:
        """Plot data"""
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(self.df_tracks_data['audio_danceability'], self.df_tracks_data['audio_valence'], alpha=0.5)
        ax.set_title('Valence vs Danceability')
        ax.set_xlabel('Danceability')
        ax.set_ylabel('Valence')
        if save_path:
            plt.savefig(save_path.png)
        return fig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='To find co-relation between the top tracks.')
    parser.add_argument('analysis_config', type=str, help='Path to the analysis configuration file')

    args = parser.parse_args()
    analysis_obj = Analysis(args.analysis_config)
    analysis_obj.load_data()
    analysis_obj.get_top_tracks()
    analysis_obj.plot_data()
