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

site_dropdown_list = []
site_dropdown_list.append({'label': 'All Sites', 'value': 'ALL'})
for site in spacex_df['Launch Site'].unique().tolist():    
    site_dropdown_list.append({'label': site, 'value': site})

marks_range = {}
marks_range[0] = '0 kg'
for i in range(1000, 11000, 10**3):
    marks_range[i] = '%s kg' % i

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                            options=site_dropdown_list,
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id = 'payload-slider',
                                                min = 0, 
                                                max = 10000, 
                                                step = 1000, 
                                                marks = marks_range,
                                                value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(df,
        names = 'Launch Site',
        title = 'Total Success Launches by Site')
    else:
        df = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(df,
        names = 'class',
        title = 'Total Success Launches for site %s' % entered_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def update_scattergraph(entered_site,payload_slider):
    if entered_site == 'ALL':
        low, high = payload_slider
        df = spacex_df
        mass = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mass], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)')
    else:
        low, high = payload_slider
        df  = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        mass = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            df[mass], x="Payload Mass (kg)", y="class",
            color="Booster Version",
            size='Payload Mass (kg)')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
