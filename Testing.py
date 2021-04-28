import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import analysis

# Spotipy Setup
cid = '3e7b0a3fcfe445a69eea02e4a4ce99b8'
secret = 'a761b0fa42734f5aa5a4182f425558c6'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#create the initial stargraph
fig = go.Figure(data=go.Scatterpolar(
  r=[0, 0, 0, 0],
  theta=['danceability', 'acousticness', 'energy', 'instrumentalness'],
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
    html.Hr(style={'color': '#7FDBFF'}),
    dcc.Graph(id='graph1', figure=fig),
    html.Br(),
    html.Div('*This is the conclusion*'),

])

@app.callback(
    Output('graph1', 'figure'),
    Input('my-input', 'value')
)
def update_output_div(input_value):
    taste, scale = analysis.generate_elements(input_value)
    return {'data': [go.Scatterpolar(r=scale, theta=taste, fill= 'toself')]}

if __name__ == '__main__':
    app.run_server(debug=True)