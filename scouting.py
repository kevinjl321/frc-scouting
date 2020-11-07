import pandas as pd

pd.set_option('display.max_rows', None, 'display.max_columns', None)

df = pd.read_csv('data/2791_2019dar.csv')

# Display a list of the teams present in the data

team_nums = df['Team Number']
team_nums = team_nums.drop_duplicates()

print('Available Teams:')
print(team_nums.to_string(index=False))

# Calculate the average score of a specified team
# Parameter team_num: team number

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
# Parameter team_num: team number

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

        # Hab Climb Bonus
        level = teamdf['Highest success'][i]
        if level == 1:
            total_score += 3
        elif level == 2:
            total_score += 6
        elif level == 3:
            total_score += 12

    return total_score / len(teamdf.index)

# Determine the average amount of defense played by a specified team

def defense_amount(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    defense_amount = 0

    for i in teamdf.index:
        defense_amount += teamdf['Def pl amt'][i]

    return defense_amount / len(teamdf.index)

# Calculate the average quality of defense played of a specified team

def defense_quality(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    total_quality = 0
    counter = 0

    for i in teamdf.index:
        if teamdf['Def pl quality'][i] > 0:
            total_quality += teamdf['Def pl quality'][i]
            counter += 1
    
    if counter == 0:
        return 0
    else:
        return total_quality / counter

# Determine how often a specified team's bot dies

def dead_score(team_num):

    # Creates a new dataframe containing only data for team team_num
    teamdf = df[df['Team Number'] == team_num]

    dead_score = 0

    for i in teamdf.index:

        dead_value = teamdf['Dead 0-3'][i]
        
        if dead_value == 1:
            dead_score += 2
        elif dead_value == 2:
            dead_score += 7
        elif dead_value == 3:
            dead_score += 15

    return dead_score / len(teamdf.index)

def view_dashboard(team_num):
        output = '\nTeam ' + str(team_num) + ' Stats:\n'

        # Average Score
        output += '\n\tAverage Score: ' + str(avg_score(team_num)) + ' points\n'

        # Average Score during Sandstorm
        output += '\n\tAverage Score During Sandstorm: ' + str(sandstorm_score(team_num))+ ' points\n'

        # Average Score during Teleop
        output += '\n\tAverage Score During Teleop: ' + str(teleop_score(team_num))+ ' points\n'

        # Defense Amount
        output += '\n\tDefense Amount: '+ str(defense_amount(team_num)) + '\n'

        # Defense Quality
        dq = defense_quality(team_num)
        output += '\n\tDefense Quality: '

        if dq == 4:
            output += 'Flawless, ' + str(dq) + '\n'
        elif dq >= 3:
            output += 'Excellent, ' + str(dq) + '\n'
        elif dq >= 2:
            output += 'Decent, ' + str(dq) + '\n'
        elif dq >= 1:
            output += 'Poor, ' + str(dq) + '\n'
        elif dq > 0:
            output += 'Terrible, ' + str(dq) + '\n'
        elif dq == 0:
            output += 'Never played defense\n'

        # Dead Score
        output += '\n\tDead Score: '+ str(dead_score(team_num))+ '\n'

        print('________________________________________________________________________\n'
              + output +
              '________________________________________________________________________\n')

def choose_members():

    # Lists to contain the stats for all teams
    scores = []
    sandstorm_scores = []
    teleop_scores = []
    defense_amounts = []
    defense_qualities = []
    dead_scores = []

    # team_nums is a existing Series containing team numbers

    for i in team_nums.index:

        scores.append(avg_score(team_nums[i]))
        sandstorm_scores.append(sandstorm_score(team_nums[i]))
        teleop_scores.append(teleop_score(team_nums[i]))
        defense_amounts.append(defense_amount(team_nums[i]))
        defense_qualities.append(defense_quality(team_nums[i]))
        dead_scores.append(dead_score(team_nums[i]))

    df1 = pd.DataFrame({'Team Number': team_nums, 'Average Score': scores})
    df2 = pd.DataFrame({'Team Number': team_nums, 'Sandstorm Score': sandstorm_scores})
    df3 = pd.DataFrame({'Team Number': team_nums, 'Teleop Score': teleop_scores})
    df4 = pd.DataFrame({'Team Number': team_nums, 'Defense Amount': defense_amounts})
    df5 = pd.DataFrame({'Team Number': team_nums, 'Defense Quality': defense_qualities})
    df6 = pd.DataFrame({'Team Number': team_nums, 'Dead Score': dead_scores})

    # Sort the dataframes
    df1 = df1.sort_values(by=['Average Score'], ascending=False)
    df2 = df2.sort_values(by=['Sandstorm Score'], ascending=False)
    df3 = df3.sort_values(by=['Teleop Score'], ascending=False)
    df4 = df4.sort_values(by=['Defense Amount'], ascending=False)
    df5 = df5.sort_values(by=['Defense Quality'], ascending=False)
    df6 = df6.sort_values(by=['Dead Score'], ascending=False)
    
    print('________________________________________________________________________\n')
    print(df1.head(10).to_string(index=False))
    print('________________________________________________________________________\n')
    print(df2.head(10).to_string(index=False))
    print('________________________________________________________________________\n')
    print(df3.head(10).to_string(index=False))
    print('________________________________________________________________________\n')
    print(df4.head(10).to_string(index=False))
    print('________________________________________________________________________\n')
    print(df5.head(10).to_string(index=False))
    print('________________________________________________________________________\n')
    print(df6.head(10).to_string(index=False))
    print('________________________________________________________________________\n')

# UI
print('________________________________________________________________________\n')

while True:
    choice = int(input("1 - View analytics dashboard for a specified team. \n"
                       "2 - View sorted lists of teams to assist in choosing alliance members. \n"
                       "3 - Exit the program. \n\n"
                       "Enter '1', '2', or '3' to select an option: "))

    if choice == 1:
        team_input = int(input('\nEnter the team number of the team you wish to analyze: '))
        while True:
            team_df = df[df['Team Number'] == team_input]
            if len(team_df.index) == 0:
                team_input = int(input('\nThe team number you have entered was not found in the database. Please enter a valid team number: '))
            else:
                break
        view_dashboard(team_input)
    elif choice == 2:
        choose_members()
    elif choice == 3:
        break
    else:
        print("________________________________________________________________________\n\n"
              "Please enter '1', '2', or '3'!\n")