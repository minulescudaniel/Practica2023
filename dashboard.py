import csv
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


csv_filename = "price_history.csv"
df = pd.read_csv(csv_filename)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])


products = df[['Nume', 'Magazin']].drop_duplicates().values.tolist()


app = dash.Dash(__name__)


app.layout = html.Div([
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': f'{product[0]} - {product[1]}', 'value': index} for index, product in enumerate(products)],
        value=0,
    ),
    dcc.Graph(id='price-history-plot'),
])


@app.callback(
    Output('price-history-plot', 'figure'),
    [Input('product-dropdown', 'value')])
def update_plot(selected_product):
    product_info = products[selected_product]
    product_name, store = product_info
    filtered_df = df[(df['Nume'] == product_name) & (df['Magazin'] == store)]

    fig = px.line(filtered_df, x='Timestamp', y='Pret', title=f'Price History for {product_name} in {store}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)