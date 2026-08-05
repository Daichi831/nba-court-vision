# CLAUDE.md

## Git ワークフロー

修正・機能追加は必ず `main` を最新にしてからブランチを切って作業する。

```bash
git checkout main && git pull
git checkout -b feature/branch-name  # 新機能追加
git checkout -b fix/branch-name      # バグ修正
# 作業後
# PR作成前にコードレビューを実行する
git push -u origin feature/branch-name
```

PR作成前に必ず `/code-review` を実行してレビューを確認すること。

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

詳細は [`docs/spec.md`](docs/spec.md)（仕様）・[`docs/design.md`](docs/design.md)（設計）を参照。
