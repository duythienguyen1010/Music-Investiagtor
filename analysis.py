import pandas as pd
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import datetime
import statistics

# Spotipy Setup
cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def generate_elements(user=''):

    playlists = sp.user_playlists(user=user)
    playlist_ids = []
    for i in playlists['items']:
        playlist_ids.append(i['id'])
    track_ids = []
    for i in playlist_ids:
        results = sp.playlist_items(playlist_id=i)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        for j in tracks:
            track_ids.append(j['track']['id'])

    taste, scale, stdevs = calculate_from_track_ids(track_ids)
    return taste, scale, stdevs


def generate_general_taste(country=''):

    # Generate timestamp
    ct = datetime.datetime.utcnow().isoformat()

    playlists = sp.featured_playlists(country=country, timestamp=ct, limit=5)
    playlist_ids = []
    for i in playlists['playlists']['items']:
        playlist_ids.append(i['id'])
    track_ids = []
    for i in playlist_ids:
        results = sp.playlist_items(playlist_id=i, limit=20)
        tracks = results['items']
        for j in tracks:
            track_ids.append(j['track']['id'])

    taste, scale, stdevs = calculate_from_track_ids(track_ids)
    return taste, scale, stdevs


def star_graph(taste=[], scale=[]):

    fig = go.Figure(data=go.Scatterpolar(
        r=scale,
        theta=taste,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False
            ),
        ),
        showlegend=True
    )
    return fig


def calculate_from_track_ids(track_ids):

    # Features
    danceability = []
    acousticness = []
    energy = []
    instrumentalness = []
    loudness = []
    speechiness = []
    liveness = []
    valence = []
    tempo = []

    for i in track_ids:
        features = sp.audio_features(i)
        if features != [None]:
            danceability.append(features[0]['danceability'])
            acousticness.append(features[0]['acousticness'])
            energy.append(features[0]['energy'])
            instrumentalness.append(features[0]['instrumentalness'])
            loudness.append(features[0]['loudness'])
            speechiness.append(features[0]['speechiness'])
            liveness.append(features[0]['liveness'])
            valence.append(features[0]['valence'])
            tempo.append(features[0]['tempo'])

    # Calculate average features
    avg_danc = statistics.mean(danceability)
    avg_acou = statistics.mean(acousticness)
    avg_ene = statistics.mean(energy)
    avg_inst = statistics.mean(instrumentalness)
    avg_speech = statistics.mean(speechiness)
    avg_live = statistics.mean(liveness)
    avg_val = statistics.mean(valence)

    # Calculate standard deviation of features
    stdev_danc = statistics.stdev(danceability)
    stdev_acou = statistics.stdev(acousticness)
    stdev_ene = statistics.stdev(energy)
    stdev_inst = statistics.stdev(instrumentalness)
    stdev_speech = statistics.stdev(speechiness)
    stdev_live = statistics.stdev(liveness)
    stdev_val = statistics.stdev(valence)

    taste = ['danceability', 'acousticness', 'energy', 'instrumentalness',
             'speechiness', 'liveness', 'valence']
    scale = [avg_danc, avg_acou, avg_ene, avg_inst, avg_speech, avg_live, avg_val]
    stdevs = [stdev_danc, stdev_acou, stdev_ene, stdev_inst, stdev_speech, stdev_live, stdev_val]
    return taste, scale, stdevs
