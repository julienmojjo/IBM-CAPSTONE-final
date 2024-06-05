# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"-O "C:/Users/julie/Documents/Perso/Python/spacex_dash_app.py"
# wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv" -O "C:/Users/julie/Documents/Perso/Python/spacex_launch_dash.csv"   
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("C:/Users/julie/Documents/Perso/Python/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),  
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             value="ALL",
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                                 ],
                                             placeholder='Select a report type',
                                             style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
                                            ),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2 Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
     )

def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df
        group_df = pd.DataFrame(filtered_df.groupby(['class','Launch Site'])["class"].sum().reset_index(name='sum'))
        fig = px.pie(group_df, values='sum', names='Launch Site', title="Total Success Launches By Site")
        fig.update_layout(transition_duration=50)
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==selected_site]
        group_df = pd.DataFrame(filtered_df.groupby(['class','Launch Site'])["class"].count().reset_index(name='count'))
        fig = px.pie(group_df, values='count', names='class', title=f"Launches Outcomes of the Site {selected_site}")
        fig.update_layout(transition_duration=50)
        return fig

# TASK 4 Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
     )
def get_pie_chart_2(selected_site,payload_range):
    low, high = payload_range
    if selected_site == 'ALL':
        filtered_df2 = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        fig2 = px.scatter(filtered_df2, x='Payload Mass (kg)',y='class', color='Launch Site', title="Outcomes depending on payload")
        fig2.update_layout(transition_duration=50)
        return fig2
    else:
        filtered_df2 = spacex_df[(spacex_df['Launch Site']==selected_site) & (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]
        fig2 = px.scatter(filtered_df2, x='Payload Mass (kg)',y='class', color='Booster Version', title=f"Launches Outcomes of the Site {selected_site}")
        fig2.update_layout(transition_duration=50)
        return fig2



# Run the app
if __name__ == '__main__':
    app.run_server()
