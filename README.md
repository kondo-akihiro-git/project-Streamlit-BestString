# ガット管理アプリ（BestString）

## アプリ概要

このアプリは、テニス・バドミントンなどの**ストリング（ガット）管理・分析Webアプリ**です。  

ユーザーは自分のラケットやガットの使用履歴を記録し、  
切れるまでの日数・コスト・打感評価などをもとに、自分に合ったストリングを分析できます。

また、スクレイピング機能によりメーカーサイト（YONEXなど）からガット・ラケット情報を取得し、データベースに自動登録できます。

<br>

主な機能
- ユーザーごとのガット使用記録の管理
- ラケット・ストリングの登録・選択
- 使用期間・コスト・打感の記録
- ストリング分析（耐久・コスト・評価）
- テンション別・ストリング別の可視化グラフ
- スクレイピングによる製品データ収集
- Streamlit Community CloudによるWeb公開

---

## 主な画面

- `トップ画面` : ユーザーURL発行画面

<kbd><img alt="トップ画面" src="picture/ball.png" /></kbd>
</br></br>

- `ダッシュボード` : ガット使用履歴一覧（カード表示）

<kbd><img alt="ダッシュボード画面" src="picture/ball.png" /></kbd>
</br></br>

- `記録画面` : ガット使用情報の登録フォーム

<kbd><img alt="記録画面" src="picture/ball.png" /></kbd>
</br></br>

- `分析画面` : 耐久・コスト・打感の分析グラフ

<kbd><img alt="分析画面" src="picture/ball.png" /></kbd>
</br></br>

※画像は仮置き（`picture/ball.png`）を使用

---

## フォルダ構成

- `page/`
  - `top_page.py` : ユーザーURL発行画面
  - `dashboard_page.py` : 記録一覧（カードUI）
  - `record_page.py` : 記録登録画面
  - `analysis_page.py` : 分析画面

- `logic/`
  - `top_logic.py` : ユーザー作成・取得
  - `record_logic.py` : 記録登録ロジック
  - `dashboard_logic.py` : 表示・更新ロジック
  - `analysis_logic.py` : 分析ロジック（集計処理）

- `model/`
  - `model.py` : DBモデル（User / Racket / Strand / Record）
  - `init.py` : DB接続・Session管理

- `racket/`
  - `yonex/`
    - `scraper.py` : ラケット情報スクレイピング
    - `insert.py` : DB登録処理

- `strand/`
  - `yonex/`
    - `scraper.py` : ガット情報スクレイピング
    - `insert.py` : DB登録処理

- `routing/`
  - `routing.py` : 画面ルーティング（Streamlitナビゲーション）

- `word/`
  - UI文言・状態管理定数

- `style/`
  - UIスタイル定義（MUI用）

- `picture/`
  - 画像アセット

- `database/`
  - SQLiteデータベース（ローカル用）

- `run.py` : アプリ起動エントリポイント
- `requirements.txt` : 依存ライブラリ定義

---

## 主な技術要件

- Streamlit : フロントエンドWebアプリ
- Streamlit Elements : MUIベースUI構築
- SQLModel / SQLAlchemy : ORM（SQLite）
- SQLite : ローカルDB（Streamlit Cloudでは一時制限あり）
- Plotly / Altair : データ可視化
- BeautifulSoup / Requests : スクレイピング
- Python-dotenv : 環境変数管理

---

## デプロイ手順（Streamlit Community Cloud）

このアプリは **Streamlit Community Cloud** にデプロイしています。

手順は以下の通りです。

1. GitHubにリポジトリを作成しPush
2. `requirements.txt` を用意
3. `run.py` をエントリポイントにする
4. Streamlit Community Cloudにログイン  
   https://share.streamlit.io/
5. 「New app」を選択
6. GitHubリポジトリを接続
7. ブランチ（main）と `run.py` を指定
8. Deployを実行
9. URLが発行され公開完了

---

## 補足（重要な設計ポイント）

- ユーザーはURLトークンで識別（`?token=`方式）
- SessionStateでページ遷移制御
- スクレイピングデータはDBにマージ（重複排除あり）
- 分析は「break_dateあり」のデータのみ対象
- テンションは2刻みでビン分割して集計