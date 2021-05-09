import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import analysis
import base64
import conclusions
import time

external_stylesheet = [
    {
        "href": 'assets/typography.css',
        "rel": 'stylesheet'
    }
]

# Open image and encode in base 64
image_filename = 'clef2.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Define features and initialize their values
init_taste = ['Danceability', 'Acousticness', 'Energy', 'Instrumentalness',
              'Speechiness', 'Liveness', 'Valence']
init_scale = [0, 0, 0, 0, 0, 0, 0]

# Create the initial user star graph
fig = analysis.star_graph(init_taste, init_scale)

# Create general taste star graph
popular_taste, popular_scale, popular_stdevs = analysis.generate_general_taste('US')
fig2 = analysis.star_graph(popular_taste, popular_scale)

# Initialize the conclusion
conclusion_string = ''

# Set background and text colors
colors = {
    'background': '#333333',
    'text': '#7FDBFF'
}

# Run Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheet)
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Br(),
                html.P(children=html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image.decode())),
                    className="header-emoji",
                    style={"textAlign": 'center',
                           'backgroundColor': colors['background'],
                           'height': '54px'}),
                html.H1(children='Music Investigator',
                        style={'textAlign': 'center',
                               'color': '#A01FF2',
                               'backgroundColor': colors['background']
                               },
                        ),
                html.Div('Web Dashboard for Data Visualization using Python',
                         style={'textAlign': 'center',
                                'color': '#FFFFFF',
                                'backgroundColor': colors['background']}),
                html.Div('Spotify User Information',
                         style={'textAlign': 'center',
                                'color': '#FFFFFF',
                                'backgroundColor': colors['background']}),
                html.Br(),
                html.Br(),

                # Allow dashboard to take user input
                html.Div(["Enter your Spotify Account ID: ",
                          dcc.Input(id='my-input', value='', type='text')],
                         style={'margin-bottom': '24px',
                                'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                                'color': '#FFFFFF',
                                'textAlign': ''}),

                # This part display loading while taking in input
                dcc.Loading(
                    id='loading',
                    type='default',
                    children=html.Div(html.Div(id='my-input)'))
                )
            ],
            style={'height': '250px',
                   'backgroundColor': colors['background']}
        ),
        html.Br(),
        html.Hr(style={'color': '#7FDBFF'}),
        dcc.Markdown('''
                # Your Music Taste: '''),
        dcc.Graph(id='graph1', figure=fig,
                  style={'margin-bottom': '24px',
                         'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                         'color': '#FFFFFF',
                         'width': '49%',
                         'display': 'inline-block'}),
        dcc.Markdown('''
            * __Danceability__ describes how suitable a playlist is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
            * __Acousticness__ is a measure from 0.0 to 1.0 of whether the playlist is acoustic.
            * __Energy__ is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic playlists feel fast, loud, and noisy.
            * __Instrumentalness__ predicts whether a playlist contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the playlist contains no vocal content.
            * __Speechiness__ detects the presence of spoken words in a playlist. The more exclusively speech-like the recordings (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value.
            * __Valence__ is a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a playlist. Playlists with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
            '''),
        dcc.Markdown('''
        ### Conclusion: '''),
        html.Div(id='my-output',
                 style={'margin-bottom': '24px',
                        'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)'
                        }),
        html.Br(),

        # This part show different countries' tastes
        dcc.Markdown('''
        # Popular Music Taste In Various Countries: '''),
        dcc.Graph(id='graph2', figure=fig2),
        html.Br(),
        html.Div('Select a Country',
                 style={'margin': '10px',
                        'margin-bottom': '24px',
                        'box-shadow': '0 4px 6px 0 rgba(0, 0, 0, 0.18)',
                        }),
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
            value='US'
        ),
    ])


@app.callback(
    Output('graph1', 'figure'),
    Input('my-input', 'value')
)
def update_graph1(input_value):
    if input_value == '':
        return analysis.star_graph(init_taste, init_scale)
    taste, scale, stdevs = analysis.generate_elements(input_value)
    fig = analysis.star_graph(taste, scale)
    return fig


@app.callback(
    Output('my-output', 'children'),
    Input('my-input', 'value')
)
def update_conclusion(input_value):
    if input_value == '':
        return 'Make sure your playlist(s) are public in your spotify account'
    global conclusion_string
    taste, scale, stdevs = analysis.generate_elements(input_value)
    conclusion_string = conclusions.generate_conclusion(taste, scale, stdevs)
    return conclusion_string


@app.callback(
    Output('loading', 'children'),
    Input('my-input', 'value'))
def input_triggers_spinner(value):
    if value != '':
        time.sleep(13)


@app.callback(
    Output('graph2', 'figure'),
    Input('select-country', 'value')
)
def update_graph2(country):
    taste, scale, stdevs = analysis.generate_general_taste(country)
    fig = analysis.star_graph(taste, scale)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
