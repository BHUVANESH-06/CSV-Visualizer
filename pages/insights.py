import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import base64
import polars as pl
import io
from dash import html, dcc, dash_table, Input, Output, State
from flask import session, redirect

dash.register_page(__name__, path="/insights")

def is_authenticated():
    return "user" in session

def layout():
    if not is_authenticated():
        return redirect("/login")

    return dbc.Container([
        html.H1("CSV Analyzer", className="text-center text-white"),
        html.P("Upload a CSV file to analyze data in table and graph format.",
               className="text-center text-white lead"),

        html.Div([
            dcc.Upload(
                id="upload-data",
                children=html.Button("Upload CSV", className="btn btn-primary"),
                multiple=False
            ),
        ], className="text-center mt-3 mb-3"),

        html.Div([
            dcc.RadioItems(
                id="view-toggle",
                options=[
                    {"label": html.Span("Table View", style={"margin-left":"10px","margin-right": "20px"}), "value": "table"},
                    {"label": html.Span("Graph View", style={"margin-left":"10px"}), "value": "graph"},
                ],
                value="table",
                inline=True,
                className="text-white"
            )
        ], className="text-center p-3 border border-light rounded bg-dark"),

        html.Div(id="chart-options", children=[
        html.Label("Select Chart Type:", className="text-white"),
        dcc.Dropdown(
                id="chart-type-dropdown",
                options=[
                    {"label": "Scatter Plot", "value": "scatter"},
                    {"label": "Bar Chart", "value": "bar"},
                    {"label": "Line Chart", "value": "line"},
                    {"label": "Pie Chart", "value": "pie"}
                ],
                value="scatter",
                className="mb-3"
            ),
        ], style={"width": "50%", "margin": "auto", "textAlign": "center", "display": "none"}),  

        html.Div(id="axis-options", children=[
            html.Label("Select X-axis:", className="text-white"),
            dcc.Dropdown(id="x-axis-dropdown", className="mb-3"),
            
            html.Label("Select Y-axis (if applicable):", className="text-white"),
            dcc.Dropdown(id="y-axis-dropdown", className="mb-3"),
        ], style={"width": "50%", "margin": "auto", "textAlign": "center", "display": "none"}), 

        html.Div(id="output-container", className="mt-4")

    ], style={"backgroundColor": "#0A0A23", "padding": "40px", "borderRadius": "10px"})

@dash.callback(
    [Output("chart-options", "style"), Output("axis-options", "style")],
    Input("view-toggle", "value")
)
def toggle_chart_options(view_type):
    if view_type == "graph":
        return {"width": "50%", "margin": "auto", "textAlign": "center"}, {"width": "50%", "margin": "auto", "textAlign": "center"}
    return {"display": "none"}, {"display": "none"}


@dash.callback(
    [Output("output-container", "children"),
     Output("x-axis-dropdown", "options"),
     Output("y-axis-dropdown", "options"),
     Output("x-axis-dropdown", "value"),
     Output("y-axis-dropdown", "value")], 
    [Input("upload-data", "contents"),
     Input("view-toggle", "value"),
     Input("chart-type-dropdown", "value"),
     Input("x-axis-dropdown", "value"),
     Input("y-axis-dropdown", "value")],
    State("upload-data", "filename"),
    prevent_initial_call=True
)
def update_output(contents, view_type, chart_type, x_col, y_col, filename):
    if contents and filename.endswith(".csv"):
        try:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            df = pl.read_csv(io.BytesIO(decoded))

            df_display = df.head(1000)

            table = dash_table.DataTable(
                data=df_display.to_dicts(),
                columns=[{"name": i, "id": i} for i in df_display.columns],
                style_table={"maxHeight": "500px", "overflowY": "auto"}, 
                style_header={"backgroundColor": "black", "color": "white"},
                style_cell={"backgroundColor": "#0A0A23", "color": "white", "textAlign": "left"},
                page_action="none", 
            )


            num_cols = [col for col in df.columns if df[col].dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
            all_cols = df.columns

            dropdown_options = [{"label": col, "value": col} for col in all_cols]

            default_x_col = all_cols[0] if len(all_cols) > 0 else None
            default_y_col = num_cols[0] if len(num_cols) > 0 else None

            x_col = x_col or default_x_col
            y_col = y_col or default_y_col

            if view_type == "graph" and x_col:
                if chart_type == "scatter":
                    fig = px.scatter(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Scatter Plot)", template="plotly_dark")
                elif chart_type == "bar":
                    fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Bar Chart)", template="plotly_dark")
                    fig.update_traces(marker=dict(color="blue", line=dict(width=2, color="white")))
                elif chart_type == "line":
                    fig = px.line(df, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Line Chart)", template="plotly_dark")
                elif chart_type == "pie":
                    fig = px.pie(df, names=x_col, title=f"{x_col} Distribution (Pie Chart)", template="plotly_dark")

                fig.update_layout(xaxis_title=x_col, yaxis_title=y_col if y_col else "", title_x=0.5)
                graph = dcc.Graph(figure=fig)
            else:
                graph = html.P("Select X and Y axes to visualize data.", className="text-warning")

            return (table if view_type == "table" else graph, dropdown_options, dropdown_options, x_col, y_col)

        except Exception as e:
            return html.P(f"Error processing file: {str(e)}", className="text-danger"), [], [], None, None

    return html.P("Please upload a valid CSV file.", className="text-danger"), [], [], None, None
