
#Calculate Probabilities based on outcome rather than fixed CPDs
def calculate_probabilities(user_inputs):
    home_advantage = user_inputs['Home_Advantage']
    home_form = user_inputs['HomeTeam_Form']
    away_form = user_inputs['AwayTeam_Form']
    home_rating = user_inputs['Home_Avg_Player_Rating']
    away_rating = user_inputs['Away_Avg_Player_Rating']
    log_home = user_inputs['Log_Position_Home']
    log_away = user_inputs['Log_Position_Away']
    head_to_head = user_inputs['Head_to_Head']


    # Baseline for Home Win
    prob_home = 0.33
    # Baseline for Draw
    prob_draw = 0.33
    # Baseline for Away Win
    prob_away = 0.33


     # If there's no home advantage adjust accordingly
    if home_form == 0:
        prob_home += 0.10  # No home team advantage and weak team form
    elif home_form == 2:
        prob_home -= 0.10

    # If Home advantage then adjust accordingly
    if home_advantage == 1:
        prob_home += 0.10  # Adjust more for home team
        prob_away -= 0.05
        prob_draw -= 0.05

    #If away team form is strong
    if away_form == 0:
        prob_away += 0.10
    elif away_form == 2:      #If away team form is weak
        prob_away -= 0.10

    # Comparing ratings for adjustments
    if home_rating < away_rating:
        prob_away += 0.10
        prob_home -= 0.05
        prob_draw -= 0.05
    elif home_rating > away_rating:
        prob_home += 0.10
        prob_away -= 0.05
        prob_draw -= 0.05

    # Log position
    if log_home < log_away:
        prob_home += 0.10
    elif log_home > log_away:
        prob_away += 0.10

    # Adjust for head to head

    # Home team dominates
    if head_to_head == 0: 
        prob_home += 0.15
    # Away team dominates
    elif head_to_head == 2: 
        prob_away += 0.15

    # Values between 0.01 and 0.98
    prob_home = max(min(prob_home, 0.98), 0.01)
    prob_away = max(min(prob_away, 0.98), 0.01)
    prob_draw = max(min(prob_draw, 0.98), 0.01)

    # Normalisation
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total

    return prob_home, prob_draw, prob_away


def get_user_input():
    print("Provide the following:")
    print()

    print("Head_to_Head (0 = Home Dominates, 1 = Balanced, 2 = Away Dominates):")
    head = int(input("Head_to_Head: "))

    print()
    print("Average Player Rating (0-10):")
    home_player_rating = float(input("Home_Avg_Player_Rating: "))
    away_player_rating = float(input("Away_Avg_Player_Rating: "))

    print()
    print("Home Advantage (1 = True, 0 = False):")
    advantage = int(input("Home_Advantage: "))

    print()
    print("Team Form (0 = Strong, 1 = Average, 2 = Weak):")
    home_form = int(input("HomeTeam_Form: "))
    away_form = int(input("AwayTeam_Form: "))

    
    print("Log Table Positions (1-20):")
    home_position = int(input("Home_Team_Position: "))
    away_position = int(input("Away_Team_Position: "))


    return {
        'Head_to_Head': head,
        'HomeTeam_Form': home_form,
        'AwayTeam_Form': away_form,
        'Home_Avg_Player_Rating': home_player_rating,
        'Away_Avg_Player_Rating': away_player_rating,
        'Log_Position_Home': home_position,
        'Log_Position_Away': away_position,
        'Home_Advantage': advantage
    }


def output_results(prob_home, prob_draw, prob_away):
    print("Predicted Outcome Probabilities:")
    print(f"HomeWin: {prob_home:.4f}")
    print(f"Draw: {prob_draw:.4f}")
    print(f"AwayWin: {prob_away:.4f}")

    print("Predicted Betting Odds:")
    for prob, label in zip([prob_home, prob_draw, prob_away], ['HomeWin', 'Draw', 'AwayWin']):
        if prob > 0:
            fractional_odds = round((1 / prob) - 1, 2)
            print(f"{label}: {fractional_odds}/1")
        else:
            print(f"{label}: Infinite (Probability Zero!)")


# Main program flow
user_evidence = get_user_input()
ph, pd, pa = calculate_probabilities(user_evidence)
output_results(ph, pd, pa)
