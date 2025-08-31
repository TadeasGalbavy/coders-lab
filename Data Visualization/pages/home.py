# pages/home.py
from dash import html, dcc
import dash
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/", name="Home")

df = pd.read_csv('project_1_python.csv')

# -------------------------------- 1. --------------------------------
df_top = (df.groupby('location')['population']
            .sum()
            .reset_index(name='population')
            .nlargest(n=10, columns='population'))

max_value = df_top['population'].max()
df_top['farba'] = df_top['population'].apply(
    lambda x: 'Najvyšší' if x == max_value else 'Ostatné'
)
fig_1 = px.bar(
    data_frame=df_top,
    x='location',
    y='population',
    text_auto=True,
    template='seaborn',
    title='First visualization',
    color='farba',
    color_discrete_map={'Ostatné': '#A3B18A', 'Najvyšší': '#E63946'},
    hover_data={'farba': False, 'population': True, 'location': True}
)
fig_1.update_layout(showlegend=False)
fig_1.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )

# -------------------------------- 2. --------------------------------
df_scatter = df[['location','population','life_expectancy']].dropna()

fig_2 = px.scatter(
    df_scatter,
    x='population',            
    y='life_expectancy',
    color='location',       
    hover_name='location',     
    template='seaborn',
    opacity=0.6,
    title='Population vs. life expectancy'
)
# logaritmická os X kvôli rozsahu populácie
fig_2.update_xaxes(type='log', title='Population (log scale)')
fig_2.update_yaxes(title='Life expectancy (years)')
fig_2.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )

# -------------------------------- 3. --------------------------------
countries = ['Czechia', 'Slovakia']
custom_colors = ['#8B0000', '#2E8B57']
df_filtered = df.loc[ df['location'].isin(countries) ].copy()
df_filtered['date'] = pd.to_datetime(df_filtered['date'])

fig_3 = px.line(
    df_filtered,
    x='date',
    y='new_cases',
    color='location',
    template='seaborn',
    title='Daily new COVID-19 cases distribution',
    color_discrete_sequence=custom_colors
)

fig_3.update_layout(
        plot_bgcolor='#292929',   # pozadie vnútri grafu
        paper_bgcolor='#292929',  # pozadie celého plátna
        font_color='#A3B18A',       # farba textov
    )

# -------------------------------- 4. --------------------------------
df_small = df.groupby(['iso_code', 'location'], as_index=False)['total_cases'].max()

fig_4 = px.choropleth(
    df_small,
    locations='iso_code',            
    color='total_cases',
    hover_name='location',
    color_continuous_scale=px.colors.diverging.Portland,
    title='Total COVID-19 cases by country',
    template='plotly_dark',
    labels={'iso_code': 'ISO', 'total_cases': 'total cases'},
    projection='natural earth',
    width=1200, height=700
    )

# -------------------------------- LAYOUT --------------------------------
layout = html.Div(
    children= [
        # grafy
        html.Div(
            children=[
                # graf 1
                html.Div(
                    children=[
                        dcc.Graph(figure=fig_1)
                    ],
                    style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                         'borderRadius': '10px',
                                         'marginTop': '10px'
                                        }
                ),
                html.Hr(),
                # graf 2
                html.Div(
                    children=[
                        dcc.Graph(figure=fig_2)
                    ],
                    style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                         'borderRadius': '10px',
                                         'marginTop': '10px'
                                        }
                ),
                html.Hr(),
                # graf 3
                html.Div(
                    children=[
                        dcc.Graph(figure=fig_3)
                    ],
                    style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                         'borderRadius': '10px',
                                         'marginTop': '10px'
                                        }
                ),
                html.Hr(),
                # graf 4
                html.Div(
                    children=[
                        dcc.Graph(figure=fig_4)
                    ],
                    style={'boxShadow': '0 4px 12px rgba(0, 0, 0, 0.3)',
                                         'borderRadius': '10px',
                                         'marginTop': '10px',
                                         'display': 'flex',
                                         'justifyContent': 'center',
                                        }
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
