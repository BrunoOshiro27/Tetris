from dash_extensions.enrich import DashProxy, MultiplexerTransform
from components.layout import create_layout
from callbacks import register_callbacks

app = DashProxy(
    __name__,
    transforms=[MultiplexerTransform()],
    suppress_callback_exceptions=True,
)
app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)