from flask import session
from dash import dcc

def protect_route():
    print("Protected Route")
    if not session.get("user"):
        return dcc.Location(href="/login",id="redirect-login")
    return None