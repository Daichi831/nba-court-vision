import streamlit as st
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonteamroster, playercareerstats, playergamelog

st.set_page_config(page_title="NBA Court Vision", layout="wide")

CURRENT_SEASON = "2025-26"

all_teams = sorted(teams.get_teams(), key=lambda t: t["full_name"])
team_name_to_info = {t["full_name"]: t for t in all_teams}

# サイドバー：チーム選択
with st.sidebar:
    st.title("NBA Court Vision")
    selected_team_name = st.selectbox("チーム", list(team_name_to_info.keys()), label_visibility="collapsed")
    selected_team = team_name_to_info[selected_team_name]
    selected_team_id = selected_team["id"]

    st.image(
        f"https://cdn.nba.com/logos/nba/{selected_team_id}/global/L/logo.svg",
        width=160,
    )
    st.markdown(f"### {selected_team_name}")

    # ロースター取得
    @st.cache_data(ttl=86400, show_spinner=False)
    def get_roster(team_id):
        roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=CURRENT_SEASON)
        df = roster.get_data_frames()[0]
        return df[["PLAYER", "PLAYER_ID", "NUM", "POSITION", "HEIGHT", "WEIGHT", "BIRTH_DATE", "EXP"]]

    with st.spinner("ロースターを取得中..."):
        roster_df = get_roster(selected_team_id)

    player_options = dict(zip(roster_df["PLAYER"], roster_df["PLAYER_ID"]))
    st.markdown("**選手を選択**")
    selected_player_name = st.radio("選手", list(player_options.keys()), label_visibility="collapsed")
    selected_player_id = player_options[selected_player_name]

# メインエリア：スタッツ表示
@st.cache_data(ttl=86400, show_spinner=False)
def get_season_averages(player_id):
    career = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36="PerGame")
    df = career.get_data_frames()[0]
    return df[df["SEASON_ID"] == CURRENT_SEASON]

@st.cache_data(ttl=86400, show_spinner=False)
def get_game_log(player_id):
    log = playergamelog.PlayerGameLog(player_id=player_id, season=CURRENT_SEASON)
    df = log.get_data_frames()[0]
    df = df[["GAME_DATE", "MATCHUP", "WL", "MIN", "PTS", "REB", "OREB", "DREB", "AST", "BLK", "STL", "TOV", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT"]].copy()
    df["FG"] = df["FGM"].astype(int).astype(str) + "-" + df["FGA"].astype(int).astype(str) + " (" + (df["FG_PCT"] * 100).round(1).astype(str) + "%)"
    df["3P"] = df["FG3M"].astype(int).astype(str) + "-" + df["FG3A"].astype(int).astype(str) + " (" + (df["FG3_PCT"] * 100).round(1).astype(str) + "%)"
    df["FT"] = df["FTM"].astype(int).astype(str) + "-" + df["FTA"].astype(int).astype(str) + " (" + (df["FT_PCT"] * 100).round(1).astype(str) + "%)"
    return df[["GAME_DATE", "MATCHUP", "WL", "MIN", "PTS", "REB", "OREB", "DREB", "AST", "BLK", "STL", "TOV", "FG", "3P", "FT"]]

# 平均スタッツ
st.subheader(f"{selected_player_name} — 今シーズン平均（{CURRENT_SEASON}）")

with st.spinner("スタッツを取得中..."):
    avg_df = get_season_averages(selected_player_id)

if avg_df.empty:
    st.info("今シーズンのデータがありません")
else:
    row = avg_df.iloc[0]
    labels = ["得点", "リバウンド", "ORB", "DRB", "アシスト", "ブロック", "スティール", "ターンオーバー", "試合数"]
    keys   = ["PTS",  "REB",        "OREB", "DREB", "AST",  "BLK",    "STL",        "TOV",            "GP"]
    fmts   = [".1f",  ".1f",        ".1f",  ".1f",  ".1f",  ".1f",    ".1f",        ".1f",            "d"]
    cols = st.columns(len(labels))
    for col, label, key, fmt in zip(cols, labels, keys, fmts):
        value = int(row[key]) if fmt == "d" else float(row[key])
        col.metric(label=label, value=f"{value:{fmt}}")

st.divider()

# ゲームログ
st.subheader("ゲームログ")

with st.spinner("ゲームログを取得中..."):
    game_log_df = get_game_log(selected_player_id)

if game_log_df.empty:
    st.info("今シーズンのゲームログがありません")
else:
    st.dataframe(
        game_log_df.rename(columns={
            "GAME_DATE": "日付",
            "MATCHUP": "対戦",
            "WL": "勝敗",
            "MIN": "分",
            "PTS": "得点",
            "REB": "リバウンド",
            "OREB": "ORB",
            "DREB": "DRB",
            "AST": "アシスト",
            "BLK": "ブロック",
            "STL": "スティール",
            "TOV": "ターンオーバー",
        }),
        use_container_width=True,
        hide_index=True,
    )
