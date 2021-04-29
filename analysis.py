import pandas as pd
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def generate_elements( x = ''):
    # Spotipy Setup
    cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
    secret = 'a761b0fa42734f5aa5a4182f425558c6'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Playlists
    playlists = sp.user_playlists(user=x, limit=10, offset=0)
    playlistIDs = []
    for i, t in enumerate(playlists['items']):
        playlistIDs.append(t['id'])

    # Tracks in First Playlist
    tracks = sp.playlist_items(playlist_id=playlistIDs[0], limit=100, offset=0)
    trackIDs = []
    total = tracks['total']
    for i, t in enumerate(tracks['items']):
        trackIDs.append(t['track']['id'])


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

    for i in range(0, len(trackIDs)):
        features = sp.audio_features(trackIDs[i])
        danceability.append(features[0]['danceability'])
        acousticness.append(features[0]['acousticness'])
        energy.append(features[0]['energy'])
        instrumentalness.append(features[0]['instrumentalness'])
        speechiness.append(features[0]['speechiness'])
        liveness.append(features[0]['liveness'])
        valence.append(features[0]['valence'])

    #Calculate average features
    sum_danc = sum(danceability) / total
    sum_acou = sum(acousticness) / total
    sum_ene = sum(energy) / total
    sum_inst = sum(instrumentalness) / total
    sum_speech = sum(speechiness) / total
    sum_live = sum(liveness) / total
    sum_val = sum(valence) / total

    print(sum_danc, sum_acou, sum_ene, sum_inst, sum_speech, sum_live, sum_val)
    taste = ['danceability', 'acousticness', 'energy', 'instrumentalness',
             'speechiness', 'liveness', 'valence']
    scale = [sum_danc, sum_acou, sum_ene, sum_inst, sum_speech, sum_val]
    return taste, scale

def star_graph(taste = [], scale = []):
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

#generate_elements('mh6sdur1otqgq0rhbllwa8k5f')