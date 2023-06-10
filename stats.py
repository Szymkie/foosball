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
        winrate = round((wins_total/all_matches) * 100, 1)
        
    elif position == 'attack':
        
        wins_1 = len(df.loc[(df['Attack_1'] == name) & (df['Win'] == 1)])
        wins_2 = len(df.loc[(df['Attack_2'] == name) & (df['Win'] == 2)])
        wins_total = wins_1 + wins_2
        all_matches_attack = played(df, name, position = 'attack')
        winrate = round((wins_total/all_matches_attack) * 100, 1)
    
    elif position == 'defence':
        wins_1 = len(df.loc[(df['Defence_1'] == name) & (df['Win'] == 1)])
        wins_2 = len(df.loc[(df['Defence_2'] == name) & (df['Win'] == 2)])
        wins_total = wins_1 + wins_2
        all_matches_defence = played(df, name, position = 'defence')
        winrate = round((wins_total/all_matches_defence) * 100, 1)
    
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
        avg_goals = round((goals/matches), 1)
        
    elif position == 'attack':
        
        goals = goals_scored_total(df, name, position = 'attack')
        matches = played(df, name, position = 'attack')
        avg_goals = round((goals/matches), 1)
        
    elif position == 'defence':
        
        goals = goals_scored_total(df, name, position = 'defence')
        matches = played(df, name, position = 'defence')
        avg_goals = round((goals/matches), 1)
        
        
    return avg_goals

    
def goals_lost_avg(df, name, position = 'all'):
    
    ''' Calculating avg goals lost by player per match while on difftent position '''

    if position == 'all':
        
        goals = goals_lost_total(df, name, position = 'all')
        matches = played(df, name, position = 'all')
        avg_goals = round((goals/matches), 1)
        
    elif position == 'attack':
        
        goals = goals_lost_total(df, name, position = 'attack')
        matches = played(df, name, position = 'attack')
        avg_goals = round((goals/matches), 1)
        
    elif position == 'defence':
        
        goals = goals_lost_total(df, name, position = 'defence')
        matches = played(df, name, position = 'defence')
        avg_goals = round((goals/matches), 1)
        
        
    return avg_goals


def winrate_w_partner(df, name, name2, position = 'total'):
    

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
                
            winrate = round(((wins_total/played_all)*100), 1)
            
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
            
            winrate = round(((wins_total/played_all)*100), 1)
            
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
            
            winrate = round(((wins_total/played_all)*100), 1)
            
        except:
            
            winrate = 'Not enough data'
            
        
    return winrate


def num_played_with(df, name, name2):

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