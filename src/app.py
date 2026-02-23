import dash
from components.layout import create_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = create_layout()

# imported here so callbacks register against `app`
# created in the next step
# import callbacks  # noqa: E402, F401

if __name__ == "__main__":
    app.run(debug=True)