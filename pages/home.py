import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc,callback,Input,Output,State
from flask import session

dash.register_page(__name__, path="/")

layout = dbc.Container([
    # Header Section
    html.Div([
        html.H1("Welcome to CSV Analyzer", className="text-center text-white"),
        html.P("Easily upload, visualize, and analyze CSV data in table and graph format.",
               className="text-center text-white lead"),
    ], className="text-center mb-5"),

    # Features Section
    html.Div([
        html.H3("Key Features", className="text-white mb-3 text-center"),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Upload CSV", className="card-title"),
                    html.P("Quickly upload CSV files for analysis."),
                ])
            ], className="shadow bg-dark text-white"), width=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Table View", className="card-title"),
                    html.P("View CSV data in a structured tabular format."),
                ])
            ], className="shadow bg-dark text-white"), width=4),

            dbc.Col(dbc.Card([
                dbc.CardBody([
                    html.H4("Graph Visualization", className="card-title"),
                    html.P("Automatically generate insights and graphs."),
                ])
            ], className="shadow bg-dark text-white"), width=4),
        ], className="mb-5"),
    ]),
    html.Div([
        dbc.Button("Start Now",id="start-now-btn",color="primary",className="mt-3"),
        dcc.Location(id="redirect",refresh=True),
    ],className="text-center"),
    dbc.Modal([
        dbc.ModalHeader("Login Required"),
        dbc.ModalBody("Please log in to access insights."),
        dbc.ModalFooter(dbc.Button("Go to Login",id="login-btn",href="/login",color="primary")),
    ],id="login-modal",is_open=False)

], className="vh-100 d-flex flex-column", style={"backgroundColor": "#0A0A23", "padding": "40px", "borderRadius": "10px", "minHeight": "100vh", "overflow": "hidden"})

@callback(
    Output("redirect", "pathname"),
    Output("login-modal", "is_open"),
    Input("start-now-btn", "n_clicks"),
    prevent_initial_call=True
)
def start_now(n):
    if "user" in session:
        return "/insights", False  
    return None, True 