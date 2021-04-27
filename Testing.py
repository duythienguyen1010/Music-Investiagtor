import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotipy Setup
cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Run Dash
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Music Investigator',
            style={'textAlign': 'center',
                   'color': '#A01FF2'
                   }
            ),
    html.Div('Web Dashboard for Data Visualization using Python',
             style={'textAlign': 'center'}),
    html.Div('Spotify User Information',
             style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),

#This part allow us to take input
    html.Div(["ENTER YOUR SPOTIFY ACCOUNT ID: ",
              dcc.Input(id='my-input', value='...text here...', type='text')]),
    html.Br(),
    html.Div(id='my-output'),

    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent your taste in music'),
    dcc.Graph(id='graph1'),
    html.Br(),
    html.Div('*This is the conclusion*'),

])

@app.callback(
    Output('graph1', 'figure'),
    Input('my-input', 'value')
)
def update_output_div(input_value):
    # Playlists
    playlists = sp.user_playlists(user=input_value, limit=10, offset=0)
    playlistIDs = []
    for i, t in enumerate(playlists['items']):
        playlistIDs.append(t['id'])

    # Tracks in First Playlist
    tracks = sp.playlist_items(playlist_id=playlistIDs[0], limit=100, offset=0)
    trackIDs = []
    for i, t in enumerate(tracks['items']):
        trackIDs.append(t['track']['id'])

    # Features
    danceability = []
    acousticness = []
    energy = []
    instrumentalness = []

    for i in range(0, len(trackIDs)):
        features = sp.audio_features(trackIDs[i])
        danceability.append(features[0]['danceability'])
        acousticness.append(features[0]['acousticness'])
        energy.append(features[0]['energy'])
        instrumentalness.append(features[0]['instrumentalness'])

    sum_danc = sum(danceability) / 100
    sum_acou = sum(acousticness) / 100
    sum_ene = sum(energy) / 100
    sum_inst = sum(instrumentalness) / 100

    taste = ['danceability', 'acousticness', 'energy', 'instrumentalness']
    scale = [sum_danc, sum_acou, sum_ene, sum_inst]
    return {'data': [go.Bar(x=taste, y=scale)], 'layout': go.Layout(title='This chart represents your taste in music',
                                                            xaxis={'title': 'Audio Feature'}, yaxis={'title': 'Scale'})
              }


if __name__ == '__main__':
    app.run_server()