# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics',
                                style={'TextAlign':'center', 'color': '#503D36', 'font-size': 30}),
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number',
                                style={'font-size':30, 'height': '35px'})],
                                style={'font-size': 30}),
                                html.Br(),
                                html.Br(), 
                                html.Div([
                                        html.Div(dcc.Graph(id='carrier-plot')),
                                        html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
    
                                html.Div([
                                        html.Div(dcc.Graph(id='nas-plot')),
                                        html.Div(dcc.Graph(id='security-plot'))
                                ], style={'display': 'flex'}),
                                 html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
                                ])

def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    categories = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    avgs = list()
    for cat in categories:
        avgs.append(df.groupby(['Month','Reporting_Airline'])[cat].mean().reset_index())
    # avg_car = df.groupby(['Month','Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    # avg_weather = df.groupby(['Month','Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    # avg_NAS = df.groupby(['Month','Reporting_Airline'])['NASDelay'].mean().reset_index()
    # avg_sec = df.groupby(['Month','Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    # avg_late = df.groupby(['Month','Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avgs #avg_car, avg_weather, avg_NAS, avg_sec, avg_late


@app.callback([ Output(component_id='carrier-plot', component_property='figure'),
                Output(component_id='weather-plot', component_property='figure'),
                Output(component_id='nas-plot', component_property='figure'),
                Output(component_id='security-plot', component_property='figure'),
                Output(component_id='late-plot', component_property='figure')
                ],
                Input(component_id='input-year', component_property='value'))

def get_graph(entered_year):

    # avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(airline_data, entered_year)
    # avgs = [avg_car, avg_weather, avg_NAS, avg_sec, avg_late]
    avgs = compute_info(airline_data, entered_year)
    delay_types = ['carrier', 'weather', 'NAS', 'security', 'late']
    titles = [f'Average {x} delay time (minutes) by airline' for x in delay_types]
    x_labels = ['Month']*len(avgs)
    y_labels = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    colors = ['Reporting_Airline']*len(avgs)

    figs = list()
    for i, avg in enumerate(avgs):
        figs.append(px.line(avg, x=x_labels[i], y=y_labels[i], color=colors[i], title=titles[i]))
    

    return figs #[fig0, fig1, fig2, fig3, fig4]

# Run the app
if __name__ == '__main__':
    app.run_server()