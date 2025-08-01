import dash
from dash import html, dcc
import base64
import io
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV File', className='upload-button'),
        multiple=False
    ),

    dcc.Store(id='stored-data'),

    html.Div(id='dropdown-container', className='dropdown-container'),

    dcc.Checklist(
        id='show-charts',
        options=[
            {'label': 'Show Scatter Plot', 'value': 'scatter'},
            {'label': 'Show Heatmap', 'value': 'heatmap'}
        ],
        value=[]
    ),

    html.Div(id='scatter-container', style={'display': 'none'}),
    html.Div(id='heatmap-container', style={'display': 'none'}),
])

@app.callback(
    Output('stored-data', 'data'),
    Input('upload-data', 'contents'),
)
def store_uploaded_file(contents):
    if contents is None:
        return None
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    return df.to_json(date_format='iso', orient='split')

@app.callback(
    Output('dropdown-container', 'children'),
    Input('stored-data', 'data')
)
def update_dropdowns(data_json):
    if data_json is None:
        return html.Div("Upload CSV to select columns.")
    df = pd.read_json(data_json, orient='split')
    options = [{'label': col, 'value': col} for col in df.columns]

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    default_x = numeric_cols[0] if numeric_cols else df.columns[0]
    default_y = numeric_cols[1] if len(numeric_cols) > 1 else default_x

    return html.Div([
        html.Label("Select X-axis:"),
        dcc.Dropdown(id='x_axis', options=options, value=default_x),
        html.Label("Select Y-axis:"),
        dcc.Dropdown(id='y_axis', options=options, value=default_y)
    ])

@app.callback(
    Output('scatter-container', 'children'),
    Output('scatter-container', 'style'),
    Output('heatmap-container', 'children'),
    Output('heatmap-container', 'style'),
    Input('show-charts', 'value'),
    Input('stored-data', 'data'),
    Input('x_axis', 'value'),
    Input('y_axis', 'value'),
)
def update_charts(show_values, data_json, x_axis, y_axis):
    if data_json is None:
        return "", {'display': 'none'}, "", {'display': 'none'}

    df = pd.read_json(data_json, orient='split')

    scatter_children = ""
    scatter_style = {'display': 'none'}
    heatmap_children = ""
    heatmap_style = {'display': 'none'}

    if 'scatter' in show_values and x_axis and y_axis and x_axis in df.columns and y_axis in df.columns:
        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, title=f"Scatter Plot: {x_axis} vs {y_axis}")
        scatter_children = dcc.Graph(figure=fig_scatter)
        scatter_style = {'display': 'block', 'margin-top': '20px'}

    if 'heatmap' in show_values:
        df_numeric = df.select_dtypes(include='number')
        if not df_numeric.empty:
            corr = df_numeric.corr()
            fig_heatmap = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Viridis')
            fig_heatmap.update_layout(title='Correlation Heatmap')
            heatmap_children = dcc.Graph(figure=fig_heatmap)
            heatmap_style = {'display': 'block', 'margin-top': '20px'}

    return scatter_children, scatter_style, heatmap_children, heatmap_style

if __name__ == '__main__':
    app.run(debug=False)
