import dash
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# * SE DEFINEN LAS COLUMNAS QUE SE USARÁN
columns = ["MES_FACTURACION", "NOM_EMPRESA", "PROMEDIO_CONSUMO"]

df = pd.read_csv("PROYECTO/BD_STAGE.csv", usecols=columns, delimiter=';')

# * SE CONVIERTE LA COLUMNA MES A FORMATO FECHA
df["MES_FACTURACION"] = pd.to_datetime(df["MES_FACTURACION"].astype(str), format="%Y%m")

df_grouped = df.groupby(["MES_FACTURACION", "NOM_EMPRESA"])["PROMEDIO_CONSUMO"].sum().reset_index()

# * SE AGREGA COLUMNA MES Y TRIMESTRE Y SE CONVIERTE LA FECHA A TIMESTAMP
df_grouped["DATE_ORDINAL"] = df_grouped["MES_FACTURACION"].apply(lambda x: x.timestamp())
df_grouped['ANIO'] = df_grouped['MES_FACTURACION'].dt.year
df_grouped['MES'] = df_grouped['MES_FACTURACION'].dt.month
df_grouped['TRIMESTRE'] = df_grouped['MES_FACTURACION'].dt.quarter

encoder = LabelEncoder()
df_grouped["EMPRESA_ID"] = encoder.fit_transform(df_grouped["NOM_EMPRESA"])

X = df_grouped[["DATE_ORDINAL", "ANIO", "MES", "TRIMESTRE", "EMPRESA_ID"]]
y = df_grouped["PROMEDIO_CONSUMO"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

modelo = RandomForestRegressor(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

controls = [
    dbc.Row(
        html.H1("Predicción de Consumo por Empresa"),
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Label("Selecciona un rango de fecha:"), width=3),
        dbc.Col(dcc.DatePickerRange(
            id="fecha-rango",
            start_date=df["MES_FACTURACION"].min(),
            end_date=df["MES_FACTURACION"].max(),
            display_format="YYYY-MM-DD",
            start_date_placeholder_text="Fecha de Inicio",
        ), width=6),
    ], className="mb-3"),
    dbc.Button(
            "Limpiar Fechas",
            id="clear-dates-btn",
            color="primary",
            className="mt-3 mb-3",
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(html.Label("Selecciona una empresa:"), width=3),
        dbc.Col(dcc.Dropdown(
            id="empresa-dropdown",
            options=[{"label": emp, "value": emp} for emp in df["NOM_EMPRESA"].unique()],
            multi=True,
            placeholder="Filtrar por empresa",
        ), width=6),
    ], className="mb-3"),
]

app.layout = dbc.Container(
    fluid=True,
    className="mt-4 mx-4",
    children=[
        html.H2(
            "Modelamiento de Datos Predicción de Consumo por empresa"
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(dbc.Card(controls, body=True), md=6, width=9),
            ]
        ),
        dbc.Row(
            [
                dcc.Graph(id="grafico-prediccion", style={"height": "700px"}, className="mt-4"), 
            ]
        ),
    ]
)


@app.callback(
    [
        Output("fecha-rango", "start_date"),
        Output("fecha-rango", "end_date")
    ],
    [
        Input("clear-dates-btn", "n_clicks")
    ],
)
def clear_dates(n_clicks):
    if n_clicks:
        return df_grouped["MES_FACTURACION"].min().date(), df_grouped["MES_FACTURACION"].max().date()
    return dash.no_update, dash.no_update

@app.callback(
    Output("grafico-prediccion", "figure"),
    Input("empresa-dropdown", "value"),
    Input("fecha-rango", "start_date"),
    Input("fecha-rango", "end_date")
)
def actualizar_grafico(empresas_seleccionadas, start_date, end_date):  
    
    if not empresas_seleccionadas:
        empresas_seleccionadas = df_grouped["NOM_EMPRESA"].unique().tolist()
        
    empresas_seleccionadas_id = encoder.transform(empresas_seleccionadas)
        
    df_filtrado  = df_grouped[(df_grouped["NOM_EMPRESA"].isin(empresas_seleccionadas)) & 
                        (df_grouped["MES_FACTURACION"] >= start_date) & 
                        (df_grouped["MES_FACTURACION"] <= end_date)]
    
    future_dates = pd.date_range(start=start_date, end=end_date, freq="ME")
    
    predicciones = []
    
    for empresa, empresa_id in zip(empresas_seleccionadas, empresas_seleccionadas_id):
        df_empresa = df_filtrado[df_filtrado["NOM_EMPRESA"] == empresa]
        
        if df_empresa.empty:
            continue
        
        X_pred = pd.DataFrame([
            {"DATE_ORDINAL": date.toordinal(), "ANIO": date.year, "MES": date.month, "TRIMESTRE": date.quarter, "EMPRESA_ID": empresa_id}
            for date in future_dates
        ])
        
        y_pred = modelo.predict(X_pred)
        
        pred_df = pd.DataFrame({
            "MES_FACTURACION": future_dates,
            "NOM_EMPRESA": empresa,
            "PROMEDIO_CONSUMO": y_pred,
            "Tipo": "Predicción"
        })
        
        predicciones.append(pred_df)
    
    if predicciones:
        df_pred = pd.concat(predicciones)
    else:
        df_pred = pd.DataFrame(columns=["MES_FACTURACION", "NOM_EMPRESA", "PROMEDIO_CONSUMO", "Tipo"])
    
    df_filtrado["Tipo"] = "Histórico"
    
    df_final = pd.concat([df_filtrado, df_pred])
    
    fig = px.line(
        df_final, 
        x="MES_FACTURACION", 
        y="PROMEDIO_CONSUMO",
        color="NOM_EMPRESA",  
        line_dash="Tipo",  
        labels={"PROMEDIO_CONSUMO": "Consumo Total", "Tipo": "Datos"},
        title="Consumo Histórico y Predicción"
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)