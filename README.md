# ストリング管理アプリ（BestString）

## アプリ概要

このアプリは、テニスの**ストリングを管理し、最適なストリングを分析する**Webアプリです。  
ユーザーは自分のラケットやガットの使用履歴を記録し、  
切れるまでの日数・コスト・打感評価などをもとに、自分に合ったストリングを分析できます。  
また、スクレイピング機能によりメーカーサイト（YONEXなど）からガット・ラケット情報を取得し、DBに自動登録します。

<br>

主な機能
- ユーザーごとのガット使用記録の管理
- ラケット・ストリングの登録・選択
- 使用期間・コスト・打感の記録
- ストリング分析（耐久・コスト・評価）
- テンション別・ストリング別の可視化グラフ
- スクレイピングによる製品データ収集


---

## 主な画面

- `トップ画面` : ユーザーURL発行画面

<kbd><img width="773" height="435" alt="top" src="https://github.com/user-attachments/assets/419eece5-7835-4b72-b938-50c216c64879" />
</kbd>
</br></br>

- `ダッシュボード` : ストリング使用履歴一覧

<kbd><img width="529" height="685" alt="dashboard" src="https://github.com/user-attachments/assets/d8e0e4b4-a689-45c3-9a89-53b77afa92b3" />
</kbd>
</br></br>

- `記録画面` : ガット使用情報の登録フォーム

<kbd><img width="537" height="772" alt="record" src="https://github.com/user-attachments/assets/cd6722cc-0381-4e78-bae3-681b366e4e4c" /></kbd>
</br></br>

- `分析画面` : 耐久・コスト・打感の分析グラフ

<kbd><img width="507" height="899" alt="ana" src="https://github.com/user-attachments/assets/015de5b2-b028-4117-ac0d-513db4770b8f" /></kbd>
</br></br>

---

## フォルダ構成

- `page/`
  - `top_page.py` : ユーザーURL発行画面
  - `dashboard_page.py` : ストリング記録一覧
  - `record_page.py` : ストリング記録登録画面
  - `analysis_page.py` : 分析画面
- `logic/`
  - `top_logic.py` : ユーザー作成・取得
  - `record_logic.py` : 記録登録ロジック
  - `dashboard_logic.py` : 表示・更新ロジック
  - `analysis_logic.py` : 分析ロジック
- `model/`
  - `model.py` : DBモデル
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
  - `routing.py` : 画面ルーティング
- `word/`
  - UI文言/状態管理定数
- `style/`
  - UIスタイル定義
- `picture/`
  - 画像アセット
- `database/`
  - SQLiteデータベース
- `run.py` : アプリ起動エントリポイント
- `requirements.txt` : 依存ライブラリ定義

---

## 主な技術要件

- Streamlit : フロントエンドWebアプリ
- Streamlit Elements : MUIベースのUI構築
- SQLAlchemy(SQLite) : ORM（SQLite）
- Plotly / Altair : データ可視化
- BeautifulSoup : スクレイピング

---

## デプロイ手順

このアプリは **Streamlit Community Cloud** にデプロイしています。

手順は以下の通りです。

1. GitHubにリポジトリを作成しPush
2. Streamlit Community Cloudにログイン  
   ```https://share.streamlit.io/```  
3. GitHubリポジトリを接続
4. ブランチ（main）と `run.py` を指定
5. Deployを実行
6. URLが発行され公開完了

---

## 補足（重要な設計ポイント）

- ユーザーはURLトークンで識別（`?token=`方式）
