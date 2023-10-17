import mysql.connector
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import time

# Crear una función que seleccione los últimos datos de tu tabla y los regrese.
def select_latest_data():
    try:
        cnx = mysql.connector.connect(user='sql10652554', database='sql10652554', password='AI989QAABC', host='sql10.freemysqlhosting.net', port='3306')
        cursor = cnx.cursor()

        # Consultar la base de datos para obtener los últimos datos
        query = ("SELECT * FROM dht_data ORDER BY id DESC LIMIT 100")  # Puedes ajustar la cantidad de datos que deseas obtener

        cursor.execute(query)
        data = cursor.fetchall()
        cnx.close()
        cursor.close()

        return data

    except mysql.connector.Error as err:
        # Manejo de errores
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None

# Crear una función que reciba los datos de la base de datos, los convierta a un dataframe,
# y regrese una gráfica de línea con los datos de humedad y temperatura.
def plot_data():
    try:
        data = select_latest_data()

        if data:
            df = pd.DataFrame(data, columns=['id', 'humidity', 'temperature', 'mq135Value', 'date_time'])
            fig = px.line(df, x='date_time', y=['humidity', 'temperature', 'mq135Value'],
                          labels={'humidity': 'Humedad', 'temperature': 'Temperatura', 'Gas': 'mq135Value'})
            fig.update_layout(
                title='Gráfica de Humedad, Temperatura y Gas',
                xaxis_title='Date Time',
                yaxis_title='Valores'
            )

            return fig

        else:
            print("No se encontraron datos en la base de datos.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(
        children=[
            html.H1("Temperature, Humidity and Gas", style={'text-align': 'center'}),
            html.P("Esta aplicación muestra una gráfica de línea con datos de humedad y temperatura. Los datos fueron generados con un código de python que generó 100 datos entre 0 y 100 tanto para temperatura como para humedad."),
            dcc.Graph(id='live-update-graph', figure=plot_data()),
            dcc.Interval(
                id='interval-component',
                interval=3 * 1000,  # Actualizar cada 3 segundos (en milisegundos)
                n_intervals=0
            )
        ])
])

@app.callback(
    Output('live-update-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    return plot_data()

if __name__ == '__main__':
    app.run_server(debug=True)
