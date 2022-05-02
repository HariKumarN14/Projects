
import pandas as pd
import numpy as np

import dash
import dash_auth
import plotly.express as px
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import io
from base64 import b64encode

df=pd.read_csv('https://raw.githubusercontent.com/nethajinirmal13/Training-datasets/main/matches.csv')

"""## Cleaning"""

df1=df.drop(['id','umpire1','umpire2','umpire3'],axis=1)   #no need for id since index is there and id is wrong also
df1.info()                                                # no need of umpire data for analysis. do dropping these columns

c1=df1[df1['city'].isnull()]                    #checking the nan values
c1

df1['city']=df1['city'].fillna('Dubai')                #the  null values all belong to same venue, so easily fill the city wit  venue name

temp=df1.groupby('city')['venue']                    #check if filled values are reflecting
temp.first()

c2=df1[df1['winner'].isnull()]
c2

df2=df1.dropna(subset=['winner'])       #dropping the data where result/winner is na. no point in filling those with 0
df2.info()

df2.isna().sum()              #checking there no nan values present

df2['city'].unique()

df2['city'].value_counts()

mappings={'Bangalore':'Bangalore','Bengaluru':'Bangalore'}
df2['city']=df2['city'].replace(mappings)
df2['city'].unique()

mappings={'Rising Pune Supergiant':'Rising Pune Supergiants'}
df2['team1']=df2['team1'].replace(mappings)
df2['team2']=df2['team2'].replace(mappings)
df2['winner']=df2['winner'].replace(mappings)
df2['toss_winner']=df2['toss_winner'].replace(mappings)
print(df2['team1'].unique())
#print(df2['team2'].unique())
#print(df2['winner'].unique())

df2['venue'].unique()

df2['venue'].unique()

mappings={'M. Chinnaswamy Stadium':'M Chinnaswamy Stadium','MA Chidambaram Stadium, Chepauk':'M. A. Chidambaram Stadium'
          ,'Punjab Cricket Association IS Bindra Stadium, Mohali':'Punjab Cricket Association Stadium, Mohali'}

df2['venue']=df2['venue'].replace(mappings)

df2['dl_applied'].value_counts()

df2['date']=pd.to_datetime(df2['date'])
df2.info()

ipl=df2
ipl  #cleaned dataset


def logo(fig):
  fig.add_layout_image(
      dict(
          source="https://raw.githubusercontent.com/HariKumarN14/Heroku/Hari_IPL/docs/assets/ipl.jpg",
          xref="paper", yref="paper",
          x=.5, y=1.05,
          sizex=0.3, sizey=0.3,
          xanchor="left", yanchor="bottom"
      )
  )  
  return fig

def dwnload(fig):
  temp_fig=fig
  buffer = io.StringIO()
  temp_fig.write_html(buffer,
                  full_html=False,
                  include_plotlyjs='cdn')

  html_bytes = buffer.getvalue().encode()
  encoded = b64encode(html_bytes).decode()
  return encoded

df=ipl

x=df['winner'].value_counts().sort_index(ascending=True)
x

y=df['winner'].unique()
y=sorted(y)
y

lst=list()
for i in range(14):
  lst.append(x[i])
lst

x2=df['team1'].value_counts().sort_index(ascending=True)

x3=df['team2'].value_counts().sort_index(ascending=True)

lst2=list()
for i in range(14):
  temp=x2[i]+x3[i]
  lst2.append(temp)

print(lst2)

winner_list=pd.DataFrame({"Team":y,"Win_count":lst,"Total_matches":lst2})         #creating new dataframe with wincounts
winner_list

fig11=px.bar(winner_list,x="Team",y="Win_count",color="Total_matches",title="<b>Win Count of All teams across all seasons")
fig11=logo(fig11)
fig11.show()



fig12=px.scatter(winner_list,x="Team",y="Win_count",size="Win_count",color="Total_matches",title="Win Count of All teams across all seasons")
fig12=logo(fig12)
fig12.show()

fig13= px.pie(winner_list, values="Win_count",names="Team",color="Total_matches",title="Win Count of All teams across all seasons",)
fig13=logo(fig13)
fig13.show()

fig14= px.sunburst(winner_list, path=['Win_count', 
                            'Total_matches',
                            'Team'], 
                  values='Win_count')
fig14=logo(fig14)
fig14.show()



"""###2-->Best player based on player of the match(1 plot)"""

df.head()

x=df['player_of_match'].value_counts().sort_index(ascending=True)
x.shape

fig21=px.histogram(df,x="player_of_match",color='player_of_match')
fig21=logo(fig21)
fig21.show()



"""###3-->find best winning teams based on the win by runs and win by wickets
###(2 plots (winning team vs win by runs and winning team vs win by wickets))
"""

#creating the unique list of winners
df=ipl 
lst=list()
for i in df['winner'].unique():
  lst.append(i)
lst=sorted(lst)
print(lst)

#creating a dateframe with each team and their maximum win by runs and wickets
max_runs=list()
max_wickets=list()

for i in lst:
  x=df[df['winner']==i]
  max_value=x.max()
  
  max_runs.append(max_value['win_by_runs'])
  max_wickets.append(max_value['win_by_wickets'])

win_list=pd.DataFrame({"Team":lst,"MAX_win_by_runs":max_runs,"MAX_win_by_wickets":max_wickets})
win_list

"""####Best team by win by most runs"""

fig31=px.bar(win_list,x="Team",y="MAX_win_by_runs",color="Team",title="Max runs by which each team has won")
fig31.show()

fig32= px.sunburst(win_list, path=['MAX_win_by_wickets', 
                            'MAX_win_by_runs',
                            'Team'], 
                  title="<b>Win Chart:  Max runs and max wickets</b>(click to interact with chart)<br><br></b>"+"<i><b>Outer circle</i>:   Team Name<br>"+
                 "<i><b>Second circle</i>: Max runs by which team has won<br>"+
                 "<i><b>Inner circle</i>:   Max wickets by which team has won" 
                  )
fig32=logo(fig32)
fig32.show()

"""####Best team by win by most wickets"""

fig33=px.bar(win_list,x="Team",y="MAX_win_by_wickets",color="Team",title="Max wickets by which each team has won")
fig33.show()

fig34= px.sunburst(win_list, path=['MAX_win_by_wickets', 
                            'MAX_win_by_runs',
                            'Team'], 
                  )
fig34.show()

"""###4-->Luckiest venue for each team(n-teams count - plots for each team(how
###much played vs how much won))
"""
def favorite(team):
  df=ipl
  #team='Chennai Super Kings'
  df1=df[df['winner']==team]
  df2=pd.DataFrame(df1[['winner','venue']])#.sort_index(ascending=True)
  venue=list()
  lst=list()
  for i in df2['venue'].unique():
    venue.append(i)
  venue=sorted(venue)

  x=df2['venue'].value_counts().sort_index(ascending=True)
  y=x.shape
  for i in range(y[0]):
    lst.append(x[i])

  df_team=pd.DataFrame({"venue":venue,"win_count":lst})
  title="<b>Win count at each stadium for </b>:"+team
  fig411=px.bar(df_team,x="win_count",y="venue",color="venue",title=title)
  fig411=logo(fig411)
  return fig411




df=ipl

lst=list()
for i in df['winner'].unique():
  lst.append(i)
lst=sorted(lst)
print(lst)

"""#####1.Best venue """

#Best venue for Chennai Super Kings

#team=input()
team='Chennai Super Kings'
df1=df[df['winner']==team]
df1
df2=pd.DataFrame(df1[['winner','venue']])#.sort_index(ascending=True)
df2
venue=list()
lst=list()
for i in df2['venue'].unique():
  venue.append(i)

venue=sorted(venue)

x=df2['venue'].value_counts().sort_index(ascending=True)
y=x.shape
for i in range(y[0]):
  lst.append(x[i])


df_team=pd.DataFrame({"venue":venue,"win_count":lst})
#df_team


fig411=px.bar(df_team,x="win_count",y="venue",color="venue",title="Win count at each stadium ")
fig411.show()

fig4101= px.sunburst(df_team, path=[ 
                            'win_count',
                            'venue'], 
                  title="Win count at each stadium  ")
fig4101.show()

"""###5->probability of winning matches vs winning toss(plot for each team)"""

ipl.head()

df=ipl

lst=list()
for i in df['winner'].unique():
  lst.append(i)
lst=sorted(lst)
print(lst)  #list of teams in alphabetical order

x2=df['team1'].value_counts().sort_index(ascending=True)
x3=df['team2'].value_counts().sort_index(ascending=True)

lst_2=list()
for i in range(14):
  temp=x2[i]+x3[i]
  lst_2.append(temp)

print(len(lst_2))   #list of total matches played by teams

y=df['winner'].value_counts().sort_index(ascending=True)

lst3=list()
for i in range(14):
  lst3.append(y[i])
lst3  #list of total games won

x=pd.DataFrame({"winner":df['winner'],"toss_winner":df['toss_winner'],"toss_decision":df['toss_decision']})
y=x['toss_winner'].value_counts().sort_index(ascending=True)
y

new_list=list()
df1=ipl
yy=df1['toss_winner'].value_counts().sort_index(ascending=True)
yy
for i in range(14):
  new_list.append(yy[i])
new_list

df2=ipl
x1=pd.DataFrame({"winner":df2['winner'],"toss_winner":df2['toss_winner']})

x2=x1.reset_index(drop=True)
x2

lst_toss_win=list()
for i in lst:
  temp=0
  for k in range(752):
    if x2['winner'][k]==i and x2['toss_winner'][k]==i:
      temp+=1
    else:
      pass
  lst_toss_win.append(temp)
lst_toss_win  #list of winning when toss won

win_percent=list()
win=0
for i in range(14):
    win=(lst_toss_win[i]/new_list[i])*100
    win_percent.append(win)
win_percent

win_percent_toss=pd.DataFrame({"Team":lst,"Total_matches_played":lst_2,"Total_matches_won":lst3,"no:times toss won":new_list,
                               "no:times won when toss won":lst_toss_win,"Win_match_toss_%":win_percent})
win_percent_toss

fig_all= px.sunburst(win_percent_toss, path=['Win_match_toss_%',
                            'no:times toss won',
                            'Team'] ,
                 title="<b>Win% chart</b>(click to interact with chart)<br><br></b>"+"<i><b>Outer circle</i>:   Team Name<br>"+
                 "<i><b>Second circle</i>: No:of times toss won<br>"+
                 "<i><b>Inner circle</i>:   Win percentage when toss is won" )
fig_all=logo(fig_all)
fig_all.show()

df=win_percent_toss
fig1=px.bar(df,x=df['Team'],y='Win_match_toss_%',color='no:times toss won')
fig1.show()

x=ipl['season'].unique()
x=sorted(x)

import plotly.graph_objects as go
win=(3,1,0,0,0,0,0,2,4,0,1,0,0,1)
df=win_percent_toss
rowEvenColor = '#4F75CD'
rowOddColor = '#4F91CD'

fig_stats = go.Figure(data=[go.Table
                          (
                        header=dict(values=['Team', 'Total_matches(All_Seasons','Total_Wins(All_Seasons','N0: of IPL Trophies won'],
                                     font=dict(color='whitesmoke', size=18),
                                    line_color='black',
                                    fill_color='#19388A',
                                    height=50),
                        cells=dict(values=[df['Team'], df['Total_matches_played'],df['Total_matches_won'],win],
                                   font=dict(color='white', size=12),
                                    line_color='black',
                                    fill_color=[[rowOddColor,rowEvenColor,rowOddColor,rowEvenColor]*4],
                                   height=30)
                        )
                     ])
fig_stats=logo(fig_stats)



"""##dash"""
USERNAME_PASSWORD_PAIRS=[['guvi','guvi']]
app=dash.Dash(__name__)
auth= dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
server=app.server

app.layout=html.Div([
          
          html.A(html.Img(src="https://raw.githubusercontent.com/HariKumarN14/Heroku/Hari_IPL/docs/assets/wp7104495-ipl-logo-wallpapers.jpg",width="600" ,height="150"),
          href="https://www.iplt20.com/",target='_blank'),
   html.H2(children='Hello Fan!!!',
           style={"textAlign": "center",
                  'color':'#19388A',
                  'background-color':'white',
                  'font-size':'200%'
                  }),
 
   html.H2(children='''
       Welcome to the IPL Analysis:.
   ''',
   style={"textAlign": "center",
          'color':'#E6E6FA',
          'background-color':'#19388A'
   }),
   html.Div([
   html.Label("Please select any option from 1-7"),
        dcc.Dropdown(
         id='FirstDropdown',
         options=[
                {'label':"1.IPL stats from 2008-2019",'value':'v'},
                {'label':"2. Best teams based on winning count",'value':'v1'},
                {'label':"3. Best player based on player of the match",'value':'v2'},
                {'label':"4. Best winning teams based on the win by runs and win by wickets",'value':'v3'},
                {'label':"5. Luckiest venue for each team",'value':'v4'},
                {'label':"6. Probability of winning matches vs winning toss",'value':'v5'},
                 {'label':"7. Rate the Analysis app",'value':'v6'}
                  
         ],
         placeholder="Please choose an option",
         searchable=False,
         value='v'
         )
   ]),
         html.Br(),
         html.Label('Please select this dropdown only for option 5--(Luckiest venue for each team)'),
  html.Div([dcc.Dropdown(
              id='Teams',
              options=[{'label':'Chennai Super Kings','value':'Chennai Super Kings'},{'label':'Deccan Chargers','value':'Deccan Chargers'},
                       {'label':'Delhi Capitals','value':'Delhi Capitals'},{'label':'Delhi Daredevils','value':'Delhi Daredevils'},
                       {'label':'Gujarat Lions','value':'Gujarat Lions'},{'label':'Kings XI Punjab','value':'Kings XI Punjab'},
                       {'label':'Kochi Tuskers Kerala','value':'Kochi Tuskers Kerala'},{'label':'Kolkata Knight Riders','value':'Kolkata Knight Riders'},
                       {'label':'Mumbai Indians','value':'Mumbai Indians'},{'label':'Pune Warriors','value':'Pune Warriors'},
                        {'label':'Rajasthan Royals','value':'Rajasthan Royals'},{'label':'Rising Pune Supergiants','value':'Rising Pune Supergiants'},
                       {'label':'Royal Challengers Bangalore','value':'Royal Challengers Bangalore'},
                       {'label':'Sunrisers Hyderabad','value':'Sunrisers Hyderabad'}
                       ],
                      placeholder="Please choose an option",
                      searchable=False,
                    value='Chennai Super Kings'
                  )
  ]),
      html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': 'Bar', 'value':1},{'label': 'Scatter', 'value':2},{'label': 'Pie', 'value':3},{'label': 'Sunburst', 'value':4}],
        value='Bar'
    ),
         dash.html.Div(id="graph_container")
                                      
])

@app.callback(
    Output("graph_container", "children"),
    [Input('FirstDropdown','value')],[Input('Teams','value')],[Input("selection", "value")],
)
def select_graph(value,value1,value2):
  if value=='v':
    encoded=dwnload(fig_stats)
    return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig_stats)
  if value=='v1':
    if value2==1:
          encoded=dwnload(fig11)
          return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig11)
    if value2==2:
          encoded=dwnload(fig12)
          return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig12)
    if value2==3:
          encoded=dwnload(fig13)
          return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig13)
    if value2==4:
          encoded=dwnload(fig14)
          return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig14)
  elif value=='v2':
    encoded=dwnload(fig21)
    return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig21)
  elif value=='v3':
    encoded=dwnload(fig32)
    return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig32)
  elif value=='v4':
    team=str(value1)
    fig=favorite(team)
    encoded=dwnload(fig)
    return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig)
  elif value=='v5':
    encoded=dwnload(fig_all)
    return html.A(
        html.Button(html.H2(children="Download Graph",
                            style={'background-color': '#4CAF50','width': '250px','border': '2px solid #4CAF50','color': 'white','padding': '10px 24px',
                                   'text-align': 'center','text-decoration': 'none','border-radius': '12px','font-size': '12px',})), id="download",
              href="data:text/html;base64," + encoded,download="IPL_stats(2008-2019).html"),dash.dcc.Graph(figure=fig_all)
  elif value=='v6':
    return html.H1(children='Please fill the Google Form below.......THANKYOU!!!!!',
           style={"textAlign": "center",
                  'color':'#19388A',
                  'background-color':'white',
                  'font-size':'200%'
                  }),html.Iframe(
            width="1000px",
            height="947px",
            src="https://docs.google.com/forms/d/e/1FAIpQLScdNtNMVIWqwddi3Q_1QvsP_qW-Pq8tamh4HzJphXYi-opwlQ/viewform?embedded=true",
        )



if __name__ == '__main__':
   app.run_server(debug=True)



