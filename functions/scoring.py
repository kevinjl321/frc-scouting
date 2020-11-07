import pandas as pd
from functions.sheets import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '12PwDvuHqI2fhktM3IN_7hZs7lZmwWKz2vihlS1Evt9A'
RANGE_NAME = 'B1:AL668'

pd.set_option('display.max_rows', None)
data = pull_sheet_data(SCOPES,SPREADSHEET_ID,RANGE_NAME)
df = pd.DataFrame(data[1:], columns=data[0])

# Calculate the average score of a specified team
# Parameter team_num: the team number of the team to find the avg score of
def avg_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    total_score = 0

    for i in teamdf.index:

        # Hab Line Cross
        if teamdf['Hab Line 1/0'][i] == 1:
            startpos = teamdf['Starting Position'][i]
            if startpos == 'L1' or startpos == 'M' or startpos == 'R1':
                total_score += 3
            elif startpos == 'L2' or startpos == 'R2':
                total_score += 6

        # Hatch Panels
        total_score += 2 * (teamdf['Auto # H Ship Side'][i] + teamdf['Auto # H Ship Front'][i] +
                        teamdf['Tele H Ship'][i] + teamdf['Tele Rocket H L1'][i] + teamdf['Tele Rocket H L2'][i] +
                        teamdf['Tele Rocket H L3'][i])

        if teamdf['Auto H Rkt Lvl'][i] > 0:
            total_score += 2

        if teamdf['Auto H Rkt Lvl [2]'][i] > 0:
            total_score += 2

        # Cargo
        total_score += 3 * (teamdf['Auto # C Ship Side'][i] + teamdf['Tele C Ship'][i] + teamdf['Tele Rocket C L1'][i] +
                        teamdf['Tele Rocket C L2'][i] + teamdf['Tele Rocket C L3'][i])

        if teamdf['Auto C Rkt Lvl'][i] > 0:
            total_score += 3

        # Fouls
        if teamdf['Fouls? 0/1'][i] == 1:
            total_score -= 7

        # Hab Climb Bonus
        level = teamdf['Highest success'][i]
        if level == 1:
            total_score += 3
        elif level == 2:
            total_score += 6
        elif level == 3:
            total_score += 12

    return total_score / len(teamdf.index)

# Calculate a team's average score achieved during sandstorm
# Parameter team_num: the team number of the team to find the avg sandstorm score of

def sandstorm_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    total_score = 0

    for i in teamdf.index:

        # Hab Line Cross
        if teamdf['Hab Line 1/0'][i] == 1:
            startpos = teamdf['Starting Position'][i]
            if startpos == 'L1' or startpos == 'M' or startpos == 'R1':
                total_score += 3
            elif startpos == 'L2' or startpos == 'R2':
                total_score += 6

        # Hatch Panels
        total_score += 2 * (teamdf['Auto # H Ship Side'][i] + teamdf['Auto # H Ship Front'][i])

        if teamdf['Auto H Rkt Lvl'][i] > 0:
            total_score += 2

        if teamdf['Auto H Rkt Lvl [2]'][i] > 0:
            total_score += 2

        # Cargo
        total_score += 3 * (teamdf['Auto # C Ship Side'][i])

        if teamdf['Auto C Rkt Lvl'][i] > 0:
            total_score += 3

    return total_score / len(teamdf.index)

# Calculate a team's average score achieved during teleop
# Parameter team_num: team number

def teleop_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    total_score = 0

    for i in teamdf.index:

        # Hatch Panels
        total_score += 2 * (teamdf['Tele H Ship'][i] + teamdf['Tele Rocket H L1'][i] + teamdf['Tele Rocket H L2'][i] +
                            teamdf['Tele Rocket H L3'][i])

        # Cargo
        total_score += 3 * (teamdf['Tele C Ship'][i] + teamdf['Tele Rocket C L1'][i] + teamdf['Tele Rocket C L2'][i] +
                            teamdf['Tele Rocket C L3'][i])

        # Fouls
        if teamdf['Fouls? 0/1'][i] == 1:
            total_score -= 7

    return total_score / len(teamdf.index)

# Calculate a specified team's defense capability
# Parameter team_num: the team number of the team to find the defense capability of
# Remove this function? See 2 functions below -->
def defense_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    defense_score = 0

    for i in teamdf.index:
        defense_score += teamdf['Def pl amt'][i] + teamdf['Def pl quality'][i]

    return defense_score / len(teamdf.index)

# Determine the average amount of defense played by a specified team:

def defense_amount(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    defense_amount = 0

    for i in teamdf.index:
        defense_amount += teamdf['Def pl amt'][i]

    return defense_amount / len(teamdf.index)

# Calculate the average quality of defense played of a specified team:

def defense_quality(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    total_quality = 0

    for i in teamdf.index:
        total_quality += teamdf['Def pl quality'][i]

    return total_quality / len(teamdf.index)

# Determine how often a specified team's bot dies

def dead_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    dead_score = 0

    for i in teamdf.index:
        if teamdf['Dead 0-3'][i] == 1:
            dead_score += 2
        elif teamdf['Dead 0-3'][i] == 2:
            dead_score += 7
        elif teamdf['Dead 0-3'][i] == 3:
            dead_score += 15

    return dead_score / len(teamdf.index)

def view_dashboard(team_num):
        output = 'Team ' + str(team_num) + ' Stats:\n'

        # Average Score
        output += '\n\tAverage Score: ' + str(avg_score(team_num)) + ' points\n'

        # Average Score during Auto
        output += '\n\tAverage Score During Auto: ' + str(sandstorm_score(team_num))+ ' points\n'

        # Average Score during Teleop
        output += '\n\tAverage Score During Teleop: ' + str(teleop_score(team_num))+ ' points\n'

        # Defense Amount
        output += '\n\tDefense Amount: '+ str(defense_amount(team_num)) + '\n'

        # Defense Quality
        dq = defense_quality(team_num)
        output += '\n\tDefense Quality: '

        if dq >= 4:
            output += 'Flawless\n'
        elif dq >= 3:
            output += 'Excellent\n'
        elif dq >= 2:
            output += 'Average\n'
        elif dq >= 1:
            output += 'Bad\n'
        elif dq >= 0:
            output += 'Non-existent\n'

        # Dead Amount
        output += '\n\tAmount of time dead: '+ str(dead_score(team_num)) + '\n'

        print(output)

def choose_members():

    #initialize code, read in team number column only
    team_df = df['Team Number']
    team_df = team_df.drop_duplicates()
    pd.set_option('display.max_rows', None)

    team_scores = []
    team_sandstorm = []
    team_teleop = []
    team_defense_scores = []
    team_defense_amount = []
    team_defense_quality = []
    team_dead_scores = []

    team_df.dropna(inplace = True)

    # get average score of all teams
    for i in team_df.index:
        avg = avg_score(team_df[i])
        team_scores.append(avg)

        sandstorm = sandstorm_score(team_df[i])
        team_sandstorm.append(sandstorm)

        teleop = teleop_score(team_df[i])
        team_teleop.append(teleop)

        ds = defense_score(team_df[i])
        team_defense_scores.append(ds)

        da = defense_amount(team_df[i])
        team_defense_amount.append(da)

        dq = defense_score(team_df[i])
        team_defense_quality.append(dq)

        dsc = dead_score(team_df[i])
        team_dead_scores.append(dsc)

    # data frame
    d = {'Team Number': team_df, 'Average Scores': team_scores}
    d1 = {'Team Number': team_df, 'Sandstorm Scores': team_sandstorm}
    d2 = {'Team Number': team_df, 'Teleop Scores': team_teleop}
    d3 = {'Team Number': team_df, 'Defense Scores': team_defense_scores}
    d4 = {'Team Number': team_df, 'Defense Amount': team_defense_amount}
    d5 = {'Team Number': team_df, 'Defense Quality': team_defense_quality}
    d6 = {'Team Number': team_df, 'Dead Scores': team_dead_scores}

    df2 = pd.DataFrame(data = d)
    df3 = pd.DataFrame(data = d1)
    df4 = pd.DataFrame(data = d2)
    df5 = pd.DataFrame(data = d3)
    df6 = pd.DataFrame(data = d4)
    df7 = pd.DataFrame(data = d5)
    df8 = pd.DataFrame(data = d6)
    
    # natural sort using average team scores
    df2 = df2.sort_values(by=['Average Scores'])
    df3 = df3.sort_values(by=['Sandstorm Scores'])
    df4 = df4.sort_values(by=['Teleop Scores'])
    df5 = df5.sort_values(by=['Defense Scores'])
    df6 = df6.sort_values(by=['Defense Amount'])
    df7 = df7.sort_values(by=['Defense Quality'])
    df8 = df8.sort_values(by=['Dead Scores'])

    print(df2)
    print('\n')
    print(df3)
    print('\n')
    print(df4)
    print('\n')
    print(df5)
    print('\n')
    print(df6)
    print('\n')
    print(df7)
    print('\n')
    print(df8)
