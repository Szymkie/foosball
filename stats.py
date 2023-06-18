import numpy as np
import pandas as pd


def count(lst):
    return sum(bool(x) for x in lst)


def played(df, name, position = 'all'):
    
    '''Calculating all matches played by played'''
    
    if position == 'all':       
        played = len(df.loc[(df['Attack_1'] == name) | (df['Attack_2'] == name) | (df['Defence_1'] == name) | (df['Defence_2'] == name)])
        
    elif position == 'attack':
        played = len(df.loc[(df['Attack_1'] == name) | (df['Attack_2'] == name)])
    
    elif position == 'defence':
        played = len(df.loc[(df['Defence_1'] == name) | (df['Defence_2'] == name)])
        
    
    return played


def win_rate(df, name, position = 'all'):
    
    ''' Calculating players win rate '''
    
    if position == 'all':
        
        wins_1 = len(df.loc[((df['Attack_1'] == name) | (df['Defence_1'] == name)) & df['Win'] == 1])
        wins_2 = len(df.loc[(df['Win'] == 2) & ((df['Attack_2'] == name) | (df['Defence_2'] == name))])
        wins_total = wins_1 + wins_2
        all_matches = played(df, name, position = 'all')
        winrate = round((wins_total/all_matches) * 100, 2)
        
    elif position == 'attack':
        
        wins_1 = len(df.loc[(df['Attack_1'] == name) & (df['Win'] == 1)])
        wins_2 = len(df.loc[(df['Attack_2'] == name) & (df['Win'] == 2)])
        wins_total = wins_1 + wins_2
        all_matches_attack = played(df, name, position = 'attack')
        winrate = round((wins_total/all_matches_attack) * 100, 2)
    
    elif position == 'defence':
        wins_1 = len(df.loc[(df['Defence_1'] == name) & (df['Win'] == 1)])
        wins_2 = len(df.loc[(df['Defence_2'] == name) & (df['Win'] == 2)])
        wins_total = wins_1 + wins_2
        all_matches_defence = played(df, name, position = 'defence')
        winrate = round((wins_total/all_matches_defence) * 100, 2)
    
    return winrate


def goals_scored_total(df, name, position = 'all'):
    
    ''' Calculating total goals scored by player '''
    if position == 'all':

        goals_1 = df.loc[(df['Attack_1'] == name) | (df['Defence_1'] == name)]['G1'].sum()
        goals_2 = df.loc[(df['Attack_2'] == name) | (df['Defence_2'] == name)]['G2'].sum()
        goals_total = goals_1 + goals_2
    
    elif position == 'attack':
        
        goals_1 = df.loc[df['Attack_1'] == name]['G1'].sum()
        goals_2 = df.loc[df['Attack_2'] == name]['G2'].sum()
        goals_total = goals_1 + goals_2
        
    elif position == 'defence':
        
        goals_1 = df.loc[df['Defence_1'] == name]['G1'].sum()
        goals_2 = df.loc[df['Defence_2'] == name]['G2'].sum()
        goals_total = goals_1 + goals_2
              
        
    return goals_total


def goals_lost_total(df, name, position = 'all'):
    
    ''' Calculating total goals lost by player '''
    if position == 'all':

        goals_1 = df.loc[(df['Attack_1'] == name) | (df['Defence_1'] == name)]['G2'].sum()
        goals_2 = df.loc[(df['Attack_2'] == name) | (df['Defence_2'] == name)]['G1'].sum()
        goals_total = goals_1 + goals_2
    
    elif position == 'attack':
        
        goals_1 = df.loc[df['Attack_1'] == name]['G2'].sum()
        goals_2 = df.loc[df['Attack_2'] == name]['G1'].sum()
        goals_total = goals_1 + goals_2
        
    elif position == 'defence':
        
        goals_1 = df.loc[df['Defence_1'] == name]['G2'].sum()
        goals_2 = df.loc[df['Defence_2'] == name]['G1'].sum()
        goals_total = goals_1 + goals_2
              
        
    return goals_total

def goals_scored_avg(df, name, position = 'all'):
    
    ''' Calculating avg goals scored by player per match while on diffrent position '''

    if position == 'all':
        
        goals = goals_scored_total(df, name, position = 'all')
        matches = played(df, name, position = 'all')
        avg_goals = round((goals/matches), 2)
        
    elif position == 'attack':
        
        goals = goals_scored_total(df, name, position = 'attack')
        matches = played(df, name, position = 'attack')
        avg_goals = round((goals/matches), 2)
        
    elif position == 'defence':
        
        goals = goals_scored_total(df, name, position = 'defence')
        matches = played(df, name, position = 'defence')
        avg_goals = round((goals/matches), 2)
        
        
    return avg_goals

    
def goals_lost_avg(df, name, position = 'all'):
    
    ''' Calculating avg goals lost by player per match while on difftent position '''

    if position == 'all':
        
        goals = goals_lost_total(df, name, position = 'all')
        matches = played(df, name, position = 'all')
        avg_goals = round((goals/matches), 2)
        
    elif position == 'attack':
        
        goals = goals_lost_total(df, name, position = 'attack')
        matches = played(df, name, position = 'attack')
        avg_goals = round((goals/matches), 2)
        
    elif position == 'defence':
        
        goals = goals_lost_total(df, name, position = 'defence')
        matches = played(df, name, position = 'defence')
        avg_goals = round((goals/matches), 2)
        
        
    return avg_goals


def winrate_w_partner(df, name, name2, position = 'total'):
    
    ''' Calculating winrate with teammate regarding positions played '''

    if position == 'total':

        played_1 = df.loc[((df['Attack_1'] == name) & 
                        (df['Defence_1'] == name2)) | 
                        ((df['Attack_1'] == name2) & 
                        (df['Defence_1'] == name))]

        played_2 = df.loc[((df['Attack_2'] == name) & 
                        (df['Defence_2'] == name2)) | 
                        ((df['Attack_2'] == name2) & 
                        (df['Defence_2'] == name))]

        wins_1 = played_1.loc[df['Win'] == 1]
        wins_2 = played_2.loc[df['Win'] == 2]

        played_all = len(played_1) + len(played_2)
        
        wins_total = len(wins_1) + len(wins_2)
        
        try:
                
            winrate = round(((wins_total/played_all)*100), 2)
            
        except:
            
            winrate = 'Not enough data'
        
        
    elif position == 'attack':

        played_1 = df.loc[((df['Attack_1'] == name) & 
                        (df['Defence_1'] == name2))]
        
        played_2 = df.loc[((df['Attack_2'] == name) & 
                        (df['Defence_2'] == name2))]
                       

        wins_1 = played_1.loc[df['Win'] == 1]
        wins_2 = played_2.loc[df['Win'] == 2]

        played_all = len(played_1) + len(played_2)
        
        wins_total = len(wins_1) + len(wins_2)
        
        try:
            
            winrate = round(((wins_total/played_all)*100), 2)
            
        except:
            
            winrate = 'Not enough data'
            
        
    elif position == 'defence':

        played_1 = df.loc[((df['Attack_1'] == name2) & 
                        (df['Defence_1'] == name))]
        
        played_2 = df.loc[((df['Attack_2'] == name2) & 
                        (df['Defence_2'] == name))]
                       

        wins_1 = played_1.loc[df['Win'] == 1]
        wins_2 = played_2.loc[df['Win'] == 2]

        played_all = len(played_1) + len(played_2)
        
        wins_total = len(wins_1) + len(wins_2)
        
        try:
            
            winrate = round(((wins_total/played_all)*100), 2)
            
        except:
            
            winrate = 'Not enough data'
            
        
    return winrate


def num_played_with(df, name, name2):
    
    '''Calculating numer of games played with teamate '''
    
    played_1 = df.loc[((df['Attack_1'] == name) & 
                    (df['Defence_1'] == name2)) | 
                    ((df['Attack_1'] == name2) & 
                    (df['Defence_1'] == name))]

    played_2 = df.loc[((df['Attack_2'] == name) & 
                    (df['Defence_2'] == name2)) | 
                    ((df['Attack_2'] == name2) & 
                    (df['Defence_2'] == name))]

    wins_1 = played_1.loc[df['Win'] == 1]
    wins_2 = played_2.loc[df['Win'] == 2]

    played_all = len(played_1) + len(played_2)
    
    return played_all


def rankings(df, kpi):
    
    """Creating DataFrame with player name and calculated metric
    
    params:
        df : pd.DataFrame - dataset with gathered scores from matches
        kpi : str - name of statistic to calculate
        
    return:
        df_kpi : pd.DataFrame - dataframe with player names and calculated statistics, adequate sorted
    
    """
    
    all_players = np.unique(df[['Attack_1', 'Defence_1','Attack_2' ,'Defence_2' ]].values)
    df_kpi = pd.DataFrame(columns = ['Player name', 'kpi'])
    
    if kpi == 'Winrate on attack':

        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(win_rate(df = df, name = name, position = 'attack'), 2)
        
    elif kpi == 'Winrate on defence':

        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(win_rate(df = df, name = name, position = 'defence'), 2)
        
    elif kpi == 'Winrate total':
    
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(win_rate(df = df, name = name, position = 'all'), 2)
        
    elif kpi == 'Played total':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = played(df, name, position = 'all')
            
    elif kpi == 'Played on attack':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = played(df, name, position = 'attack')
            
    elif kpi == 'Played on defence':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = played(df, name, position = 'defence')
        
    elif kpi == 'Avg goals scored while on attack':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(goals_scored_avg(df, name, position = 'attack'), 2)
            
    elif kpi == 'Avg goals scored while on defence':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(goals_scored_avg(df, name, position = 'defence'), 2)
            
    elif kpi == 'Avg goals lost while on defence':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(goals_lost_avg(df, name, position = 'defence'), 2)
            
    elif kpi == 'Avg goals lost while on attack':
        
        for idx, name in enumerate(all_players):
            df_kpi.loc[idx, 'Player name'] = name
            df_kpi.loc[idx, 'kpi'] = round(goals_lost_avg(df, name, position = 'attack'), 2)
            
    if (kpi == 'Avg goals lost while on defence') | (kpi == 'Avg goals lost while on attack'):
        df_kpi.sort_values('kpi', inplace = True, ascending  = True)
    else:
        df_kpi.sort_values('kpi', inplace = True, ascending  = False)
        
    df_kpi.reset_index(drop = True, inplace = True)
    df_kpi.index += 1 
    df_kpi  = df_kpi.index.name = 'Rank'
    df_kpi.rename(columns = {'kpi' : kpi}, inplace = True)
    
    
    return df_kpi