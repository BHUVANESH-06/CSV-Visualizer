import dash
import dash_bootstrap_components as dbc
from flask import Flask, session, redirect, request
from dash import html, dcc, Input, Output, State
from flask_session import Session
from config import SESSION_CONFIG
from dash.exceptions import PreventUpdate
from auth import verify_user, register_user

server = Flask(__name__)
server.config.update(SESSION_CONFIG)
Session(server)

app = dash.Dash(
    __name__, 
    server=server, 
    use_pages=True,  
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

import pages.home  
import pages.login  
import pages.signup  

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    
    html.Div( 
        id="navbar-container",
        style={
            "margin": "0",
            "padding": "0",
            "display": "flex",
            "justifyContent": "space-between",
            "width": "100vw",  
            "position": "fixed",  
            "top": "0",
            "left": "0",
            "zIndex": "1000"
        }
    ),

    html.Div(  
        dash.page_container, 
        className="flex-grow-1 w-100 mh-100",
        style={"minHeight": "100vh", "paddingTop": "60px"}  
    )
], style={
    "backgroundColor": "#0A0A23", 
    "minHeight": "100vh",  
    "display": "flex",
    "flexDirection": "column",
    "overflow": "hidden"
})

@app.callback(
    Output("navbar-container", "children"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def update_navbar(pathname):
    if session.get("last_navbar_update") == pathname:
        raise PreventUpdate 
    
    session["last_navbar_update"] = pathname 

    print(f"Updating Navbar -> Path: {pathname}") 

    if "user" in session:
        return dbc.Navbar(
            dbc.Container(
                [
                    dbc.NavbarBrand("CSV Analyzer", href="/", className="text-white", style={"marginLeft":"15px"}),
                    dbc.Nav(
                        [
                            dbc.NavLink("Home", href="/", className="text-white mx-3"),
                            dbc.Button("Logout", n_clicks=0, id="logout-btn", className="text-white"),
                        ],
                        className="ms-auto mx-3", 
                        navbar=True,
                        style={"marginRight":"15px"}
                    ),
                ],
                fluid=True,
            ),
            color="dark",
            dark=True,
            className="w-100",
            style={"position": "fixed", "top": "0", "left": "0", "zIndex": "1000"},
        )

    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand("CSV Analyzer", href="/", className="text-white", style={"marginLeft":"15px"}),
                dbc.Nav(
                    [
                        dbc.NavLink("Register", href="/signup", className="text-white mx-3"),
                    ],
                    className="ms-auto",  
                    navbar=True,
                    style={"marginRight":"15px"}
                ),
            ],
            fluid=True,
        ),
        color="dark",
        dark=True,
        className="w-100",
        style={"position": "fixed", "top": "0", "left": "0", "zIndex": "1000"},
    )



@app.callback(
    Output("url", "pathname"),
    Input("logout-btn", "n_clicks"),
    prevent_initial_call=True
)

def handle_logout(n_clicks):
    if(n_clicks):
        print("Handle Logout")
        session.pop("user", None)
        return "/signup"
    raise dash.exceptions.PreventUpdate

@app.callback(
    Output("login-output", "children"),
    Input("login-btn", "n_clicks"),
    [State("login-username", "value"), State("login-password", "value")],
    prevent_initial_call=True
)

def handle_login(n_clicks, username, password):
    print("Handle Login")
    if n_clicks:
        if verify_user(username, password):
            session["user"] = username
            return dcc.Location(href="/", id="redirect-home")
        return "Invalid username or password."
    return ""

@app.callback(
    Output("signup-output", "children"),
    Input("signup-btn", "n_clicks"),
    [State("signup-username", "value"), State("signup-password", "value")],
    prevent_initial_call=True
)

def handle_signup(n_clicks, username, password):
    print("Handle Signup")
    if n_clicks:
        if register_user(username, password):
            return "Signup successful! Go to login."
        return "Username already exists."
    return ""

def is_authenticated():
    return "user" in session

@app.server.before_request
def restrict_access():
    if request.path.startswith("/_dash"):
        return
    if not is_authenticated() and request.path == "/insights":
        return redirect("/login") 

if __name__ == "__main__":
    app.run(debug=True,threaded=True)