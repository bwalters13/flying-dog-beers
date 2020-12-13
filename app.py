



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
    for week in range(13,15):
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
    cols = ['Proj','Actual']
    data[cols] = data[cols].apply(lambda x: round(x,2))
    
    return data

def generate_table(dataframe,color ,max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col,style={'text-align':'center','border':'2px solid black'}) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col],style={'text-align':'center','border':'2px solid black','border-right':'2px solid black'}) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
            
        ])
    ],style={'padding':'15px','float':'left','width':'50%','border':'2px solid black','backgroundColor': color,'text-align':'center','marginLeft':'auto','marginRight':'auto'}
        )


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, minimum-scale=1"}])
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
    tm1_df = players[(players.Team == 4) & (players.Week.isin([13,14])) & (players.Pos != 'Bench') & (players.Pos != 'IR')].sort_values(by='Slot')
    tm2_df = players[(players.Team == 9) & (players.Week.isin([13,14])) & (players.Pos != 'Bench') & (players.Pos != 'IR')].sort_values(by='Slot')
    tm3_df = players[(players.Team == 7) & (players.Week.isin([13,14])) & (players.Pos != 'Bench') & (players.Pos != 'IR')].sort_values(by='Slot')
    tm4_df = players[(players.Team == 10) & (players.Week.isin([13,14])) & (players.Pos != 'Bench') & (players.Pos != 'IR')].sort_values(by='Slot')
    
    scores = players[(players.Pos != 'Bench') & (players.Week == 13)].groupby(['Team'])['Actual','Proj'].sum().reset_index()
    tm1_df.loc[(tm1_df.Week == 13),'Proj'] = tm1_df.loc[(tm1_df.Week == 13),'Actual']
    tm2_df.loc[(tm2_df.Week == 13),'Proj'] = tm2_df.loc[(tm2_df.Week == 13),'Actual']
    tm3_df.loc[(tm3_df.Week == 13),'Proj'] = tm3_df.loc[(tm3_df.Week == 13),'Actual']
    tm4_df.loc[(tm4_df.Week == 13),'Proj'] = tm4_df.loc[(tm4_df.Week == 13),'Actual']
    cols = ['Actual','Proj']
    scores[cols] = scores[cols].apply(lambda x: round(x,2))
    tm1_df.drop(columns={'Slot','Team','Status'},inplace=True)
    tm2_df.drop(columns={'Slot','Team','Status'},inplace=True)
    tm3_df.drop(columns={'Slot','Team','Status'},inplace=True)
    tm4_df.drop(columns={'Slot','Team','Status'},inplace=True)
    tm1_df.loc['Total',['Proj','Actual']] = tm1_df.sum(axis=0)
    tm2_df.loc['Total',['Proj','Actual']] = tm2_df.sum(axis=0)
    tm3_df.loc['Total',['Proj','Actual']] = tm3_df.sum(axis=0)
    tm4_df.loc['Total',['Proj','Actual']] = tm4_df.sum(axis=0)
    tm2_df.index = tm1_df.index
    tm4_df.index = tm3_df.index
    # matchup1 = pd.concat([tm1_df,tm2_df],axis=1)
    # matchup1.columns = ['Player ','Pos ','Proj ','Actual ','Player','Pos','Proj','Actual']
    # matchup1 = matchup1.reset_index(drop=True).fillna('')
    # matchup2 = pd.concat([tm3_df,tm4_df],axis=1)
    # matchup2.columns = ['Player ','Pos ','Proj ','Actual ','Player','Pos','Proj','Actual']
    df = scores[(scores.Team == 7) | (scores.Team == 10)]
    df2 = scores[(scores.Team == 4) | (scores.Team == 9)]
    df['Team'] = df['Team'].apply(lambda x: ids[x])
    df2['Team'] = df2['Team'].apply(lambda x: ids[x])
    left_to_play = players[(players.Actual.isna()) & (players.Week.isin([13,14])) & (players.Pos != 'Bench') & (players.Pos != 'IR')].groupby(['Team']).count()
    left_to_play.index = [ids[x] for x in left_to_play.index]
    return html.Div(style={'backgroundColor':'#DDE0E6','marginLeft':'auto','marginRight':'auto'},children=[
                        html.Div(
                        className='scoreboard',
                        children=[
                            html.Div(
                                [
                                    html.H4(children='Scoreboard',style={'color':'black','textDecoration':'underline','text-align':'center'}),
                                    html.Table([
                                        html.Thead(
                                            html.Tr([html.Th('',style={'text-align':'center','borderRight':'none'}), 
                                                     html.Th('Team',style={'text-align':'left','border':'2px solid black'}),
                                                     html.Th('Actual',style={'text-align':'center','border':'2px solid black'}),
                                                     html.Th('Proj',style={'text-align':'center','border':'2px solid black'}),
                                                     html.Th('Left To Play',style={'text-align':'center','border':'2px solid black'})])
                                            ),
                                        html.Tbody([
                                            html.Tr([
                                                html.Td(html.Img(src='https://media4.giphy.com/media/xT9Igt1SacnVe3BkQg/giphy-downsized.gif',
                                             style={'float':'right','width':'80px','height':'80px','display':'inline','borderRadius':'50%'})),
                                                html.Td(html.A('Hasta Laviska, Baby',href='https://fantasy.espn.com/football/team?leagueId=1194235&teamId=7')),
                                                html.Td(round(tm3_df.loc['Total','Actual'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(round(tm3_df.loc['Total','Proj'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(0,
                                                        style={'text-align':'center'})
                                                
                                                ]),
                                            html.Tr([
                                                html.Td(html.Img(src='https://img.buzzfeed.com/buzzfeed-static/static/2019-12/27/3/enhanced/3a6729677dba/enhanced-7541-1577416148-8.jpg?downsize=900:*&output-format=auto&output-quality=auto',
                                             style={'float':'right','width':'80px','height':'80px','display':'inline','borderRadius':'50%'})),
                                                html.Td(html.A('And That is Dallas',href='https://fantasy.espn.com/football/team?leagueId=1194235&teamId=10')),
                                                html.Td(round(tm4_df.loc['Total','Actual'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(round(tm4_df.loc['Total','Proj'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(left_to_play.loc[ids[10],'Week'],
                                                        style={'text-align':'center'})
                                                ])
                                            ],style={'margin':0, 'padding':0})
    ],style={'width':'100%','border':'2px solid black','backgroundColor': 'white','text-align':'center','marginLeft':'auto','marginRight':'auto'}
        ),
                                    html.Table([
                                        html.Thead(
                                            html.Tr([html.Th('',style={'text-align':'center','borderRight':'none'}), 
                                                     html.Th('Team',style={'text-align':'left','border':'2px solid black'}),
                                                     html.Th('Actual',style={'text-align':'center','border':'2px solid black'}),
                                                     html.Th('Proj',style={'text-align':'center','border':'2px solid black'}),
                                                     html.Th('Left To Play',style={'text-align':'center','border':'2px solid black'})])
                                            ),
                                        html.Tbody([
                                            html.Tr([
                                                html.Td(html.Img(src='https://www.holbrooktravel.com/sites/default/files/THUMB-whale-shark-stock_0.jpg',
                                             style={'float':'right','width':'80px','height':'80px','display':'inline','borderRadius':'50%'})),
                                                html.Td(html.A('Whale Sharks',href='https://fantasy.espn.com/football/team?leagueId=1194235&teamId=4')),
                                                html.Td(round(tm1_df.loc['Total','Actual'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(round(tm1_df.loc['Total','Proj'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(left_to_play.loc['Whale Sharks','Week'],
                                                        style={'text-align':'center'})
                                                ]),
                                            html.Tr([
                                                html.Td(html.Img(src='https://prowrestlingnewshub.com/wp-content/uploads/2019/07/Booker-T.jpg',
                                             style={'float':'right','width':'80px','height':'80px','display':'inline','borderRadius':'50%'})),
                                                html.Td(html.A('Can you DIGGS it? Sucka',href='https://fantasy.espn.com/football/team?leagueId=1194235&teamId=9',target='_blank')),
                                                html.Td(round(tm2_df.loc['Total','Actual'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(round(tm2_df.loc['Total','Proj'],2),
                                                        style={'text-align':'center'}),
                                                html.Td(left_to_play.loc['Can you  DIGGS it? Sucka','Week'],
                                                        style={'text-align':'center'})
                                                ])
                                            ],style={'margin':0,'padding':0})
    ],style={'width':'100%','border':'2px solid black','backgroundColor': 'white','text-align':'center','marginLeft':'auto','marginRight':'auto'}
        ),
                                    
                                    
                                    # generate_table(df,'#FDC1FB'),
                                    # generate_table(df2,'#90FFE1'),
                                    
                                ],className='scores',
                                style={'marginLeft':'auto','marginRight':'auto','position':'relative'}
                            ),
                            dcc.Tabs(
                                style={'width':'45%','marginLeft':'auto','marginRight':'auto','padding':'15px'},
                                id='matchup',
                                value='tab-1',
                                children=[
                                    dcc.Tab(label='Ben vs. Jake',children=[
                                            generate_table(tm1_df[tm1_df.Week == 14].drop(columns={'Week'}),'#C7FFEF'),
                                            generate_table(tm2_df[tm2_df.Week == 14].drop(columns={'Week'}),'#F3D0FF')
                                        ],
                                        style={'width':'50%'}),
                                    dcc.Tab(label='Spencer vs. CJ',children=[
                                            generate_table(tm3_df[tm3_df.Week == 14].drop(columns={'Week'}),'#C7FFEF'),
                                            generate_table(tm4_df[tm4_df.Week == 14].drop(columns={'Week'}),'#F3D0FF')
                                        ])
                                    ]),
                            # dcc.Dropdown(
                            #     id='teams2',
                            #     options=[
                            #         {'label': ids[num], 'value': num}
                            #         for num in ids
                            #         ],
                            #     value=10,
                            #     style={'width':'45%'}
                            #     ),
                        # html.Div(className='rosters',
                        #          style={'display':'inline-block','padding':'15px'},
                        #          children=[
                        #     dash_table.DataTable(
                        #         id='team-table',
                        #         columns=[{"name":i,"id":i} for i in tm1_df.columns],
                        #         data=tm1_df.to_dict('records'),
                        #         style_table={'width':'50%'},
                        #         style_cell_conditional=[
                        #             {'if':{'column_id':'Actual'},
                        #              'width':'5%'},
                        #             {'if':{'column_id':'Proj'},
                        #              'width':'5%'}],
                        #         style_data_conditional=[
                        #             {
                        #                 'if': {'row_index': 'odd'},
                        #                 'backgroundColor': 'rgb(248, 248, 248)'
                        #             }]
                        #         )]),
                        # html.Div(style={'display':'inline-block'},
                        #          children=[
                        #     dash_table.DataTable(
                        #         id='team-table2',
                        #         columns=[{"name":i,"id":i} for i in tm1_df.columns],
                        #         data=tm2_df.to_dict('records'),
                        #         style_table={'width':'50%'},
                        #         style_cell_conditional=[
                        #             {'if':{'column_id':'Actual'},
                        #              'width':'5%'},
                        #             {'if':{'column_id':'Proj'},
                        #              'width':'5%'}],
                        #         style_data_conditional=[
                        #             {
                        #                 'if': {'row_index': 'odd'},
                        #                 'backgroundColor': 'rgb(248, 248, 248)'
                        #             }]
                        #         )]),
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
                              
    ])
app.layout = layout





# def update_table(matchup):
#     li = get_rosters()
#     print('hi')
#     tm1_df = li[(li.Team == matchup) & (li.Week == 13) & (li.Pos != 'Bench')].sort_values('Slot')
#     tm2_df = li[(li.Team == matchup2) & (li.Week == 13) & (li.Pos != 'Bench')].sort_values('Slot')
#     print(tm1_df.head())
#     tm1_df.loc['Total',['Proj','Actual']] = tm1_df.sum(axis=0)
#     tm2_df.loc['Total',['Proj','Actual']] = tm2_df.sum(axis=0)
#     tm1_df.drop(columns={'Week','Slot','Team','Status'},inplace=True)
#     tm2_df.drop(columns={'Week','Slot','Team','Status'},inplace=True)
#     return [tm1_df.to_dict('records'), tm2_df.to_dict('records')]



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
