import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import analysis
import base64

# Spotipy Setup
cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# imports picture and reads in base 64 code
image_filename = 'clef2.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# define features and initialize their value
init_taste = ['danceability', 'acousticness', 'energy', 'instrumentalness',
              'speechiness', 'liveness', 'valence']
init_scale = [0, 0, 0, 0, 0, 0, 0, 0]
# create the initial stargraph
fig = analysis.star_graph(init_taste, init_scale)

#create popular graph
popular_taste, popular_scale = analysis.generate_general_taste('US')
fig2 = analysis.star_graph(popular_taste, popular_scale)

# Run Dash
app = dash.Dash()
app.layout = html.Div(children=[
    html.P(children= html.Img(
        src='data:image/png;base64,{}'.format(encoded_image.decode())),
        className="header-emoji",
        style={"textAlign": 'center',}),
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

    # This part allow us to take input
    html.Div(["ENTER YOUR SPOTIFY ACCOUNT ID: ",
              dcc.Input(id='my-input', value='...text here...', type='text')]),

    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.Div("This graph represents your music taste"),
    dcc.Graph(id='graph1', figure=fig),
    html.Br(),

    # This part show different countries' tastes
    html.Div("This graph represents the music taste across different countries"),
    dcc.Graph(id='graph2', figure=fig2),
    html.Div('Please select a country', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-country',
        options=[
            {'label': 'United States of America', 'value': 'US'},
            {'label': 'Andorra', 'value': 'AD'},
            {'label': 'Australia', 'value': 'AU'},
            {'label': 'Brazil', 'value': 'BR'},
            {'label': 'Canada', 'value': 'CA'},
            {'label': 'Chile', 'value': 'CL'},
        ],
        value='USA'
    ),
    html.Div('*This is the conclusion*'),

])


@app.callback(
    Output('graph1', 'figure'),
    Input('my-input', 'value')
)
def update_graph1(input_value):
    taste, scale = analysis.generate_elements(input_value)
    fig = analysis.star_graph(taste, scale)
    return fig


@app.callback(
    Output('graph2', 'figure'),
    Input('select-country', 'value')
)
def update_graph2(country):
    taste, scale = analysis.generate_general_taste(country)
    fig = analysis.star_graph(taste, scale)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
