# CLAUDE.md

## Commands

```bash
# 依存インストール
pip3 install -r requirements.txt

# アプリ起動
streamlit run app.py
```

## Architecture

単一ファイル構成（`app.py`）の Streamlit アプリ。データベースなし。

**データフロー：**
`stats.nba.com`（非公式API）→ `nba_api` ライブラリ → `@st.cache_data(ttl=86400)` → Streamlit UI

**画面構成：**
- サイドバー：チーム選択（ドロップダウン）→ チームロゴ表示 → 選手選択（ラジオボタン）
- メインエリア：今シーズン平均スタッツ（メトリクス横並び）→ ゲームログ（データフレーム）

**APIエンドポイントと用途：**
- `commonteamroster` — チームのロースター取得
- `playercareerstats` — 選手のシーズン平均スタッツ（`per_mode36="PerGame"`）
- `playergamelog` — 選手のゲームログ

**キャッシュ戦略：**
全APIコールに `ttl=86400`（24時間）を設定。同一引数での再呼び出しはキャッシュから返す。アプリ再起動でリセット。

**定数：**
- `CURRENT_SEASON` — シーズンを変更する際はここだけ更新する（例: `"2025-26"`）

## NBA API の注意点

`stats.nba.com` は非公式APIのため、短時間の大量リクエストでIPブロックされることがある。個人利用＋キャッシュありの現構成では問題ない。チームロゴは `https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg` から取得。
