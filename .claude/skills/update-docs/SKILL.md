---
name: update-docs
description: docs/spec.md・docs/design.md・CLAUDE.mdのArchitectureセクションを、mainとのgit diffに基づき最新のコードに合わせて更新する。app.pyの画面構成・表示項目・シーズン設定・技術スタック・データソース・APIエンドポイント・キャッシュ戦略・チームロゴ取得方法などに影響する変更を行った後、PR作成前や、ユーザーがdocs同期を依頼したときに使う。
---

# docs更新

`docs/spec.md`・`docs/design.md`・`CLAUDE.md` の `## Architecture` セクションを、実際のコードの変更内容と一致させる。

## 手順

1. **差分の取得**
   - 現在のブランチが `main` でなければ `git diff main...HEAD` でコード変更を確認する。
   - `main` ブランチ上であれば `git status` と `git diff` で未コミットの変更を確認する。
   - 差分がなければ「docs更新は不要」と報告して終了する。

2. **影響範囲の判定**
   変更内容が以下のどれに該当するか判定する。複数該当してもよい。
   - `docs/spec.md` 対象：画面フロー、表示項目（平均スタッツ／ゲームログの列）、シーズン設定（`CURRENT_SEASON`）
   - `docs/design.md` 対象：技術スタック、データソース、APIエンドポイント（`nba_api` の呼び出し）、キャッシュ戦略（`@st.cache_data`）、チームロゴ取得方法
   - `CLAUDE.md` の `## Architecture` 対象：データフローの一行要約（`stats.nba.com` → `nba_api` → cache → UI）

   どれにも該当しない変更（typo修正やdocs以外の設定ファイル変更など）であれば、何もせず「docs更新は不要」と報告して終了する。

3. **更新**
   - 該当するファイルを読み込んでから、既存の見出し構成・表形式・日本語の文体（簡潔な体言止め/常体）を保ったまま該当箇所だけを書き換える。
   - 新規セクションの追加は、変更内容が既存の見出しに収まらない場合のみ行う。

4. **報告**
   - 更新したファイルと変更点を簡潔に要約する。
   - 次のアクション（例：`git add docs/ CLAUDE.md`、PR作成前なら `/code-review` の実行）を提案する。
