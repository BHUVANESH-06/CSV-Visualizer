from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import dash
from auth import register_user, verify_user
from flask import session

dash.register_page(__name__, path="/signup")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("Signup", className="text-center text-white mb-4"),
                    dbc.Input(id="signup-username", placeholder="Username", type="text", className="mb-2"),
                    dbc.Input(id="signup-password", placeholder="Password", type="password", className="mb-3"),
                    dbc.Button("Signup", id="signup-btn", color="success", className="w-100"),
                    html.Div(id="signup-output", className="mt-3 text-center text-danger"),
                    dbc.Button("Already registered? Login", href="/login", color="secondary", className="mt-2 w-100"),
                ]),
                className="shadow-lg p-4", style={"backgroundColor": "#1E1E2F", "borderRadius": "10px"}
            )
        ], width=3)
    ], justify="center", align="center", className="vh-100")
],fluid=True)

