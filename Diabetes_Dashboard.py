import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

df = pd.read_csv('./diabetes.csv')
df=df.sort_values("Age")
df['Outcome'] = df['Outcome'].astype(str)
df['Outcome'] = df['Outcome'].str.replace('0', 'negative')
df['Outcome'] = df['Outcome'].str.replace('1', 'positivity')

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Diabetes_Dashboard", style = {"text-align" : "center"}),

        html.H4("Select Age", style = {"margin-left" : "497px"}),
        html.Div(children = [
            dcc.Dropdown(options = [
                {"label" : i , "value" : i}for i in df['Age'].unique()],
                value = 21,
                multi = False,
                id = "Input_Dropdown_Age")],
                style = {"width" : "48%",  "margin" :"auto"}
                ),
        
        html.Div(children = [
            dcc.Graph(id = "Output_bar_fig", style = {"float" : "left", "width" : "50%"}),
            dcc.Graph(id = "Output_line_fig", style = {"float" : "left", "width" : "50%"}),
        ]),

        html.Br(),
        html.Br(),
        html.Div(children = [
            dcc.Graph(id = "Output_scatter_fig_1", style={"float" : "left"}),
            dcc.Graph(id = "Output_scatter_fig_2", style={"float" : "left"}),
            dcc.Graph(id = "Output_scatter_fig_3", style={"float" : "left"}),
            dcc.Graph(id = "Output_pie_fig", style={"float" : "left"})
        ])
    ])
])

@app.callback(
    Output(component_id = "Output_bar_fig", component_property = "figure"),
    Output(component_id = "Output_line_fig", component_property = "figure"),
    Output(component_id = "Output_scatter_fig_1", component_property = "figure"),
    Output(component_id = "Output_scatter_fig_2", component_property = "figure"),
    Output(component_id = "Output_scatter_fig_3", component_property = "figure"),
    Output(component_id = "Output_pie_fig", component_property = "figure"),
    Input(component_id = "Input_Dropdown_Age", component_property = "value")
)

def update_figure(select_Age):
    dff = df[df['Age'] == select_Age]

    bar_fig = px.bar(dff, x = 'Pregnancies', y = 'Outcome', color = 'Pregnancies')

    line_fig = px.scatter(dff, x ='Glucose', y ='Outcome', color = 'Glucose')

    scatter_fig_1 = px.scatter_3d(dff , x = 'BloodPressure', y = 'Outcome', z = 'Age', color = 'BloodPressure')
    scatter_fig_1.update_layout(title = "BloodPressue to Occur Diabetes", autosize = False, width = 470,)

    pie_fig = px.pie(dff, title = "BMI to Occur Diabetes", values = 'BMI', names = 'Outcome', color = 'Outcome', hole = 0.3)
    pie_fig.update_layout(autosize = False, width = 470)

    line_fig_1 = px.line(dff, x = 'Insulin', y = 'DiabetesPedigreeFunction', color = 'Outcome')
    line_fig_1.update_layout(title = "Isulin, DiabetesPedigreeFunction correlation", autosize = False, width = 470)

    fig_3d = go.Figure(data=[go.Surface(z=df.values)])
    fig_3d.update_layout(title = "Diabetes value", autosize = False, width = 470)


    return bar_fig, line_fig, scatter_fig_1, pie_fig, line_fig_1, fig_3d


if __name__ == "__main__" : 
    app.run_server(debug = True)
