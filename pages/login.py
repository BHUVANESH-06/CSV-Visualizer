import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from flask import session
from auth import verify_user

dash.register_page(__name__, path="/login")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H2("Login", className="text-center text-white mb-4"),
                    dbc.Input(id="login-username", placeholder="Username", type="text", className="mb-2"),
                    dbc.Input(id="login-password", placeholder="Password", type="password", className="mb-3"),
                    dbc.Button("Login", id="login-btn", color="primary", className="w-100"),
                    html.Div(id="login-output", className="mt-3 text-center text-danger"),     
                    dbc.Button("Not registered? Sign Up", href="/signup", color="secondary", className="mt-3 w-100"),
                ]),
                className="shadow-lg p-4", style={"backgroundColor": "#1E1E2F", "borderRadius": "10px"}
            )
        ], width=3)
    ], justify="center", align="center", className="vh-100")
], fluid=True, style={"backgroundColor": "#0A0A23"})
