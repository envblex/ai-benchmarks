# AI実務エンジニアリング・ベンチマーク V4 (Deterministic & Self-Contained Edition)

シニア〜最上位エンジニアが直面する高難度・泥臭い開発・運用課題に焦点を当て、自律型AIエージェントの「探索・仮説検証・外科手術的修復能力」を測定する決定論的ベンチマークスイートです。

- **総問題数**: 5カテゴリ × 5問 ＝ 計25問
- **配点**: 各問20点（計500点満点）
- **評価方式**: Python内包テスト（pytest・メトリクス測定・非公開Holdoutテスト）。LLM-as-a-Judge不使用。

---

## V4の特徴（V3からの進化点と根本改善）

1. **完全自己完結・非特権動作（Zero Host-Daemon Dependency）**:
   * root権限、systemd、cgroups物理設定、外部デーモン（Nginx/PostgreSQL実体）への不要な依存を全廃。
   * Python標準ライブラリ（`resource`, `tracemalloc`, `sqlite3`）、ASGI/Uvicorn、インメモリ制御で完全再現。Google Colabや制約の厳しいコンテナ環境でも100%決定論的に動作します。
2. **公開テストと非公開Holdoutテストの明確な分離**:
   * エージェントが自己検証ループで回す「公開テスト（Public Tests）」と、汎化性能と過学習を厳密に測定する「非公開Holdoutテスト（Private Tests）」の境界を確立。
3. **決定論的自動採点ハーネス（Built-in Benchmark Runner）**:
   * 各タスクの実行・採点・スコア集計を行う決定論的CLIランナー（`harness/runner.py`）を標準内包。

---

## カテゴリ一覧

### [01_agent: Agent性（自律調査・インフラ障害復旧・自律トラブルシューティング）](./01_agent/)
原因のネタバレがないブラックボックス環境で、ログやプロセス、OSシグナルを能動的に調査し、根本原因の特定から復旧・テスト完走まで自律的に完遂する能力を測定します。（全タスク非特権・自己完結型）

  * [問1-1：ASGIリバースプロキシのUnixソケット通信障害・502復旧](./01_agent/1-1_asgi_socket_proxy_502_recovery.md)
  * [問1-2：Webhook受信プロキシの署名検証不整合とリプレイ攻撃脆弱性の解明・修正](./01_agent/1-2_webhook_signature_replay_guard.md)
  * [問1-3：常駐データコレクターデーモンの周期的OOMクラッシュ調査とメモリリークの外科手術](./01_agent/1-3_daemon_memory_leak_surgical_patch.md)
  * [問1-4：壊れたGitリポジトリ（Detached HEAD・参照不整合・未コミット退避）の自動復旧](./01_agent/1-4_git_detached_head_branch_recovery.md)
  * [問1-5：CIで間欠的に失敗する非同期イベントバスFlakyテストの根本原因特定と決定論的修正](./01_agent/1-5_flaky_test_deterministic_elimination.md)

### [02_low_level: 低レイヤー（性能・メモリ効率・並行制御・バイナリ処理）](./02_low_level/)
厳格なメモリ上限・高並行下でのデータ競合・バイナリ境界跨ぎなど、ハードウェアとOSの制約を意識した外科手術的パッチと最適化能力を測定します。（全タスク非特権・自己完結型）

  * [問2-1：メモリ上限（30MB）下での150MBトランザクションCSV外部ソート](./02_low_level/2-1_external_merge_sort_memory_limit.md)
  * [問2-2：マルチスレッドSPMC固定長リングバッファの競合状態・データ読み飛ばし解消](./02_low_level/2-2_spmc_ring_buffer_concurrency_fix.md)
  * [問2-3：ビットパッキング・可変長RLEエンコーダの非アライメント境界跨ぎデータ破壊修復](./02_low_level/2-3_unaligned_rle_bitpack_repair.md)
  * [問2-4：高並行トークンバケット型レートリミッターのロック競合（CAS/Lazy Refill）最適化](./02_low_level/2-4_token_bucket_lazy_refill_lock_contention.md)
  * [問2-5：追記専用SSTableエンジンにおけるコンパクション時データ消失バグの修正](./02_low_level/2-5_sstable_compaction_data_loss_fix.md)

### [03_high_level: 高レイヤー（アーキテクチャ・状態管理・分散ワークフロー・堅牢性）](./03_high_level/)
複雑な業務ドメイン、ステートマシン、分散ワークフローの障害注入テストから生還する堅牢なアーキテクチャ修復能力を測定します。（全タスク非特権・自己完結型）

  * [問3-1：配送追跡FSMの不正遷移・ゾンビ状態引き起こしバグの解消](./03_high_level/3-1_fsm_delivery_zombie_state_elimination.md)
  * [問3-2：サーキットブレーカーのスライディングウィンドウ・スレッドセーフティ不備と誤遮断修正](./03_high_level/3-2_circuit_breaker_sliding_window_thread_safety.md)
  * [問3-3：決済マイクロサービスにおけるSagaオーケストレーターの補償トランザクション漏れ修正](./03_high_level/3-3_saga_orchestrator_chaos_recovery.md)
  * [問3-4：依存スキーマバリデータの再帰的循環参照スタックオーバーフロー回避](./03_high_level/3-4_dependent_schema_recursive_deadlock.md)
  * [問3-5：共同編集エンジンの3-Way差分マージにおける競合検出漏れ（サイレント上書き）解消](./03_high_level/3-5_three_way_diff_merge_conflict_leak.md)

### [04_logical_reasoning: 論理推論・最適化・分散合意（制約充足・デッドロック・分散ログ整合）](./04_logical_reasoning/)
実務の現場で発生する組み合わせ爆発、トランザクションデッドロック競合グラフ、分散合意アルゴリズムの不整合を、厳密な論理とアルゴリズムで外科手術的に解消する能力を測定します。（全タスク非特権・自己完結型）

  * [問4-1：カンファレンスタイムテーブル自動スケジューラーの探索空間枝刈り・SAT最適解](./04_logical_reasoning/4-1_conference_timetable_sat_exponential_blowup.md)
  * [問4-2：クラウドSpot/On-Demand混在配置アルゴリズムの中断リスク最適化](./04_logical_reasoning/4-2_spot_instance_arbitrage_risk_constraint.md)
  * [問4-3：サービスメッシュ障害ノード迂回ルーティングのトポロジー閉路・ブラックホール解消](./04_logical_reasoning/4-3_service_mesh_topology_routing_loop_fix.md)
  * [問4-4：SQLite WALマルチトランザクションデッドロックログ解析とロック順序一意化パッチ](./04_logical_reasoning/4-4_sqlite_wal_deadlock_cycle_resolver.md)
  * [問4-5：分散合意（Raft）シミュレータのスプリットブレイン・未コミットログ破棄バグ修正](./04_logical_reasoning/4-5_raft_consensus_split_brain_audit.md)

### [05_info_integration: 情報統合・仕様監査・脆弱性検出（スキーマ破壊・トレーシング不整合・権限昇格）](./05_info_integration/)
長大なドキュメント、スキーマ定義、分散トレーシングログ、IAMポリシー群を横断解析し、サイレント障害やセキュリティ脆弱性の再現・修正パッチを作成する能力を測定します。（全タスク非特権・自己完結型）

  * [問5-1：gRPC Protobuf・OpenAPIスキーマ変更に伴うGatewayのサイレント型崩れ監査と修復](./05_info_integration/5-1_grpc_protobuf_openapi_type_mismatch.md)
  * [問5-2：OpenTelemetry分散トレーシングログからの非同期キューデータ化け箇所の特定と修正](./05_info_integration/5-2_opentelemetry_tracing_silent_corruption.md)
  * [問5-3：クラウドIAMポリシーとAssumeRole信頼関係における特権昇格脆弱性の塞ぎ込み](./05_info_integration/5-3_cloud_iam_privilege_escalation_fix.md)
  * [問5-4：複数データソース間の売上集計乖離（シンプソンのパラドックス）の定量的解明とSQL修正](./05_info_integration/5-4_billing_simpsons_paradox_sql_repair.md)
  * [問5-5：災害復旧（DR）計画ランブックとIaC定義の乖離監査と自動修復パッチ](./05_info_integration/5-5_disaster_recovery_runbook_drift_patch.md)

