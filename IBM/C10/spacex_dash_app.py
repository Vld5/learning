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

list_sites = spacex_df['Launch Site'].unique()
dropdown_opts = [{'label': 'All sites', 'value': 'ALL'}]
for site in list_sites:
    dropdown_opts.append({'label': site, 'value': site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=dropdown_opts,
                                             placeholder='All sites', value='ALL', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min = 0, max=10000, step=1000,
                                                marks={i: f'{i}' for i in range(0, 11000, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
#Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def pie_chart_func(site):
    if site not in list_sites:
        df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()

        title = 'Total Success Launches by Site'
        figure = px.pie(df, values='class', names='Launch Site', title=title)
        return figure
    else:
        df = spacex_df[spacex_df['Launch Site'] == site]['class'].value_counts().reset_index()
        title = f'Total Success Launches for {site}'
        names = df['class'].map(lambda x: 'Success' if x else 'Failure')
        figure = px.pie(df, values='count', names=names, title=title, color='class',
                        color_discrete_map={1: 'forestgreen', 0: 'crimson'})
        return figure
    return []




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def scatter_chart(site, payload):
    if site not in list_sites:
        title = 'Correlation between Payload and Success for all sites'
        df = spacex_df[ spacex_df['Payload Mass (kg)'].between(payload[0],payload[1]) ]
        figure = px.scatter(df, x='Payload Mass (kg)', y='class',
                             color='Booster Version Category', title=title)
        return figure
    else:
        df = spacex_df[ (spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])) &
                        (spacex_df['Launch Site'] == site) ]
        title = f'Correlation between Payload and Success for {site}'
        figure = px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return figure

    return []


# Run the app
if __name__ == '__main__':
    app.run_server()
