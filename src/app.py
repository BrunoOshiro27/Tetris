from dash_extensions.enrich import DashProxy, html, Output, Input

app_basico = DashProxy(prevent_initial_callbacks=True)
app_basico.layout = html.Div([
    html.Button("Clique aqui", id="btn"),
    html.Div(id="output")
])

@app_basico.callback(Output("output", "children"), Input("btn", "n_clicks"))
def atualizar(n_clicks):
    return f"Cliques: {n_clicks}"
