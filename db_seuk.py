import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
import warnings
import plotly.graph_objects as go
import joblib
from datetime import datetime
import sklearn

pd.options.mode.chained_assignment = None

from stats import win_rate, count, played, goals_scored_total, goals_scored_avg, goals_lost_total, goals_lost_avg, winrate_w_partner, num_played_with, rankings, all_unique, model_preprocessing

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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["General Info", "Personal Statistics", "Cooperational Analysis", "Predictive Modeling", "Matches to be played"])

with tab1:
    
    st.header('General info 📈')    

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
        
    st.header("Rankings")
    
    kpis = ['Winrate total', 
            'Winrate on attack', 
            'Winrate on defence', 
            'Played total', 
            'Played on attack', 
            'Played on defence', 
            'Avg goals scored while on attack', 
            'Avg goals scored while on defence', 
            'Avg goals lost while on defence', 
            'Avg goals lost while on attack']
    
    choosen_kpi = st.selectbox(label = 'Select the metric:', options = kpis)
    
    df_kpis = rankings(df = df, kpi = choosen_kpi)
    
    col1, col2 = st.columns([0.25, 0.75], gap = 'large')
    
    with col1:
        
        st.table(df_kpis)
        
    with col2:
        st.header(f"Top 3 players in {choosen_kpi} metric")
        
        col1, col2, col3, col4, col5 = st.columns([0.2, 0.2, 0.2, 0.2, 0.2], gap = 'large')
        
        with col1:
            st.subheader(f'{df_kpis.iloc[0, 0]}🏆')
            st.write(f'with score of {df_kpis.iloc[0,1]}')
            
        with col2:
            st.subheader(f'{df_kpis.iloc[1, 0]}🥈')
            st.write(f'with score of {df_kpis.iloc[1,1]}')
            
        with col3:   
            st.subheader(f'{df_kpis.iloc[2, 0]}🥉')
            st.write(f'with score of {df_kpis.iloc[2,1]}')


with tab2: 
    
    st.header('Personal statistics 🙋‍♂️')    

    name = st.selectbox(label = "Choose the player", options = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2']].values))

    image = Image.open(f'data/players/{name}.JPEG')

    col1, col2, col3 = st.columns([0.2, 0.2, 0.5], gap = 'large')

    with col1:

        st.image(image, caption = name)
    
    with col2:
        
        position = st.radio(label = 'Choose the position', options = ['All', 'Attack', 'Defence'], horizontal = True)
        
        position_arg = position.lower()
        
        gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = win_rate(df, name, position = position_arg),
        domain = {'x': [0, 1], 'y': [0, 1]},
        number = {'suffix': "%"},
        title = {'text': f"Winrate<br>({position})"}))
        
        
        cond_color = win_rate(df, name, position = position_arg)
            
        if (cond_color <= 35):
            gauge.update_traces(gauge_bar_color = 'red')
            
        elif (cond_color >= 35) & (cond_color < 50):
            gauge.update_traces(gauge_bar_color = 'yellow') 
            
        elif (cond_color >= 50) & (cond_color < 65):
            gauge.update_traces(gauge_bar_color = 'forestgreen')    
            
        elif (cond_color >= 65) & (cond_color < 75):
            gauge.update_traces(gauge_bar_color = 'darkgreen')
            
        elif (cond_color >= 75):
            gauge.update_traces(gauge_bar_color = 'turquoise')
            
        gauge.update_traces(gauge_axis_range=[0,100], selector=dict(type='indicator'))
        
        st.plotly_chart(gauge, use_container_width=True, use_container_highth=True)
        
    with col3:
        
        players = list(np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2']].values))
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
        
        fig_2.update_layout(title=dict(font=dict(size=35), 
                                       automargin=True), 
                            showlegend=False, 
                            title_font_family="sans-serif")
        
        fig_2.update_traces(textposition = 'bottom center', 
                            textfont_size=15)
        
        st.plotly_chart(fig_2, use_container_width=True)
   

    st.header('Goals statistics')
    col1, col2, col3 = st.columns(3)
        
        
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
        
        
    with col3:
        
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
    
    st.header('Cooperational analysis 🧑‍🤝‍🧑')    

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
        
        
        st.subheader('Nemesis system in development')
        
with tab4:
    st.header("Predictive Modeling 🤖")
    st.write('')
    col1, col2 = st.columns(2)
    
    with col2:
        st.write("""Choose you squad for virtual game, to predict outcome
        \n (You need to choose 4 diffrent players)""")
        
        all_players_pred = list(df["Attack_1"].unique())
        
        st.subheader('Attack on 🟥 Team')
        a1 = st.selectbox(label = "Choose the Attack_1 player", 
                          options = all_players_pred, 
                          label_visibility="hidden")
        
        # all_players_pred = all_players_pred.remove(a1)
    
        st.subheader('Defence on 🟥 Team')
        d1 = st.selectbox(label = "Choose the Defence_1 player", 
                          options = all_players_pred, 
                          label_visibility="hidden")
        
        # all_players_pred = all_players_pred.remove(d1)
        
        st.subheader('Attack on 🟦 Team')
        a2 = st.selectbox(label = "Choose the Attack_2 player", 
                          options = all_players_pred, 
                          label_visibility="hidden")
        
        # all_players_pred = all_players_pred.remove(a2)
        
        st.subheader('Defence on 🟦 Team')
        d2 = st.selectbox(label = "Choose the Defence_2 player", 
                          options = all_players_pred, 
                          label_visibility="hidden")
        
        model_list = [a1, d1, a2, d2]
    
    with col1:
        
        try:
            assert(all_unique(model_list))
            
                        
#             data_model = {'Attack_1' : [a1], 
#                           'Defence_1' : [d1], 
#                           'Attack_2' : [a2], 
#                           'Defence_2' : [d2]}

#             model_df = pd.DataFrame.from_dict(data_model)
#             model_log = joblib.load('modeling/models/log_reg.plk')
#             score = model_preprocessing(df_data, model_df, model = model_log)
            
#             st.header(f"🟥 Team have {score}% chance of winning this match!")
#             st.subheader('Model metrics:')

#             st.write('''
#             Model used: Logistic Regression\n 
#             ROC AUC (train set): 0.84\n 
#             ROC AUC (test set): 0.72''')

        except:  
            st.header('You need to choose 4 diffrent players ❌')
            
        data_model = {'Attack_1' : [a1], 
                      'Defence_1' : [d1], 
                      'Attack_2' : [a2], 
                      'Defence_2' : [d2]}

        model_df = pd.DataFrame.from_dict(data_model)
        model_log = joblib.load('modeling/models/log_reg.plk')

        score = model_preprocessing(df_data, model_df, model = model_log)

        st.header(f"🟥 Team have {score}% chance of winning this match!")
        st.subheader('Model metrics:')

        st.write('''
        Model used: Logistic Regression\n 
        ROC AUC (train set): 0.84\n 
        ROC AUC (test set): 0.72''')

    
with tab5:
    st.subheader("In development")
    
    
    