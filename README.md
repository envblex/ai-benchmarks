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
* **[`v4/`](./v4/)**: 決定論的自己完結版（Deterministic & Self-Contained Edition）
  * **非特権・完全自己完結**：systemd/cgroups/外部DB依存を排除し、Python標準・ASGI・SQLite WAL・メモリ制御でColabや非特権コンテナでも即実行可能。
  * **公開テスト vs 非公開Holdoutテストの二層分離**：自己修正ループと過学習判定の完全自動化。
  * **内包ハーネスランナー**：`harness/runner.py` により各問20点・計500点満点を自動集計。
* **[G4 × ローカルPodman 自律対話エージェント運用仕様書](./docs/G4_BENCHMARK_SPEC.md)**: Colab G4（RTX PRO 6000 Blackwell）と手元サンドボックス連携による125試行自律ベンチマーク運用手順とアーキテクチャ仕様。

---

## ディレクトリ構成

```text
ai-benchmarks/
├── README.md
├── v1/
├── v2/
├── v3/
└── v4/
    ├── README.md
    ├── harness/
    │   └── runner.py           # 決定論的採点・実行ハーネスランナー
    ├── 01_agent/               # Agent性（ASGIソケット障害・Webhook HMAC・メモリリーク・Git復旧・Flaky撲滅）
    ├── 02_low_level/           # 低レイヤー（外部マージソート・SPMCリングバッファ・非整列ビットパック・Lazy Refill・SSTable）
    ├── 03_high_level/          # 高レイヤー（FSMゾンビ解消・サーキットブレーカー・Saga補償・依存スキーマDAG・3-Way差分）
    ├── 04_logical_reasoning/   # 論理推論（CSP/SATタイムテーブル・Spot配置・メッシュ閉路・SQLite WALデッドロック・Raft分断）
    └── 05_info_integration/   # 情報統合（gRPC/OpenAPI型・OTelトレース特定・クラウドIAM昇格・シンプソンSQL・DRドリフト）
```

---

## 実行環境・アーキテクチャ

* **`sandbox` コンテナ**: AIエージェントの作業空間（`/workspace`）。Python 3.12, git, gcc, sqlite3, curl, jq 完備。
* **`verifier` コンテナ**: モックAPI稼働および非公開テストスイート（Holdout Tests）を実行する採点ハーネス。

各問題のディレクトリ内にある個別Markdownファイルに、課題設定・制約条件・採点基準（配点内訳）が記載されています。
