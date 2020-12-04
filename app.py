import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import pandas as pd
import requests
import plotly.express as px



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




def get_rosters():
    league_id = 1194235
    year = 2020
    slotcodes = {
        0 : 'QB', 2 : 'RB', 4 : 'WR',
        6 : 'TE', 16: 'Def', 17: 'K',
        20: 'Bench', 21: 'IR', 23: 'Flex'
    }
    url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + \
      str(2020) + '/segments/0/leagues/' + str(league_id) + \
      '?view=mMatchup&view=mMatchupScore'

    data = []
    print('Week ', end='')
    for week in range(12,14):
        print(week, end=' ')

        r = requests.get(url,
                     params={'scoringPeriodId': week},
                     cookies={"SWID": "{C0029F35-8FC0-4E99-B1F3-74350A1A393F}", "espn_s2": "AECVFCgRUHaRjBzQ2Qi%2BNZi8LROvfzxhsilRma%2FT9XxyP%2BW1ejKJzlt5OqxfBhM6UuXXY9QGUomuZzLIGT3PNXK%2FSTq5RPl2pk27wRErOL7noxJsSIJMqOGZyb09C9ztwYKZkH6M0JoPsIHORZLPB2G%2F4K3kXIa947AIDWmWRsGQWTs9S69NKW71VMB3dpwoSEbfxYlSYOkNZlwXw1aJrvqiEmdHIPbqDf4G8G9MZB9w3EzTa5HPthk6ylP549FXuRfXkB0ABq5IeQQff9zmL8w4"})
        d = r.json()
    
        for tm in d['teams']:
            tmid = tm['id']
            for p in tm['roster']['entries']:
                name = p['playerPoolEntry']['player']['fullName']
                slot = p['lineupSlotId']
                pos  = slotcodes[slot]

                # injured status (need try/exc bc of D/ST)
                inj = 'NA'
                try:
                    inj = p['playerPoolEntry']['player']['injuryStatus']
                except:
                    pass

                # projected/actual points
                proj, act = None, None
                for stat in p['playerPoolEntry']['player']['stats']:
                    if stat['scoringPeriodId'] != week:
                        continue
                    if stat['statSourceId'] == 0:
                        act = round(stat['appliedTotal'],3)
                    elif stat['statSourceId'] == 1:
                        proj = round(stat['appliedTotal'],3)

                data.append([
                    week, tmid, name, slot, pos, inj, proj, act
                ])
        print('\nComplete.')

    data = pd.DataFrame(data, 
                    columns=['Week', 'Team', 'Player', 'Slot', 
                            'Pos', 'Status', 'Proj', 'Actual'])
    url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/{}/segments/0/leagues/{}".format(year,league_id)
    r = requests.get(url,
                 cookies={"swid": "{C0029F35-8FC0-4E99-B1F3-74350A1A393F}",
                          "espn_s2": "AECVFCgRUHaRjBzQ2Qi%2BNZi8LROvfzxhsilRma%2FT9XxyP%2BW1ejKJzlt5OqxfBhM6UuXXY9QGUomuZzLIGT3PNXK%2FSTq5RPl2pk27wRErOL7noxJsSIJMqOGZyb09C9ztwYKZkH6M0JoPsIHORZLPB2G%2F4K3kXIa947AIDWmWRsGQWTs9S69NKW71VMB3dpwoSEbfxYlSYOkNZlwXw1aJrvqiEmdHIPbqDf4G8G9MZB9w3EzTa5HPthk6ylP549FXuRfXkB0ABq5IeQQff9zmL8w4"})
    di = r.json()

    ids = {
        team['id']:team['location'] + " " + team['nickname']
        for team in di['teams']
    }
    
    return data

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col,style={'text-align':'center','border':'2px solid black'}) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col],style={'text-align':'center','border':'none','border-right':'2px solid black'}) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ],style={'width':'50%','border':'2px solid black','backgroundColor':'#AFC7FF','text-align':'center','marginLeft':'auto','marginRight':'auto'}
        )


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
app.title='Fantasy'
def layout():
    ids =  {1: 'K . A . R  . E . E . M .',
            2: 'Catchin babies Unlike agalar',
            3: 'Erybody n the Chubb gin Tipsy',
            4: 'Whale Sharks',
            6: 'Will Lutz n sum BIG BOOTY SLUTZ',
            7: 'Hasta Laviska,  Baby ',
            8: 'Big Baller Waller',
            9: 'Can you  DIGGS it? Sucka',
            10: 'And That Is Dallas',
            12: 'Will and Chase',
            13: 'Team Jafarinia',
            14: 'Hursting My Thielens'}
    players = get_rosters()
    tm1_df = players[(players.Team == 2) & (players.Week == 13) & (players.Pos != 'Bench')].sort_values(by='Slot')
    scores = players[(players.Pos != 'Bench') & (players.Week == 13)].groupby(['Team'])['Actual','Proj'].sum().reset_index()
    cols = ['Actual','Proj']
    scores[cols] = scores[cols].apply(lambda x: round(x,2))
    
    tm1_df.drop(columns={'Week','Slot','Team','Status'},inplace=True)
    tm1_df.loc['Total',['Proj','Actual']] = tm1_df.sum(axis=0)
    tm2_df = tm1_df.copy()
    df = scores[(scores.Team == 7) | (scores.Team == 10)]
    df2 = scores[(scores.Team == 4) | (scores.Team == 9)]
    df['Team'] = df['Team'].apply(lambda x: ids[x])
    df2['Team'] = df2['Team'].apply(lambda x: ids[x])
    racists = pd.DataFrame(['Spencer','CJ','Jake'],columns=['Name'])
    #df2 = df2.drop(columns={'Unnamed: 0'})
    teams = list(df.Team.unique()) + list(df2.Team.unique())
    mas = df.append(df2)
    return html.Div(style={'backgroundColor':'#DDE0E6','marginLeft':'auto','marginRight':'auto'},children=[
                        html.Div(
                        className='scoreboard',
                        children=[
                            html.Div(
                                [
                                    html.H4(children='Scoreboard',style={'color':'black','textDecoration':'underline','text-align':'center'}),
                                    generate_table(df),
                                    generate_table(df2),
                                    html.H4(children='List Of Racists'),
                                    generate_table(racists),
                                ],className='scores',
                                style={'marginLeft':'auto','marginRight':'auto'}
                            ),
                            dcc.Dropdown(
                                id='teams',
                                options=[
                                    {'label': ids[num], 'value': num}
                                    for num in ids
                                    ],
                                value=7,
                                style={'width':'45%'}
                                )]),
                            dcc.Dropdown(
                                id='teams2',
                                options=[
                                    {'label': ids[num], 'value': num}
                                    for num in ids
                                    ],
                                value=10,
                                style={'width':'45%'}
                                ),
                        html.Div(className='rosters',
                                 style={'display':'inline-block','padding':'15px'},
                                 children=[
                            dash_table.DataTable(
                                id='team-table',
                                columns=[{"name":i,"id":i} for i in tm1_df.columns],
                                data=tm1_df.to_dict('records'),
                                style_table={'width':'50%'},
                                style_cell_conditional=[
                                    {'if':{'column_id':'Actual'},
                                     'width':'5%'},
                                    {'if':{'column_id':'Proj'},
                                     'width':'5%'}],
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }]
                                )]),
                        html.Div(style={'display':'inline-block'},
                                 children=[
                            dash_table.DataTable(
                                id='team-table2',
                                columns=[{"name":i,"id":i} for i in tm1_df.columns],
                                data=tm2_df.to_dict('records'),
                                style_table={'width':'50%'},
                                style_cell_conditional=[
                                    {'if':{'column_id':'Actual'},
                                     'width':'5%'},
                                    {'if':{'column_id':'Proj'},
                                     'width':'5%'}],
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                    }]
                                )]),
                        html.Br()
                        
                        
                    ,
                        html.Div(children=[            
                            html.Img(src='https://i.ibb.co/0Y3DrYr/bracket.jpg',
                                 style={
                                'height': 500,
                                'width': 500,
                                "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                })
                                ])
                              
    ])
app.layout = layout

@app.callback(
     [Output(component_id='team-table',component_property='data'),
      Output(component_id='team-table2',component_property='data')],
    [Input(component_id='teams',component_property='value'),
     Input(component_id='teams2',component_property='value')]
    
)



def update_table(matchup,matchup2):
    li = get_rosters()
    print('hi')
    tm1_df = li[(li.Team == matchup) & (li.Week == 13) & (li.Pos != 'Bench')].sort_values('Slot')
    tm2_df = li[(li.Team == matchup2) & (li.Week == 13) & (li.Pos != 'Bench')].sort_values('Slot')
    print(tm1_df.head())
    tm1_df.loc['Total',['Proj','Actual']] = tm1_df.sum(axis=0)
    tm2_df.loc['Total',['Proj','Actual']] = tm2_df.sum(axis=0)
    tm1_df.drop(columns={'Week','Slot','Team','Status'},inplace=True)
    tm2_df.drop(columns={'Week','Slot','Team','Status'},inplace=True)
    return [tm1_df.to_dict('records'), tm2_df.to_dict('records')]



# # Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))



def updateTable(n):
    df, df2 = create_df()
    mas = df.append(df2)
    mas = mas.sort_values(by='team1Score',ascending=False)
    return mas.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
