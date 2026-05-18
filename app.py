import streamlit as st
import pandas as pd
import requests
import re

# --- 1. PAGE SETUP ---
st.set_page_config(
    page_title="NHL Front Office Dashboard 2026",
    page_icon="🏒",
    layout="wide"
)

CAP_CEILING_2026 = 104.0 
CAP_FLOOR_2026 = 76.9

# --- 2. TEAM MAPPING ---
TEAM_MAP = {
    "Anaheim Ducks": "ANA", "Boston Bruins": "BOS", "Buffalo Sabres": "BUF",
    "Calgary Flames": "CGY", "Carolina Hurricanes": "CAR", "Chicago Blackhawks": "CHI",
    "Colorado Avalanche": "COL", "Columbus Blue Jackets": "CBJ", "Dallas Stars": "DAL",
    "Detroit Red Wings": "DET", "Edmonton Oilers": "EDM", "Florida Panthers": "FLA",
    "Los Angeles Kings": "LAK", "Minnesota Wild": "MIN", "Montreal Canadiens": "MTL",
    "Nashville Predators": "NSH", "New Jersey Devils": "NJD", "New York Islanders": "NYI",
    "New York Rangers": "NYR", "Ottawa Senators": "OTT", "Philadelphia Flyers": "PHI",
    "Pittsburgh Penguins": "PIT", "San Jose Sharks": "SJS", "Seattle Kraken": "SEA",
    "St. Louis Blues": "STL", "Tampa Bay Lightning": "TBL", "Toronto Maple Leafs": "TOR",
    "Vancouver Canucks": "VAN", "Vegas Golden Knights": "VGK", "Washington Capitals": "WSH",
    "Winnipeg Jets": "WPG", "Utah Hockey Club": "UTA"
}

# --- 3. UTILITY: NAME NORMALIZATION ---
def normalize_name(name):
    """Removes special characters and extra spaces for better matching."""
    if not isinstance(name, str): return ""
    name = name.lower()
    name = re.sub(r'[^a-zA-Z\s]', '', name) # Remove accents/dots
    return " ".join(name.split())

# --- 4. DATA ENGINES ---

@st.cache_data(ttl=3600)
def fetch_api_rosters():
    roster_list = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        standings_url = "https://api-web.nhle.com/v1/standings/now"
        response = requests.get(standings_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            standings = response.json()
            for team in standings.get('standings', []):
                abbr = team['teamAbbrev']['default']
                roster_url = f"https://api-web.nhle.com/v1/roster/{abbr}/current"
                r_res = requests.get(roster_url, headers=headers, timeout=5)
                
                if r_res.status_code == 200:
                    data = r_res.json()
                    for group in ['forwards', 'defensemen', 'goalies']:
                        for p in data.get(group, []):
                            # API returns: "firstName", "lastName"
                            fname = p['firstName']['default']
                            lname = p['lastName']['default']
                            full_name = f"{fname} {lname}"
                            roster_list.append({
                                "Player": full_name,
                                "Match_Name": normalize_name(full_name),
                                "API_Team": abbr,
                                "API_Pos": p['positionCode']
                            })
        return pd.DataFrame(roster_list)
    except Exception:
        return pd.DataFrame()

@st.cache_data
def load_local_data():
    try:
        team_df = pd.read_csv("nhl_data.csv")
        salary_df = pd.read_csv("cleaned_players.csv")
        return team_df, salary_df
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

# --- 5. INITIALIZE DATA ---
df, salary_data = load_local_data()
api_rosters = fetch_api_rosters()

# --- 6. SIDEBAR ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/3/3a/05_NHL_Shield.svg", width=100)
st.sidebar.title("Front Office Controls")

if not df.empty:
    target_team = st.sidebar.selectbox("🔍 Select Franchise", df["Team"].unique())
    target_abbr = TEAM_MAP.get(target_team, "N/A")
else:
    target_team = "No Data"
    target_abbr = "N/A"

if st.sidebar.button("🔄 Force API Refresh"):
    st.cache_data.clear()
    st.rerun()

# --- 7. MAIN DASHBOARD ---
if not df.empty:
    team_stats = df[df["Team"] == target_team].iloc[0]
    st.title(f"🏒 {target_team} | Salary Cap Portal")
    
    # Header Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Projected Total Hit", f"${team_stats['Projected_Cap_Hit']}M")
    actual_space = round(CAP_CEILING_2026 - team_stats['Projected_Cap_Hit'], 2)
    m2.metric("Remaining Cap Space", f"${actual_space}M", 
              delta=f"{actual_space}M", delta_color="normal" if actual_space > 0 else "inverse")
    m3.metric("League Ceiling", f"${CAP_CEILING_2026}M")
    m4.metric("League Floor", f"${CAP_FLOOR_2026}M")

    st.markdown("---")

    # --- 8. CONTRACT REGISTRY (The Optimized Logic) ---
    st.header(f"📋 {target_team} Roster & Contracts")
    
    if not salary_data.empty:
        # Prepare salary data for merging
        salary_data['Match_Name'] = salary_data['Player'].apply(normalize_name)
        
        if not api_rosters.empty:
            # Join local salary data with API team data on the normalized Match_Name
            full_registry = pd.merge(salary_data, api_rosters[['Match_Name', 'API_Team']], on="Match_Name", how="left")
            
            # Filter for the selected team
            team_roster = full_registry[full_registry['API_Team'] == target_abbr]
            
            if team_roster.empty:
                st.warning(f"⚠️ Live Roster sync for {target_abbr} returned no matches. Showing entire salary registry instead.")
                st.dataframe(salary_data[['Player', 'Position', 'Cap_Hit']], use_container_width=True, hide_index=True)
            else:
                st.dataframe(
                    team_roster[['Player', 'Position', 'Cap_Hit']].style.format({"Cap_Hit": "${:,.0f}"}),
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.error("Could not reach NHL API. Check your connection.")
            st.dataframe(salary_data[['Player', 'Position', 'Cap_Hit']], use_container_width=True, hide_index=True)
    else:
        st.warning("Please run your parser script to generate cleaned_players.csv.")

    # --- 9. TRANSACTION SIMULATOR ---
    st.markdown("---")
    st.header("⚖️ Front Office War Room")
    sim1, sim2 = st.columns(2)
    with sim1:
        fa_name = st.text_input("Free Agent Name", placeholder="e.g. Connor McDavid")
        fa_aav = st.slider("Requested AAV ($M)", 0.8, 16.0, 8.0, step=0.25)
    with sim2:
        if st.button(f"Analyze {fa_name}"):
            if actual_space >= fa_aav:
                st.success(f"APPROVED: {fa_name} fits.")
                st.balloons()
            else:
                st.error(f"DENIED: Deficit of ${round(fa_aav - actual_space, 2)}M")

    # --- 10. LEAGUE CHART ---
    st.markdown("---")
    st.header("📊 League-Wide Spending")
    chart_data = df[['Team', 'Projected_Cap_Hit']].sort_values(by='Projected_Cap_Hit', ascending=False)
    st.bar_chart(chart_data.set_index('Team'))

else:
    st.warning("Ensure 'nhl_data.csv' is present.")