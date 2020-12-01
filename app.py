import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/bwalters13/flying-dog-beers/master/game1.csv')
df = df.drop(columns={'Unnamed: 0'})
df.columns = ['team','score']

df2 = pd.read_csv('https://raw.githubusercontent.com/bwalters13/flying-dog-beers/master/game2.csv')
df2 = df2.drop(columns={'Unnamed: 0'})
df2.columns = ['team','score']
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Fantasy'
app.layout = html.Div(children=[
    html.H4(children='Scoreboard'),
    generate_table(df),
    generate_table(df),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
])



def updateTable(n):
    df = pd.read_csv('https://raw.githubusercontent.com/bwalters13/flying-dog-beers/master/game2.csv')
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)

