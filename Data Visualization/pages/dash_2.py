import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/dash-2", name="Dashboard B")

# --- data ---
df_covid = pd.read_csv('project_1_python.csv')
df_covid['date'] = pd.to_datetime(df_covid['date'], errors='coerce')

# posledný deň + istota, že máme súradnice a kontinent
df_latest = (df_covid.loc[df_covid['date'] == df_covid['date'].max()],
             )[0].copy()
df_latest = df_latest.dropna(subset=['latitude', 'longitude', 'continent'])
df_latest['latitude']  = pd.to_numeric(df_latest['latitude'], errors='coerce')
df_latest['longitude'] = pd.to_numeric(df_latest['longitude'], errors='coerce')
df_latest = df_latest.dropna(subset=['latitude','longitude'])

metric_dict = {
    'total_cases': 'Total cases',
    'total_deaths': 'Total deaths',
    'total_tests': 'Total tests',
    'total_vaccinations': 'Total vaccinations',
    'people_fully_vaccinated': 'Number of fully vaccinated people'
}

continents = sorted(df_latest['continent'].unique().tolist())

# --- app ---

layout = html.Div(
            children=[
                html.H1('COVID-19 Tracker'),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.P("Choose continent:"),
                                dcc.Dropdown(
                                    id='continent',
                                    options=[{'label': c, 'value': c} for c in continents],
                                    value=continents[0],
                                    clearable=False,
                                )
                            ],
                            style={'width': '45%'}
                        ),
                        html.Div(
                            children=[
                                html.P("Choose metric:"),
                                dcc.Dropdown(
                                    id='metric',
                                    options=[{'label': v, 'value': k} for k, v in metric_dict.items()],
                                    value='total_cases',
                                    clearable=False,
                                )
                            ],
                            style={'width': '45%'}
                        )
                    ],
                    style={'display': 'flex', 
                           'justifyContent': 'left',
                           'gap': '1%',
                           'width': '35%',
                           'margin': '0px'
                           }
                ),
                html.Br(),
                dcc.Graph(id="map", style={'height': '80vh', 'width': '100%'})
        ],
        style={
        'backgroundColor': "#292929",      # temná šedá
        'color': 'white',                  # text biely
        'fontFamily': 'Segoe UI, sans-serif',
        'padding': '20px',
        'color': '#A3B18A'
        }
    )

@callback(
    Output('map', 'figure'),
    [Input('continent', 'value'),
     Input('metric', 'value')]
)
def generate_covid_map(continent, metric):
    d = df_latest[df_latest['continent'] == continent].copy()
    # metrika numerická, NaN -> 0 len tu
    d[metric] = pd.to_numeric(d[metric], errors='coerce').fillna(0)

    # DEBUG do konzoly – uvidíš v terminali, koľko bodov kreslíme
    print(f"[map] continent={continent} metric={metric} rows={len(d)}")

    # ŽIADNE tiles: scatter_geo funguje offline, vždy niečo uvidíš
    fig = px.scatter_geo(
        d,
        lat='latitude', lon='longitude',
        color='continent',
        size=metric, size_max=28,
        hover_name='location',
        hover_data={metric:':,', 'population':':,', 'continent': True},
        projection='natural earth',   # celý svet
        title=f'COVID-19 — {metric_dict[metric]} in {continent}',
        color_discrete_sequence=['#A3B18A'],
        template='plotly_dark'
    )
    fig.update_traces(marker_sizemin=5, opacity=0.9)
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=0))
    return fig
