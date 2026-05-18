import requests
import pandas as pd

def fetch_nhl_rosters():
    # 1. Get the list of all teams and their IDs
    teams_url = "https://api-web.nhle.com/v1/standings/now"
    response = requests.get(teams_url).json()
    
    all_players = []
    
    # 2. Loop through every team in the league
    for team in response['standings']:
        team_abbr = team['teamAbbrev']['default']
        print(f"Fetching roster for {team_abbr}...")
        
        # 3. Get the roster for that specific team
        roster_url = f"https://api-web.nhle.com/v1/roster/{team_abbr}/current"
        roster_data = requests.get(roster_url).json()
        
        # 4. Parse Forwards, Defensemen, and Goalies
        for group in ['forwards', 'defensemen', 'goalies']:
            for p in roster_data.get(group, []):
                all_players.append({
                    "Player": f"{p['lastName']['default']}, {p['firstName']['default']}",
                    "Team": team_abbr,
                    "Position": p['positionCode'],
                    "Position_Group": "Offense" if p['positionCode'] in ['C', 'L', 'R'] else "Defense" if p['positionCode'] == 'D' else "Goalie",
                    "Player_ID": p['id']
                })
    
    return pd.DataFrame(all_players)

# Run and save
df = fetch_nhl_rosters()
df.to_csv("cleaned_players.csv", index=False)
print(f"✅ Successfully synced {len(df)} players to cleaned_players.csv")