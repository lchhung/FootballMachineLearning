import glob
import pandas as pd


def main():

    file_path = glob.glob('data/*csv')

    home_col = ['matchdate', 'teamId', 'playerId', 'OVA', 'POT', 'BOV', 'BP', 'GROWTH',
       'ATTACHING', 'CROSSING', 'FINISHING', 'HEADING_ACCURACY',
       'SHORT_PASSING', 'Volleys', 'TotalSkill', 'Dribbing', 'Curve',
       'FkAccuracy', 'LONG_PASSING', 'BallControl', 'TotalMovement',
       'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
       'TotalPower', 'ShotPower', 'Jumping', 'Stamina', 'Strength',
       'LongShots', 'TotalMentary', 'Aggression', 'Interceptions',
       'Positioning', 'Vision', 'Penalties', 'Composure', 'DEFENDING',
       'Marking', 'StandingStackle', 'SlidingTackle', 'GOALKEEPING',
       'GKDriving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes',
       'TotalStats', 'BaseStats', 'AttackingWorkRate', 'DefensiveWorkRate',
       'Pac', 'SHO', 'Pas', 'Dri', 'DEF', 'PHY']

    for file in file_path:
        home_df = pd.read_csv(file)
        print(home_df.columns)






if __name__ == "__main__":
    main()