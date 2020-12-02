import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import requests



def create_df():
    league_id = 1194235
    year = 2020
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}".format(year,league_id)

    r = requests.get(url,params={"view": "mScoreboard"},
                 cookies={"swid": "{C0029F35-8FC0-4E99-B1F3-74350A1A393F}",
                          "espn_s2": "AECVFCgRUHaRjBzQ2Qi%2BNZi8LROvfzxhsilRma%2FT9XxyP%2BW1ejKJzlt5OqxfBhM6UuXXY9QGUomuZzLIGT3PNXK%2FSTq5RPl2pk27wRErOL7noxJsSIJMqOGZyb09C9ztwYKZkH6M0JoPsIHORZLPB2G%2F4K3kXIa947AIDWmWRsGQWTs9S69NKW71VMB3dpwoSEbfxYlSYOkNZlwXw1aJrvqiEmdHIPbqDf4G8G9MZB9w3EzTa5HPthk6ylP549FXuRfXkB0ABq5IeQQff9zmL8w4"})
    d = r.json()

    scores1 = []
    scores2 = []
    for game in d['schedule']:
        try:
            scores1.append([game['away']['teamId'],game['away']['totalPointsLive']])
            scores2.append([game['home']['teamId'],game['home']['totalPointsLive']])
        except:
            pass
    scores = scores1+scores2
    scores = pd.DataFrame(scores,columns=['team1Id','team1Score'])
    
    r = requests.get(url,
                 cookies={"swid": "{C0029F35-8FC0-4E99-B1F3-74350A1A393F}",
                          "espn_s2": "AECVFCgRUHaRjBzQ2Qi%2BNZi8LROvfzxhsilRma%2FT9XxyP%2BW1ejKJzlt5OqxfBhM6UuXXY9QGUomuZzLIGT3PNXK%2FSTq5RPl2pk27wRErOL7noxJsSIJMqOGZyb09C9ztwYKZkH6M0JoPsIHORZLPB2G%2F4K3kXIa947AIDWmWRsGQWTs9S69NKW71VMB3dpwoSEbfxYlSYOkNZlwXw1aJrvqiEmdHIPbqDf4G8G9MZB9w3EzTa5HPthk6ylP549FXuRfXkB0ABq5IeQQff9zmL8w4"})
    di = r.json()

    ids = {
        team['id']:team['location'] + " " + team['nickname']
        for team in di['teams']
    }
    scores['team1Id'] = scores['team1Id'].apply(lambda x: ids[x])
    game1 = scores[(scores.team1Id=='Big Baller Waller') | (scores.team1Id == 'Hasta Laviska,  Baby ')]
    game2 = scores[(scores.team1Id == 'Can you  DIGGS it? Sucka') | (scores.team1Id == 'Will Lutz n sum BIG BOOTY SLUTZ')]
    return game1,game2














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


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Fantasy'
def layout():
    df,df2 = create_df()
    #df = df.drop(columns={'Unnamed: 0'})
    df.columns = ['team','score']

    #df2 = df2.drop(columns={'Unnamed: 0'})
    df2.columns = ['team','score']
    return html.Div(children=[
    html.H4(children='Scoreboard'),
    generate_table(df),
    generate_table(df2),
    html.Br(),
    html.Img(src=app.get_asset_url('https://i.ibb.co/dL2Rz9L/bracket.jpg'))
    html.Div(id='my-output'),
    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])
app.layout = layout


def updateTable(n):
    df = pd.read_csv('game1.csv')
    df2 = pd.read_csv('game2.csv')
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)


