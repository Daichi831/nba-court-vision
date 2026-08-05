# 設計書

## 技術スタック

| レイヤー | 技術 |
|----------|------|
| UI | Streamlit |
| 言語 | Python 3.9 |
| データ取得 | nba_api |
| データ処理 | pandas |

## データソース

`stats.nba.com`（非公式API）を `nba_api` ライブラリ経由で利用する。

**注意点：**
- 公式のレート制限ドキュメントは存在しない
- 短時間の大量リクエストで一時的にIPブロックされることがある
- 個人利用＋キャッシュありの構成であれば問題ない

## APIエンドポイント

| エンドポイント | 用途 | 主な引数 |
|---------------|------|---------|
| `commonteamroster` | チームのロースター取得 | `team_id`, `season` |
| `playercareerstats` | 選手のシーズン平均スタッツ | `player_id`, `per_mode36="PerGame"` |
| `playergamelog` | 選手のゲームログ | `player_id`, `season` |

## キャッシュ戦略

全APIコールに `@st.cache_data(ttl=86400)` を設定（24時間キャッシュ）。

- 同じ引数での再呼び出しはキャッシュから返す
- アプリ再起動でリセットされる
- シーズン中の日次更新に対応するためTTLを24時間に設定

## チームロゴ

NBA公式CDNからチームIDを使って取得する。

```
https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg
```
