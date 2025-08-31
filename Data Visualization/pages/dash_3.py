import pandas as pd
import plotly.express as px
import dash
import numpy as np
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/dash-3", name="Dashboard C")


df_covid = pd.read_csv('project_1_python.csv')
df_covid['date'] = pd.to_datetime(df_covid['date'])


# -------------------------------- LAYOUT --------------------------------
layout = html.Div(
            children=[
                html.Div(
                    children=[
                    html.H1('COVID-19 Tracker')
                    ]
                ),                           
                html.P("Choose top x countries:"),
                html.Div(
                    children=[
                            dcc.Slider(5, 20, 5,
                        value=5,
                        id='my-slider',
                    )
                    ],
                    style={'width': '35%'}
                ),   
                html.Br(),
                html.Div(
                    children=[
                        dcc.Graph(id='first-graph', style={'display':'inline-block', 'width': '48%'}),
                        dcc.Graph(id='second-graph', style={'display':'inline-block', 'width': '48%'})
                    ],
                    style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                         'borderRadius': '10px',
                                         'marginTop': '10px',
                                         'display': 'flex',
                                         'justifyContent': 'center'
                                        }
                )
            ],
            style={
            'backgroundColor': "#292929",      # temná šedá
            'color': 'white',                  # text biely
            'fontFamily': 'Segoe UI, sans-serif',
            'padding': '20px',
            'color': '#A3B18A'
            }
        )

# -------------------------------- CALLBACKS --------------------------------
@callback(
    Output(component_id='first-graph', component_property='figure'),
    [Input(component_id='my-slider', component_property='value')]
)
def generate_vaccinations_graph(n):
    max_date = df_covid['date'].max()
    df = df_covid[df_covid['date'] == max_date].sort_values(by='total_vaccinations', ascending=False).head(n).fillna(0)
    
    max_value = df['total_vaccinations'].max()
    df['farba'] = df['total_vaccinations'].apply(
        lambda x: 'Najvyšší' if x == max_value else 'Ostatné')

    
    fig = px.bar(
        data_frame=df,
        x='location',
        y='total_vaccinations',
        title=f'Number of vaccinations',
        labels={'total_vaccinations': 'Total vaccinations'},
        text_auto=True,
        color='farba',
        color_discrete_map={'Ostatné': '#A3B18A', 'Najvyšší': '#E63946'},
        hover_data={'farba': False}
    )
    
    fig.update_layout(showlegend=False)
    fig.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )
    return fig

@callback(
    Output(component_id='second-graph', component_property='figure'),
    Input(component_id='my-slider', component_property='value')
)
def generate_vaccination_ratio_graph(n):
    max_date = df_covid['date'].max()
    df = df_covid[df_covid['date'] == max_date]
    df['vaccination_ratio'] = df['total_vaccinations'] / df['population']
    df = df.sort_values(by='vaccination_ratio', ascending=False).head(n).fillna(0)
    
    max_value = df['vaccination_ratio'].max()
    df['farba'] = df['vaccination_ratio'].apply(
        lambda x: 'Najvyšší' if x == max_value else 'Ostatné')
    
    fig = px.bar(
        data_frame=df,
        x='location',
        y='vaccination_ratio',
        title=f'Vaccination ratio',
        labels={'vaccination_ratio': 'Vaccination ratio'},
        text_auto=True,
        color='farba',
        color_discrete_map={'Ostatné': '#A3B18A', 'Najvyšší': '#E63946'},
        hover_data={'farba': False}
    )
    
    fig.update_layout(showlegend=False)
    fig.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )
    return fig