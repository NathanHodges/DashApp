import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('Tax_Data\statesData.csv')
available_locations = df.Location.unique()
available_taxes = df.Tax_Type.unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='State Taxes Application'),

    dcc.Graph(id='state-graph'),

    html.Label('Choose a state.'),
    dcc.Dropdown(
        id = 'xaxis1-column',
        options=[{'label': i, 'value': i} for i in available_locations],
        value = 'United States'
    ),

    html.Label('Choose another state to compare.'),
    dcc.Dropdown(
        id = 'xaxis2-column',
        options=[{'label': i, 'value': i} for i in available_locations],
        value = 'Alabama'
    ),

    html.Label('Choose Tax Type.'),
    dcc.Dropdown(
        id = 'yaxis-column',
        options=[{'label': i, 'value': i} for i in available_taxes],
        value = 'Total Taxes'
    )
])

@app.callback(
    Output('state-graph', 'figure'),
    [Input('xaxis1-column', 'value'),
     Input('xaxis2-column', 'value'),
     Input('yaxis-column', 'value')])
def update_graph(location1,location2, tax_type):
    dff1 = df[(df['Location']==location1) & (df['Tax_Type']==tax_type)]
    dff2 = df[(df['Location']==location2) & (df['Tax_Type']==tax_type)]

    return {
        'data': [go.Bar(
                x=dff1['Year'],
                y=dff1['Amount'],
                name = location1),
                go.Bar(
                x=dff2['Year'],
                y=dff2['Amount'],
                name = location2)],
        'layout': go.Layout(title = go.layout.Title(text = tax_type))
    }

if __name__ == '__main__':
    app.run_server()
