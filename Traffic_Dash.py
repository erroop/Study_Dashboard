import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

df = pd.read_csv('C:/Users/YONSAI/Desktop/db/Dash/Traffic_Dash/Traffic.csv', encoding = 'cp949')
df=df.sort_values("월")
df['월'] = df['월'].astype(str)


app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.H5("please select an option", style = {"font-size" : 15, "color" : "white"})
                    ])
                , width = 2),
                dbc.Col(
                    dbc.Row([html.Div([html.H4("Traffic accident Dashboard", style = {"color" : "white", "margin-left" : "600px"})])])
                ),
            html.Br(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Label("Month select"),
                    html.Br(),
                    dbc.RadioItems(
                        id = "checklist_select_month",
                        options = [
                        {"label" : i, "value" : i}for i in df['월'].unique()],
                        value = "1",
                        label_checked_style = {"color" : "red"},
                        input_checked_style = {
                            "backgroundColor": "#fa7268",
                            "borderColor": "#ea6258"}),
                    ])
                , width = 2, align = "center"),
                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.Div([dcc.Graph(id = "fig1", style = {"margin-bottom" : "20px"})])),
                        dbc.Col(html.Div([dcc.Graph(id = "fig2", style = {"margin-bottom" : "20px"})]))
                    ], align = "center")
                )
            ]),
            html.Br(),

            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Label("road type select"),
                    html.Br(),
                    dbc.RadioItems(
                        id = "checklist_select_roadtype",
                        options = [
                        {"label" : i, "value" : i}for i in df['도로형태'].unique()
                    ],
                    value = '교차로부근',
                    label_checked_style = {"color" : "red"},
                        input_checked_style = {
                            "backgroundColor": "#fa7268",
                            "borderColor": "#ea6258"}),
                    html.Br(),
                    ])
                , width = 2, align = "center"),
            

            dbc.Col(
                dbc.Row([
                    dbc.Col(html.Div([dcc.Graph(id = "fig3", style = {"margin-top" : "20px", "margin-bottom" : "20px"})]), width = 3),
                    dbc.Col(html.Div([dcc.Graph(id = "fig4", style = {"margin-top" : "20px", "margin-bottom" : "20px"})]), width = 3),
                    dbc.Col(html.Div([dcc.Graph(id = "fig5", style = {"margin-top" : "20px", "margin-bottom" : "20px"})]), width = 3),
                    dbc.Col(html.Div([dcc.Graph(id = "fig6", style = {"margin-top" : "20px", "margin-bottom" : "20px"})]), width = 3)
                ], align = "center")
            )
            ]),

            html.Br(),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        dbc.Label("accident type select"),
                    html.Br(),
                    dbc.RadioItems(
                        id = "checklist_select_accident",
                        options = [
                        {"label" :i, "value" : i}for i in df['사고유형'].unique()
                    ],
                    value = "차량단독",
                    label_checked_style = {"color" : "red"},
                        input_checked_style = {
                            "backgroundColor": "#fa7268",
                            "borderColor": "#ea6258"})
                    ])
                , width=2 , align = "center"),

                dbc.Col(
                    dbc.Row([
                        dbc.Col(html.Div([dcc.Graph(id = "fig7", style = {"margin-top" : "20px", "margin-bottom" : "20px"})])),
                        dbc.Col(html.Div([dcc.Graph(id = "fig8", style = {"margin-top" : "20px", "margin-bottom" : "20px"})]))
                        
                    ], align = "center")
                )
            ])
            ])
        ])
    )
])

@app.callback(
    Output(component_id = "fig1", component_property = "figure"),
    Output(component_id = "fig2", component_property = "figure"),
    Output(component_id = "fig3", component_property = "figure"),
    Output(component_id = "fig4", component_property = "figure"),
    Output(component_id = "fig5", component_property = "figure"),
    Output(component_id = "fig6", component_property = "figure"),
    Output(component_id = "fig7", component_property = "figure"),
    Output(component_id = "fig8", component_property = "figure"),
    Input(component_id = 'checklist_select_month', component_property = 'value'),
    Input(component_id = 'checklist_select_roadtype', component_property = 'value'),
    Input(component_id = 'checklist_select_accident', component_property = 'value')
)

def update_fig(checklist_select_month, checklist_select_roadtype, checklist_select_accident):

    df_month = df[df['월'] == checklist_select_month]


    fig_1 = px.bar(df_month, x = df_month[df_month['도로형태'] == checklist_select_roadtype]['도로형태'], y = df_month[df_month['도로형태'] == checklist_select_roadtype]['사망자수'])
    fig_1.update_layout( go.Layout(xaxis={'title': {'text': 'Selected road type'}}, yaxis = {'title':{'text' : '사망자수'}})
                        ,template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)')
                        #paper_bgcolor= 'rgba(0, 0, 0, 0)')
    
    fig_2 = px.bar(df_month, x = df_month[df_month['사고유형'] == checklist_select_accident]['사고유형'], y = df_month[df_month['사고유형'] == checklist_select_accident]['사망자수'])
    fig_2.update_layout(go.Layout(xaxis={'title': {'text': 'Selectd accident sype'}}, yaxis = {'title':{'text' : '사망자수'}})
                        ,template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)')
    
    fig_3 = px.pie(df, values = df['사망자수'], names = df['도로형태'], color = df['도로형태'])
    fig_3.update_layout(template = 'plotly_dark', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_4 = px.pie(df, values = df['사망자수'], names = df['사고유형'], color = df['사고유형'])
    fig_4.update_layout(template = 'plotly_dark', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_5 = px.pie(df , values = df['사망자수'], names = df['주야'], color = df['주야'])
    fig_5.update_layout(template = 'plotly_dark', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_6 = px.pie(df, values = df['사망자수'], names = df['요일'], color = df['요일'])
    fig_6.update_layout(template = 'plotly_dark', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_7 = px.bar(df_month, x = df_month[df_month['도로형태'] == checklist_select_roadtype]['시군'], y = df_month[df_month['도로형태'] == checklist_select_roadtype]['사망자수'])
    fig_7.update_layout(go.Layout(xaxis={'title': {'text': 'Selected road type'}}, yaxis = {'title':{'text' : '사망자수'}}),
                        template = 'plotly_dark', plot_bgcolor= 'rgba(0, 0, 0, 0)')

    fig_8 = px.bar(df_month,x = df_month[df_month['사고유형'] == checklist_select_accident]['시군'], y = df_month[df_month['사고유형'] == checklist_select_accident]['사망자수'])
    fig_8.update_layout(go.Layout(xaxis={'title': {'text': 'Selectd accident sype'}}, yaxis = {'title':{'text' : '사망자수'}})
                        ,template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)')

    return fig_1, fig_2, fig_3, fig_4, fig_5, fig_6, fig_7, fig_8


if __name__ == "__main__":
    app.run_server(debug = True)