# AI実務エンジニアリング・ベンチマーク V3 (Agent-Centric / Symptom-Driven Edition)

シニア〜最上位エンジニアが直面する高難度・泥臭い開発・運用課題に焦点を当て、自律型AIエージェントの「探索・仮説検証・外科手術的修復能力」を測定する決定論的ベンチマークスイートです。

- **総問題数**: 5カテゴリ × 5問 ＝ 計25問
- **配点**: 各問20点（計500点満点）
- **評価方式**: Dockerコンテナ上での自動テスト（pytest・メトリクス測定・Holdoutテスト）。LLM-as-a-Judge不使用。

---

## V3の特徴（V2からの進化点）

1. **事前ネタバレの完全排除（Symptom-Driven）**:
   * 「原因は3箇所ある」等の事前ヒントを全廃。エージェントは「502エラーが発生している」「OOMで落ちる」「テストが間欠的に失敗する」といった**症状のみ**から自律的にログやコードを探索します。
2. **ゼロからのコード生成から「既存コードベースへの介入（Brownfield）」へ**:
   * 単なるアルゴリズムのワンショット生成を排除。数千行の既存リポジトリに対する再現確認、ボトルネック特定、最小限の外科手術的パッチ（git diff）を要求します。
3. **決定論的フィードバックループ（Holdout Tests）**:
   * 公開テストによる試行錯誤（自己修正ループ）と、過学習を防ぐ非公開テスト（Holdout tests）による厳密な合否判定（Pass@1）を採用しています。

---

## カテゴリ一覧

### [01_agent: Agent性（CLI自律調査・インフラ障害復旧・自律トラブルシューティング）](./01_agent/)
原因のネタバレがないブラックボックス環境で、ログやプロセス、OSシグナルを能動的に調査し、根本原因の特定から復旧・テスト完走まで自律的に完遂する能力を測定します。

  * [問1-1：本番Nginxリバースプロキシの502 Bad Gateway原因特定と自律復旧](./01_agent/1-1_nginx_502_socket_investigation.md)
  * [問1-2：Webhook受信プロキシの署名検証不整合とリプレイ攻撃脆弱性の解明・修正](./01_agent/1-2_webhook_signature_replay_guard.md)
  * [問1-3：常駐データコレクターデーモンの周期的OOMクラッシュ調査とメモリリークの外科手術](./01_agent/1-3_daemon_memory_leak_surgical_patch.md)
  * [問1-4：壊れたGit SubmoduleとDetached HEAD状態からのリグレッションなし自動復旧](./01_agent/1-4_git_submodule_detached_head_recovery.md)
  * [問1-5：CIで間欠的に失敗するFlakyテストの根本原因特定と決定論的修正](./01_agent/1-5_flaky_test_deterministic_elimination.md)

### [02_low_level: コーディング性（低レイヤー：性能・メモリ効率・並行制御・バイナリ処理）](./02_low_level/)
厳格なメモリ上限・高並行下でのデータ競合・バイナリ境界跨ぎなど、ハードウェアとOSの制約を意識した外科手術的パッチと最適化能力を測定します。

  * [問2-1：cgroupsメモリ制限（30MB）下での150MB CSVパイプラインOOM解消](./02_low_level/2-1_external_merge_sort_oom_bypass.md)
  * [問2-2：並行メッセージキュー（SPMC）のデータ競合・読み飛ばしバグ特定と解消](./02_low_level/2-2_spmc_ring_buffer_race_fix.md)
  * [問2-3：ビットパッキング・RLE展開エンジンのバイト境界アライメント跨ぎバグ修復](./02_low_level/2-3_unaligned_rle_bitpack_repair.md)
  * [問2-4：高並行トークンバケット型レートリミッターのロック競合ボトルネック解消](./02_low_level/2-4_token_bucket_lazy_refill_lock_contention.md)
  * [問2-5：追記専用SSTableエンジンにおけるコンパクション時データ消失バグの修正](./02_low_level/2-5_sstable_compaction_data_loss_fix.md)

### [03_high_level: コーディング性（高レイヤー：設計・状態管理・リファクタリング・堅牢性）](./03_high_level/)
複雑な業務ドメイン、ステートマシン、分散ワークフローの障害注入テスト（Chaos Testing）から生還する堅牢なアーキテクチャ修復能力を測定します。

  * [問3-1：配送追跡FSMの不正遷移・ゾンビ状態引き起こしバグの解消](./03_high_level/3-1_fsm_delivery_zombie_state_elimination.md)
  * [問3-2：サーキットブレーカーのHalf-Open遷移時スレッドセーフティ不備と誤遮断修正](./03_high_level/3-2_circuit_breaker_sliding_window_thread_safety.md)
  * [問3-3：決済マイクロサービスにおけるネットワーク障害時のSaga補償トランザクション漏れ修正](./03_high_level/3-3_saga_orchestration_chaos_recovery.md)
  * [問3-4：多言語スキーマバリデータの再帰的依存フィールド評価時スタックオーバーフロー回避](./03_high_level/3-4_dependent_schema_recursive_deadlock.md)
  * [問3-5：共同編集エンジンの3-Way差分マージにおける競合検出漏れ（サイレント上書き）解消](./03_high_level/3-5_three_way_diff_merge_conflict_leak.md)

### [04_logical_reasoning: 論理推論・最適化・分散合意（制約充足・デッドロック・分散ログ整合）](./04_logical_reasoning/)
実務の現場で発生する組み合わせ爆発、DBデッドロック競合グラフ、分散合意アルゴリズムの不整合を、厳密な論理とアルゴリズムで外科手術的に解消する能力を測定します。

  * [問4-1：カンファレンスタイムテーブル自動ソルバーの指数関数的探索停止と最適解算出](./04_logical_reasoning/4-1_conference_timetable_sat_exponential_blowup.md)
  * [問4-2：マルチAZクラウドSpot/On-Demand混在配置アルゴリズムの中断リスク不整合修正](./04_logical_reasoning/4-2_spot_instance_arbitrage_risk_constraint.md)
  * [問4-3：サービスメッシュ障害ノード迂回ルーティングのトポロジー閉路・ブラックホール解消](./04_logical_reasoning/4-3_service_mesh_topology_routing_loop_fix.md)
  * [問4-4：PostgreSQLデッドロック多発トランザクション群のログ解析とロック順序一意化パッチ](./04_logical_reasoning/4-4_postgresql_deadlock_lock_order_unification.md)
  * [問4-5：ネットワーク分断シミュレーション下でスプリットブレインを起こすRaft合意エンジンの修正](./04_logical_reasoning/4-5_raft_consensus_split_brain_commit_audit.md)

### [05_info_integration: 情報統合・仕様監査・脆弱性検出（スキーマ破壊・トレーシング不整合・権限昇格）](./05_info_integration/)
長大なドキュメント、スキーマ定義、分散トレーシングログ、IAMポリシー群を横断解析し、サイレント障害やセキュリティ脆弱性の再現・修正パッチを作成する能力を測定します。

  * [問5-1：gRPC Protobuf型変更に伴うGatewayのサイレント型崩れとE2Eテスト修正](./05_info_integration/5-1_grpc_protobuf_openapi_type_mismatch.md)
  * [問5-2：分散トレーシング（OpenTelemetry）ログからの非同期キューデータ化け箇所の特定と修正](./05_info_integration/5-2_opentelemetry_tracing_silent_corruption.md)
  * [問5-3：AWS IAMポリシーとAssumeRole信頼関係における特権昇格脆弱性の特定と塞ぎ込み](./05_info_integration/5-3_cloud_iam_privilege_escalation_exploit_fix.md)
  * [問5-4：複数データソース間の売上乖離（シンプソンのパラドックス）の定量的解明とSQL修正](./05_info_integration/5-4_billing_simpsons_paradox_sql_repair.md)
  * [問5-5：災害復旧（DR）計画ランブックとTerraformインフラコードの乖離監査と自動修復PR](./05_info_integration/5-5_disaster_recovery_runbook_drift_patch.md)

