# Task 1:
#    Create a body mass index calculator app. 
#    It should take in height in feet or meters and weight in lbs or kilograms and return the associated body mass index. 
#    Post both the python code for your dash app and a gif screen capture of it running.

# Logic ->  BMI = weight (kg) / (height (m))^2

# dash_bmi_app.py
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        html.H2("BMI Calculator"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Height"),
                        dbc.Input(id="height-input", type="number", min=0, step=0.01, placeholder="Enter height"),
                        dcc.RadioItems(
                            id="height-units",
                            options=[
                                {"label": "meters (m)", "value": "m"},
                                {"label": "feet (ft)", "value": "ft"},
                            ],
                            value="m",
                            labelStyle={"display": "inline-block", "margin-right": "10px"}
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Weight"),
                        dbc.Input(id="weight-input", type="number", min=0, step=0.1, placeholder="Enter weight"),
                        dcc.RadioItems(
                            id="weight-units",
                            options=[
                                {"label": "kilograms (kg)", "value": "kg"},
                                {"label": "pounds (lb)", "value": "lb"},
                            ],
                            value="kg",
                            labelStyle={"display": "inline-block", "margin-right": "10px"}
                        ),
                    ],
                    md=6,
                ),
            ],
            className="mb-3",
        ),
        dbc.Button("Calculate BMI", id="calc-btn", color="primary"),
        html.Hr(),
        html.Div(id="result-output", className="mt-3"),
    ],
    fluid=True,
    className="p-4",
)

def compute_bmi(height, height_unit, weight, weight_unit):
    # Convert height to meters
    if height_unit == "ft":
        # feet to meters: 1 ft = 0.3048 m
        height_m = height * 0.3048
    else:
        height_m = height

    # Convert weight to kg
    if weight_unit == "lb":
        # pounds to kg: 1 lb = 0.45359237 kg
        weight_kg = weight * 0.45359237
    else:
        weight_kg = weight

    if height_m <= 0:
        return None, "Height must be > 0"
    bmi = weight_kg / (height_m ** 2)
    return bmi, None

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"

@app.callback(
    Output("result-output", "children"),
    Input("calc-btn", "n_clicks"),
    State("height-input", "value"),
    State("height-units", "value"),
    State("weight-input", "value"),
    State("weight-units", "value"),
)
def on_calculate(n_clicks, height, height_units, weight, weight_units):
    if not n_clicks:
        return ""
    # Basic input validation
    if height is None or weight is None:
        return dbc.Alert("Please enter both height and weight.", color="warning")

    bmi, err = compute_bmi(height, height_units, weight, weight_units)
    if err:
        return dbc.Alert(err, color="danger")

    category = bmi_category(bmi)
    return dbc.Card(
        dbc.CardBody([
            html.H4(f"BMI: {bmi:.2f}", className="card-title"),
            html.P(f"Category: {category}", className="card-text"),
            html.Small("Height: {:.2f} {} · Weight: {:.1f} {}".format(height, height_units, weight, weight_units))
        ])
    )

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
