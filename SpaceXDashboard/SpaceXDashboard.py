# Import required libraries
import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("/workspaces/codespaces-blank/SpaceXDashboard/spacex_web_scraped.csv")
max_payload = spacex_df['Payload mass'].max()
min_payload = spacex_df['Payload mass'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[{'label':'All Sites', 'value':'ALL'},
                                                                          {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'},
                                                                          {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'},
                                                                          {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                                          {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'}],
                                                                          value = 'ALL',
                                                                          placeholder = "place holder here",
                                                                          searchable = True),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 17000, step = 1000, value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.P("Payload Scatter Chart"),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                html.P("Booster Categories Class 1 Frequency Chart"),
                                html.Div(dcc.Graph(id='success-booster-bar-chart')),

                                html.P("Booster Categories Success Rate"),
                                html.Div(dcc.Graph(id='success-booster-probbar-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch site']==entered_site]
    dataF = pd.DataFrame(spacex_df.groupby('Launch site')['Class'].mean().reset_index())
    if entered_site == 'ALL':
        fig = px.pie(dataF, values='Class', 
        names='Launch site', 
        title='Pie Chart of All sites')
        return fig
    else:
        outcome = []
        for row in filtered_df.index:
            if filtered_df.loc[row, 'Class'] == 1:
                outcome.append('Success')
            else:
                outcome.append('Failed')
        filtered_df['Outcome'] = outcome
        filtered_df['freq_count'] = filtered_df.groupby('Outcome')['Outcome'].transform('count')
        dataE = pd.DataFrame(filtered_df.groupby('Outcome')['freq_count'].mean().reset_index())
        fig = px.pie(dataE, values='freq_count', 
        names='Outcome', 
        title='Pie Chart of selected site', color = 'Outcome', color_discrete_map={'Success':'blue', 'Failed':'red'})
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter(entered_site, value):
    df = spacex_df[(spacex_df['Payload mass'] <= max(value)) & (spacex_df['Payload mass'] >= min(value))]
    if entered_site == 'ALL':
        fig1 = px.scatter(df, x='Payload mass', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig1
    else:
        filtered_df = df[spacex_df['Launch site']==entered_site]
        fig1 = px.scatter(filtered_df, x='Payload mass', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig1
    
@app.callback(Output(component_id='success-booster-bar-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_bar(entered_site, value):
    df = spacex_df[(spacex_df['Payload mass'] <= max(value)) & (spacex_df['Payload mass'] >= min(value))]
    x = df.groupby(['Booster Category'])['Class'].sum()
    data1 = pd.DataFrame(x)
    data1 = data1.reset_index()
    if entered_site == 'ALL':
        fig2 = px.bar(df, x='Booster Category', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig2
    else:
        filtered_df = df[df['Launch site']==entered_site]
        x = filtered_df.groupby(['Booster Category'])['Class'].sum()
        data1 = pd.DataFrame(x)
        data1 = data1.reset_index()
        fig2 = px.bar(filtered_df, x='Booster Category', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig2

@app.callback(Output(component_id='success-booster-probbar-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_probbar(entered_site, value):
    df = spacex_df[(spacex_df['Payload mass'] <= max(value)) & (spacex_df['Payload mass'] >= min(value))]
    x = df.groupby(['Booster Category'])['Class'].mean()
    data1 = pd.DataFrame(x)
    data1 = data1.reset_index()
    if entered_site == 'ALL':
        fig2 = px.bar(data1, x='Booster Category', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig2
    else:
        filtered_df = df[df['Launch site']==entered_site]
        x = filtered_df.groupby(['Booster Category'])['Class'].mean()
        data1 = pd.DataFrame(x)
        data1 = data1.reset_index()
        fig2 = px.bar(data1, x='Booster Category', y = 'Class', color = "Booster Category", color_discrete_map={'v1.0':'blue', 'v1.1':'red', 'FT':'green', 'B4':'brown', 'B5':'gold'})
        return fig2

# Run the app
if __name__ == '__main__':
    app.run_server()
