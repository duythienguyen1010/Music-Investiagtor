import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

artist_name = []
track_name = []
popularity = []
track_id = []

# Search
for i in range(0, 1000, 50):
    track_results = sp.search(q='year:2021', type='track', limit=50, offset=i)
    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])

avg_popularity = sum(popularity)/1000