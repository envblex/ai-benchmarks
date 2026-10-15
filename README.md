# AI実務エンジニアリング・ベンチマークスイート（ai-benchmarks）

実務のシニア〜中堅エンジニアが直面するリアルな開発・運用課題に焦点を当て、自律型AIエージェントの真の実力を測定する決定論的ベンチマークスイートです。

- **総問題数**: 5カテゴリ × 5問 ＝ 計25問
- **配点**: 各問20点（計500点満点）
- **評価方式**: Dockerコンテナ上での自動テスト（pytest・完全一致照合・メトリクス測定）。LLM-as-a-Judge不使用。

---

## バージョン構成

* **[`v1/`](./v1/)**: 実務課題適正化版（基本設計）
  * 文字コード混在CSV集計、レート制限API取得、壊れたFastAPI復旧、Git bisect、プロンプトインジェクション防御、TTL LRUキャッシュ、バイナリパケットパース、DAGタスクランナー、シフト最適化、OpenAPI/DDL不整合検出など。
* **[`v2/`](./v2/)**: 現場エッジケース＆泥臭いトラブルシューティング特化版（発展設計）
  * Unixソケット権限・Nginx復旧、HMACリプレイ防御、メモリリークホットフィックス、Flakyテスト撲滅、外部マージソート（メモリ30MB制限）、SSTableスパースインデックス、Saga補償トランザクション、IAM特権昇格パス検出、DRランブック監査など。
* **[`v3/`](./v3/)**: 自律Agent特化・症状ドリブン版（Agent-Centric Edition）
  * **事前ネタバレ全廃**：ヒントなしの障害症状から自律調査。
  * **既存コードベース外科手術（Brownfield）**：数千行リポジトリのボトルネック特定・最小パッチ（git diff）。
  * **非公開Holdoutテストによる決定論的合否判定**：高難度（シニア級）を維持したまま純粋なAgent性を測定。

---

## ディレクトリ構成

```text
ai-benchmarks/
├── README.md
├── v1/
│   ├── README.md
│   ├── 01_agent/
│   ├── 02_low_level/
│   ├── 03_high_level/
│   ├── 04_logical_reasoning/
│   └── 05_info_integration/
├── v2/
│   ├── README.md
│   ├── 01_agent/
│   ├── 02_low_level/
│   ├── 03_high_level/
│   ├── 04_logical_reasoning/
│   └── 05_info_integration/
└── v3/
    ├── README.md
    ├── 01_agent/               # Agent性（CLI自律調査・インフラ障害復旧・ブラックボックス調査）
    ├── 02_low_level/           # 低レイヤー（cgroups制約突破・並行キュー競合・バイナリ復旧）
    ├── 03_high_level/          # 高レイヤー（FSMゾンビ状態解消・Sagaカオス耐性・差分マージ競合）
    ├── 04_logical_reasoning/   # 論理推論（探索空間枝刈り・PostgreSQLデッドロック・Raft合意分断）
    └── 05_info_integration/   # 情報統合（Proto-OpenAPI型崩れ・トレーシングデータ破壊・IAM昇格PoC）
```

---

## 実行環境・アーキテクチャ

* **`sandbox` コンテナ**: AIエージェントの作業空間（`/workspace`）。Python 3.12, git, gcc, sqlite3, curl, jq 完備。
* **`verifier` コンテナ**: モックAPI稼働および非公開テストスイート（Holdout Tests）を実行する採点ハーネス。

各問題のディレクトリ内にある個別Markdownファイルに、課題設定・制約条件・採点基準（配点内訳）が記載されています。
