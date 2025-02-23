import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import polars as pl
from dash import html, dcc, dash_table, Input, Output
from flask import session, redirect

# Hard-coded file paths (update these to your actual file locations)
CSV_PATH_1 = r"C:\Users\bhuva\Downloads\SampleSuperstore.csv"
CSV_PATH_2 = r"C:\Users\bhuva\Downloads\cereal.csv"
CSV_PATH_3 = r"C:\Users\bhuva\Downloads\20170308hundehalter.csv"

df1 = pl.read_csv(CSV_PATH_1)
df2 = pl.read_csv(CSV_PATH_2)
df3 = pl.read_csv(CSV_PATH_3)

dfs = [df1, df2, df3]

dash.register_page(__name__, path="/insights")

def is_authenticated():
    return "user" in session

def layout():
    if not is_authenticated():
        return redirect("/login")
    
    return dbc.Container([
        html.H1("CSV Analyzer", className="text-center text-white"),
        html.P("Displaying three CSV files in table and graph format.",
               className="text-center text-white lead"),
        
        html.Div("CSV files loaded directly from the local system.", 
                 className="text-center text-white mt-3 mb-3"),

        html.Div(
            dcc.Tabs(
                id="csv-tabs",
                value="tab-0",
                children=[
                    dcc.Tab(label="CSV 1", value="tab-0"),
                    dcc.Tab(label="CSV 2", value="tab-1"),
                    dcc.Tab(label="CSV 3", value="tab-2")
                ]
            ),
            className="rounded bg-dark"
        ),

        html.Div([
            dcc.RadioItems(
                id="view-toggle",
                options=[
                    {"label": html.Span("Table View", style={"margin-left": "10px", "margin-right": "20px"}), "value": "table"},
                    {"label": html.Span("Graph View", style={"margin-left": "10px"}), "value": "graph"},
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
    [Input("csv-tabs", "value"),
     Input("view-toggle", "value"),
     Input("chart-type-dropdown", "value"),
     Input("x-axis-dropdown", "value"),
     Input("y-axis-dropdown", "value")]
)
def update_output(selected_tab, view_type, chart_type, x_col, y_col):
    try:
        index = int(selected_tab.split("-")[1])
        df = dfs[index]
        df_display = df.head(1000)
        
        table = dash_table.DataTable(
            data=df_display.to_dicts(),
            columns=[{"name": col, "id": col} for col in df_display.columns],
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={
                "maxHeight": "500px",
                "overflowY": "auto",
                "border": "2px solid #ddd",
                "margin": "20px 0",
            },
            style_header={
                "backgroundColor": "#0074D9",
                "color": "white",
                "fontWeight": "bold",
                "textAlign": "center",
                "border": "2px solid #ddd",
            },
            style_cell={
                "backgroundColor": "white",
                "color": "#333",
                "textAlign": "center",
                "padding": "12px",
                "minWidth": "120px",
                "width": "150px",
                "maxWidth": "250px",
                "overflow": "hidden",
                "textOverflow": "ellipsis",
                "border": "1px solid #ddd",
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#f9f9f9",
                },
                {
                    "if": {"state": "selected"},
                    "backgroundColor": "#FF4136",
                    "border": "2px solid #FF4136",
                },
            ],
            style_as_list_view=True,
        )
        
        num_cols = [col for col in df.columns if df[col].dtype in (pl.Int64, pl.Float64, pl.Int32, pl.Float32)]
        all_cols = df.columns
        dropdown_options = [{"label": col, "value": col} for col in all_cols]
        
        default_x_col = all_cols[0] if len(all_cols) > 0 else None
        default_y_col = num_cols[0] if len(num_cols) > 0 else None

        x_col = x_col or default_x_col
        y_col = y_col or default_y_col

        if view_type == "graph" and x_col:
            df_pd = df.to_pandas()
            if chart_type == "scatter":
                fig = px.scatter(df_pd, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Scatter Plot)", template="plotly_white")
            elif chart_type == "bar":
                fig = px.bar(df_pd, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Bar Chart)", template="plotly_white")
                fig.update_traces(marker=dict(color="blue", line=dict(width=2, color="white")))
            elif chart_type == "line":
                fig = px.line(df_pd, x=x_col, y=y_col, title=f"{x_col} vs {y_col} (Line Chart)", template="plotly_white")
            elif chart_type == "pie":
                fig = px.pie(df_pd, names=x_col, title=f"{x_col} Distribution (Pie Chart)", template="plotly_white")
            
            fig.update_layout(xaxis_title=x_col, yaxis_title=y_col if y_col else "", title_x=0.5)
            output_component = dcc.Graph(figure=fig)
        else:
            output_component = table

        return (output_component, dropdown_options, dropdown_options, x_col, y_col)

    except Exception as e:
        return html.P(f"Error processing data: {str(e)}", className="text-danger"), [], [], None, None

if __name__ == '__main__':
    from dash import Dash
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout
    app.run_server(debug=True)
