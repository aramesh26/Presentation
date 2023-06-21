# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    html.Br(),

    html.Div([
        html.Label('Select a Launch Site:'),
        dcc.Dropdown(
            id='site-dropdown',
            options=[
                {'label': 'All Sites', 'value': 'ALL'},
                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
            ],
            value='ALL',
            placeholder="Select a Launch Site",
            searchable=True
        ),
    ]),
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        value=[min_payload, max_payload],
        marks={str(payload): str(payload) for payload in range(min_payload, max_payload + 1, 2000)}
    ),

    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df
        title = 'Total Success Launches by Site'
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        title = f'Success vs. Failed Launches for Site {entered_site}'

    fig = px.pie(
        data_frame=data,
        names='class',
        title=title,
        hole=0.5,
        labels={'class': 'Launch Outcome'}
    )

    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=12,
        marker=dict(colors=['#55D605', '#FF0000'])
    )

    return fig


# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    if entered_site == 'ALL':
        data = spacex_df
        title = 'Payload and Launch Success Correlation'
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        title = f'Payload and Launch Success Correlation for Site {entered_site}'

    filtered_data = data[(data['Payload Mass (kg)'] >= payload_range[0]) & (data['Payload Mass (kg)'] <= payload_range[1])]

    fig = px.scatter(
        filtered_data,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title,
        labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()