import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

pd.options.mode.chained_assignment = None

import warnings

from stats import win_rate, count, played, goals_scored_total, goals_scored_avg, goals_lost_total, goals_lost_avg

@st.experimental_memo
def load_data():
    df_1 = pd.read_excel('data/seuk_04.xlsx')
    df = df_1.drop('Date', axis = 1)
    return df

@st.experimental_memo
def load_data_data():
    df_data = pd.read_excel('data/seuk_04.xlsx')
    return df_data

st.set_page_config(
    page_title="Samsung Foosball",
    page_icon="✅",
    layout="wide",
)

df = load_data()
df_data = load_data_data()

grouped = df_data.groupby(['Date']).count()['Win']

st.title("SEUK Foosball KPI's")


col1, col2 = st.columns(2)
fig_1 = px.line(x = grouped.index, 
        y = grouped.values,
        title='Matches played by dates', 
        labels={ "x": "Date",
                 "y": "Matches played"}, 
        markers = True, 
        height=450,
        width=800)
fig_1.update_traces(line_color='#03ecfc', line_width=2, texttemplate="%{y}")
fig_1.update_yaxes(tick0=0)

with col1: 
    st.plotly_chart(fig_1, use_container_width=True)
    
with col2:
    st.metric(
        label="Total matches played ⚽",
        value=len(df))
    st.write('Last 5 matches')
    st.table(df.tail())
    
name = st.selectbox(label = "Player name", options = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values))

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Matches played",
        value= played(df, name, position = 'all') 
    )
    
with col2:
    st.metric(
        label="Goals scored on average while player on attack",
        value=goals_scored_avg(df, name, position = 'attack')
    )
    
with col3:
    st.metric(
        label="Goals lost on average while player on defence",
        value=goals_lost_avg(df, name, position = 'defence')
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Win Rate (all games)",
        value= win_rate(df, name, position = 'all') 
    )
    
with col2:
    st.metric(
        label="Win Rate (played on attack)",
        value=win_rate(df, name, position = 'attack')
    )
    
with col3:
    st.metric(
        label="Win Rate (played on defence)",
        value=win_rate(df, name, position = 'defence')
    )