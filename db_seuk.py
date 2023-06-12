import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
import warnings
import plotly.graph_objects as go

pd.options.mode.chained_assignment = None

from stats import win_rate, count, played, goals_scored_total, goals_scored_avg, goals_lost_total, goals_lost_avg, winrate_w_partner, num_played_with

st.set_page_config(
    page_title="Samsung Foosball",
    page_icon="⚽",
    layout="wide",
)

@st.cache_data
def load_data():
    df_1 = pd.read_excel('data/seuk_04.xlsx')
    df = df_1.drop('Date', axis = 1)
    return df

@st.cache_data
def load_data_data():
    df_data = pd.read_excel('data/seuk_04.xlsx')
    return df_data

df = load_data()
df_data = load_data_data()

grouped = df_data.groupby(['Date']).count()['Win']


st.title("SEUK Foosball KPI's")

tab1, tab2, tab3 = st.tabs(["General info", "Personal Statistics", "Cooperational Analysis"])

with tab1:
    
    st.header('General info')    

    col1, col2 = st.columns(2)
    fig_1 = px.line(x = grouped.index, 
            y = grouped.values,
            title='Matches played by dates', 
            labels={ "x": "Date",
                     "y": "Matches played"}, 
            markers = True, 
            height=450,
            width=800)

    fig_1.update_traces(marker=dict(size=12))
    fig_1.update_traces(line_color='#03ecfc', line_width=2, texttemplate="%{y}", textposition = 'top center')
    fig_1.update_yaxes(tick0=0)

    with col1: 
        st.plotly_chart(fig_1, use_container_width=True)

    with col2:
        st.metric(
            label="Total matches played ⚽",
            value=len(df))
        st.write('Last 5 matches')
        st.table(df.tail())

with tab2: 
    
    st.header('Individual statistics')    

    name = st.selectbox(label = "Choose the player", options = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values))

    image = Image.open(f'data/players/{name}.JPEG')

    col1, col2 = st.columns([0.3, 0.6], gap = 'large')

    with col1:

        st.image(image, caption = name)

    with col2:
        
        players = list(np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values))
        players.remove(name)
        
        win_total_attack = []
        win_total_defence = []
        played_w = []
        
        for ply in players:
            
            tmp1 = round(winrate_w_partner(df = df, name = name, name2 = ply, position = 'attack'), 1)
            tmp2 = round(winrate_w_partner(df = df, name = name, name2 = ply, position = 'defence'), 1)
            tmp3 = num_played_with(df = df, name = name, name2 = ply)
            win_total_attack.append(tmp1)
            win_total_defence.append(tmp2)
            played_w.append(tmp3)
        
        
        data_plot = pd.DataFrame({'name' : players,
                                'winrate_attack' : win_total_attack, 
                                'winrate_defence' : win_total_defence,
                                'played' : played_w}
                                )
        
        fig_2 = px.scatter(data_frame = data_plot, 
                           x = 'winrate_attack', 
                           y = 'winrate_defence', 
                           title='Teammates analysis', 
                           text = 'name', 
                           size = 'played', color = 'name', 
                           labels = {'played' : "Number of games together", 
                                     'winrate_attack' : f'Winrate ({name} on attack)', 
                                     'name' : 'Teammate', 
                                     'winrate_defence' : f'Winrate ({name} on defence)'}
                            )
        
        fig_2.update_layout(title=dict(font=dict(size=40), automargin=True), showlegend=False)
        fig_2.update_traces(textposition = 'bottom center', textfont_size=15)
        
        
        
        st.plotly_chart(fig_2, use_container_width=True)
        
    col1, col2, col3, col4 = st.columns(4)
        
        
    with col1:
        
        st.subheader('Games played')
            
        st.metric(
            label="Total games",
            value= played(df, name, position = 'all') 
        )
        st.metric(
            label="Games on attack",
            value= played(df, name, position = 'attack') 
        )
        st.metric(
            label="Games on defence",
            value= played(df, name, position = 'defence') 
        )
        
        
    with col2:

        st.subheader('Win rates')
        
        st.metric(
            label= f"Win Rate (all games)",
            value= win_rate(df, name, position = 'all') 
        )
        
        st.metric(
            label="Win Rate (played on attack)",
            value=win_rate(df, name, position = 'attack')
        )


        st.metric(
            label="Win Rate (played on defence)",
            value=win_rate(df, name, position = 'defence')
        )
        
        
    with col3:

        st.subheader('Goals scored total')

        st.metric(
            label = f"Total goals scored while {name} in team",
            value = goals_scored_total(df, name, position = 'all') 
        )

        st.metric(
            label = f"Total goals scored while {name} on attack",
            value = goals_scored_total(df, name, position = 'attack')
        )


        st.metric(
            label = f"Total goals scored while {name} on defence",
            value = goals_scored_total(df, name, position = 'defence')
        )
        
        
    with col4:
        
        st.subheader('Goals average')

        st.metric(
            label = f"Goals scored on average while {name} on attack",
            value = goals_scored_avg(df, name, position = 'attack')
        )

        st.metric(
            label = f"Goals lost on average while {name} on defence",
            value = goals_lost_avg(df, name, position = 'defence')
        )
        
with tab3:
    
    st.header('Cooperational analysis')    

    col1, col2 = st.columns(2)

    with col1:
        name1 = st.selectbox(label = "Choose player one", options = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values), index = 1)

    with col2:
        name2 = st.selectbox(label = "Choose second player", options = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values), index = 3)


    if name1 == name2 :

        st.write('Choose two diffrent players!')

    else:

        total = winrate_w_partner(df = df, name = name1, name2 = name2, position = 'total')

        attack1 = winrate_w_partner(df = df, name = name1, name2 = name2, position = 'attack')

        defence1 = winrate_w_partner(df = df, name = name1, name2 = name2, position = 'defence')

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                label = f'Winrate (in total)', value = total
            )

        with c2:

            st.metric(
                label = f'Winrate \n ({name1} on Attack, {name2} on Defence)', value = attack1
            )

        with c3:

            st.metric(
                label = f'Winrate \n ({name2} on Attack, {name1} on Defence)', value = defence1
            )
        
        
        st.subheader('Nemesis system in progress')