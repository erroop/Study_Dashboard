import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

app = Dash(__name__)

df = pd.read_csv('C:/Users/YONSAI/Desktop/db/Dash/아보카도.csv', index_col = 0)

app.layout = html.Div([
    html.Div([
        html.H1("Avocado Prices Dashboard", style ={'text-align' : 'center', 'width' : '70'}),

        html.Br(),

        html.Div(children=[
            dcc.Dropdown(options=[
                {"label" : i, "value" : i}for i in df['geography'].unique()],
                value = 'San Francisco',
                id = "Input_Dropdown_x"),
            
            dcc.RadioItems(options=[
                {'label': 'conventional', 'value' : 'conventional'},
                {'label': 'organic', 'value' : 'organic'}],
                value = 'organic',
                id = "Input_Radio_x",
                inline = True)
        ], style = {'width' : '48%', 'display' : 'inline-block'}),

        html.Div(children=[
            dcc.Dropdown(options = [
                {'label' : i, 'value' :i}for i in df['geography'].unique()],
                value = "Albany",
                id = "Input_Dropdown_y"),

            dcc.RadioItems(options = [
                {'label': 'conventional', 'value' : 'conventional'},
                {'label': 'organic', 'value' : 'organic'}],
                value = 'conventional',
                id = "Input_Radio_y",
                inline = True
            )
        ], style = {'width' : '48%', 'float' : 'right', 'display' : 'inline-block'}),
        
        dcc.Graph(id = "Avocado_fig"),

        dcc.Slider(
            df['year'].min(),
            df['year'].max(),
            value = df['year'].max(),
            marks = {str(year) : str(year) for year in df['year'].unique()},
            id = "year-Slider"),
        

        html.Br(),
        html.Div([
            dcc.Graph(id = "Avocado_fig_1", style = {"float" : "left", "width" : "50%"}),
            dcc.Graph(id = "Avocado_fig_2", style = {"float" : "left", "width" : "50%"})
        ], style = {'float' : 'left'})
    ])])

@app.callback(
    [Output(component_id = "Avocado_fig", component_property = "figure"),
    Output(component_id = "Avocado_fig_1", component_property = 'figure'),
    Output(component_id = "Avocado_fig_2", component_property = "figure")],
    Input(component_id = 'Input_Dropdown_x', component_property = 'value'),
    Input(component_id = 'Input_Dropdown_y', component_property = 'value'),
    Input(component_id = 'Input_Radio_x', component_property = 'value'),
    Input(component_id = 'Input_Radio_y', component_property = 'value'),
    Input(component_id = 'year-Slider', component_property = 'value'))

def update_figure(Input_Dropdown_x, Input_Dropdown_y, Input_Radio_x, Input_Radio_y, year_value):
    dff = df[df['year'] == year_value]

    fig = px.scatter(x = dff[dff['geography'] == Input_Dropdown_x]['average_price'],
                     y = dff[dff['geography'] == Input_Dropdown_y]['average_price'])


    fig.update_layout(autosize = False, height = 600)

    fig.update_xaxes(title=Input_Dropdown_x,
                     type='conventional' if Input_Dropdown_x == 'Linear' else 'log')

    fig.update_yaxes(title=Input_Dropdown_y,
                     type='conventional' if Input_Dropdown_y == 'Linear' else 'log')
    
    fig_1 = px.bar(dff, x = 'geography', y = 'average_price', color = "geography")

    fig_1.update_layout(title = "geography_prices", autosize = False,
                    width = 1300, height = 500, )
    

    fig_2 = go.Figure(data=[go.Surface(z=df.values)])

    fig_2.update_layout(title='Avocado Prices', autosize=False,
                  width=700, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))
    
    return fig, fig_1 , fig_2
if __name__ == '__main__':
    app.run_server(debug = True)