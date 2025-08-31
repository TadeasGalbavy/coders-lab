import pandas as pd
import plotly.express as px
import dash
import numpy as np
from dash import dcc, html, callback
from dash.dependencies import Input, Output

dash.register_page(__name__, path="/dash-1", name="Dashboard A")

df = pd.read_csv('project_1_python.csv')
df['date'] = pd.to_datetime(df['date'])
# -------------------------------- LAYOUT --------------------------------
layout = html.Div(
    children= [
        html.Div(
            children=[
                html.H1('COVID-19 Tracker')
            ]
        ),
        # grafy
        html.Div(
            children=[
                # graf 1
                html.P("Choose country:"),
                html.Div(
                    children=[
                        dcc.Dropdown(id='dropdown-1', options=df['location'].unique(), value='Slovakia', style={'width': '35%'}),
                        html.Div(
                            children=[
                                dcc.Graph(id='graph-1', style={'display': 'inline-block', 'width': '48%'}),
                                dcc.Graph(id='graph-2', style={'display': 'inline-block', 'width': '48%'})
                            ],
                            style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                                'borderRadius': '10px',
                                                'marginTop': '10px',
                                                'display': 'flex',
                                                'justifyContent': 'center'
                            }
                        )
                    ]
                )
            ]
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
    Output(component_id='graph-1', component_property='figure'),
    Input(component_id='dropdown-1', component_property='value')
)

def graph_1(country):
    
    df_graph_1 = df
    
    df_filtered = df_graph_1.loc[ df_graph_1['location'] == country ]
    
    fig = px.line(
        df_filtered,
        x='date',
        y='total_cases',
        template='seaborn',
        title=f'Cumulative number of positive cases in {country}',
        labels={'total_cases': 'Total cases'},
        color_discrete_sequence=['#A3B18A']
    )
    
    fig.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )
    return fig

@callback(
    Output(component_id='graph-2', component_property='figure'),
    Input(component_id='dropdown-1', component_property='value')
)

def graph_2(country):
    
    df_graph_2 = df
    
    df_filtered = df_graph_2.loc[ df_graph_2['location'] == country ]

    fig = px.line(
        df_filtered,
        x='date',
        y='total_deaths',
        template='seaborn',
        title=f'Cumulative number of deaths in {country}',
        labels={'total_deaths': 'Total deaths'},
        color_discrete_sequence=['#A3B18A']
    )
    
    fig.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )
    return fig