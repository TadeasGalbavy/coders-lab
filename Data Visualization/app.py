import dash
from dash import html, dcc, Input, Output

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, title='Final project')

header = html.Div(
    [
        html.Img(
            src='https://www.adobe.com/creativecloud/design/discover/media_1eeac4f414fef7a2538f45d131ecae95e859923d9.png?width=750&format=png&optimize=medium',
            style={'height': '60px'}
        ),
        html.H1('Final project', style={'margin': 0, 'color': '#A3B18A'})
    ],
    style={
        'display': 'flex',
        'gap': '5%',
        'justifyContent': 'center',
        'alignItems': 'center',
        'padding': '12px 0',
        'backgroundColor': '#1f1f1f'
    }
)

app.layout = html.Div(
    children=[
        dcc.Location(id='url'),
        header,
        html.Nav(id='navbar', className='navbar'),
        dash.page_container
    ],
    style={'backgroundColor': '#1b1b1b', 'minHeight': '100vh', 'color': '#eaeaea'})


@app.callback(
    Output(component_id='navbar', component_property='children'), 
    Input(component_id='url', component_property='pathname')
)

def render_nav(pathname):
    links = []

    for p in dash.page_registry.values():
        active = (p['relative_path'] == pathname)
        cls = 'nav-btn nav-btn--active' if active else 'nav-btn'
        links.append(dcc.Link(p['name'], href=p['relative_path'], className=cls))
    return links

if __name__ == '__main__':
    app.run(debug=True, port=8050)
