# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
# URL del archivo CSV
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"

spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
launch_sites = spacex_df['Launch Site'].unique()

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'}
                                        ] + [{'label': site, 'value': site} for site in launch_sites],
                                    value='ALL',
                                    placeholder="place holder here",
                                    searchable=True
                                ),
                                # ----
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,  # Minimum value
                                    max=10000,  # Maximum value
                                    step=1000,  # Step size (interval)
                                    marks={0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'},
                                    value=[min_payload, max_payload]  # Default value set to min and max payloads
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Filter the dataframe based on the selected site
    if entered_site == 'ALL':
        # If 'ALL' is selected, use the entire dataframe
        filtered_df = spacex_df[spacex_df['class'] == 1]  # Solo lanzamientos exitosos
        fig = px.pie(
            spacex_df, 
            names='Launch Site',  # Success or Failure (class column)
            title='Total Launch Success'
        )
    else:
        # If a specific site is selected, filter the dataframe
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        
        # Create a pie chart showing the success vs failure for the selected site
        fig = px.pie(
            filtered_df,
            names='class',  # Success or Failure (class column)
            title=f'Launch Success vs Failure for {entered_site}'
        )
    
    # Return the pie chart figure
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    # Filter dataframe based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if entered_site == 'ALL':
        # Plot all sites
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome for All Sites',
            labels={'class': 'Mission Outcome'}
        )
    else:
        # Filter data for the selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome for {entered_site}',
            labels={'class': 'Mission Outcome'}
        )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()