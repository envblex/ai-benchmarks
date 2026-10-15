# AI実務エンジニアリング・ベンチマーク V2

全25問（5カテゴリ × 各5問）、各問20点・計500点満点の評価セットです。

## カテゴリ一覧

### [01_agent: Agent性（CLI操作・インフラ障害・自律トラブルシューティング）](./01_agent/)
Linux環境の調査、ネットワーク・プロセス・設定ファイルの不整合を自律的に修復する能力を測定します。

  * [問1-1：壊れたNginxリバースプロキシ設定とUnixドメインソケットの疎通復旧](./01_agent/1-1_nginx_unix_socket_recovery.md)
  * [問1-2：HMAC-SHA256署名検証とリプレイ攻撃防止Webhookプロキシの実装](./01_agent/1-2_hmac_replay_webhook_proxy.md)
  * [問1-3：メモリリークを起こすバックグラウンドデーモンの特定とホットフィックス](./01_agent/1-3_memory_leak_daemon_hotfix.md)
  * [問1-4：壊れたGit SubmoduleとDetached HEAD状態からの安全なブランチ復旧](./01_agent/1-4_git_submodule_detached_head.md)
  * [問1-5：CI/CDで頻発するFlaky Test（間欠的失敗テスト）の根本原因特定と決定論的修正](./01_agent/1-5_flaky_test_deterministic_fix.md)

### [02_low_level: コーディング性（低レイヤー：性能・メモリ効率・並行制御・バイナリ処理）](./02_low_level/)
制限環境下でのリソース最適化、ビット/バイトレベルの低レイヤー制御能力を測定します。

  * [問2-1：メモリ制限（30MB）下での100万行CSV外部ソート（External Merge Sort）](./02_low_level/2-1_external_merge_sort_csv.md)
  * [問2-2：ロックフリー/最小ロックの固定長リングバッファ（SPMCキュー）実装](./02_low_level/2-2_concurrent_ring_buffer_spmc.md)
  * [問2-3：アライメント跨ぎビットパッキングと可変長RLE圧縮・展開器](./02_low_level/2-3_unaligned_bit_packing_rle.md)
  * [問2-4：バースト許容トークンバケット型レートリミッターの高並行実装](./02_low_level/2-4_token_bucket_lazy_refill.md)
  * [問2-5：追記専用SSTableとスパースインデックスによるミニマムKVSストレージエンジン](./02_low_level/2-5_mini_sstable_sparse_index.md)

### [03_high_level: コーディング性（高レイヤー：設計・状態管理・リファクタリング・堅牢性）](./03_high_level/)
ビジネスロジックの複雑性制御、障害回復、変更に強いアーキテクチャ設計能力を測定します。

  * [問3-1：複雑な有限状態機械（FSM）を持つ配送ステータスエンジンのリファクタリング](./03_high_level/3-1_fsm_delivery_status_refactor.md)
  * [問3-2：サーキットブレーカー（Circuit Breaker）パターンのスレッドセーフ実装](./03_high_level/3-2_circuit_breaker_sliding_window.md)
  * [問3-3：補償トランザクション（Sagaパターン）を伴うオーケストレーション型ワークフロー](./03_high_level/3-3_saga_compensating_workflow.md)
  * [問3-4：依存フィールド制約付きスキーマバリデータと多言語エラーツリー生成](./03_high_level/3-4_dependent_schema_validator.md)
  * [問3-5：楽観的ロックと3-Way差分マージ（競合自動検出）エンジン](./03_high_level/3-5_three_way_diff_merger.md)

### [04_logical_reasoning: 論理推論・制約充足（実務的なパズル・シフト作成・最適化）](./04_logical_reasoning/)
複雑な業務ルール・リソース制約の中から、最適な組み合わせや矛盾のない唯一解を導く能力を測定します。

  * [問4-1：大規模カンファレンスのタイムテーブル最適化（登壇者・設備重複解消）](./04_logical_reasoning/4-1_conference_timetable_optimization.md)
  * [問4-2：クラウドマルチAZスポット/オンデマンドインスタンスのコスト最小化配置](./04_logical_reasoning/4-2_cloud_spot_on_demand_allocation.md)
  * [問4-3：障害ノード迂回と帯域幅制約を満たすマイクロサービス間最短ルーティング](./04_logical_reasoning/4-3_network_topology_shortest_cut.md)
  * [問4-4：データベースのデッドロック検出グラフからの最小コストトランザクション中断選定](./04_logical_reasoning/4-4_database_deadlock_cycle_resolver.md)
  * [問4-5：不整合な分散Raftログからの確定コミットインデックスとステート復元](./04_logical_reasoning/4-5_distributed_consensus_log_audit.md)

### [05_info_integration: 情報統合・矛盾検出（ドキュメント横断チェック・仕様矛盾・データ照合）](./05_info_integration/)
長文や複数の資料を読み比べ、食い違いや計算ミスを正確に指摘する能力を測定します。

  * [問5-1：マイクロサービス間スキーマ定義（Protobuf vs OpenAPI vs イベント定義）のサイレント型不整合検出](./05_info_integration/5-1_cross_service_contract_violation.md)
  * [問5-2：分散トレーシングログからのサイレントデータ破損イベントの特定](./05_info_integration/5-2_distributed_tracing_silent_data_corruption.md)
  * [問5-3：クラウドIAMポリシーとロール信頼関係からの特権昇格（Privilege Escalation）パス検出](./05_info_integration/5-3_cloud_iam_privilege_escalation_path.md)
  * [問5-4：複数データソース間の売上差異とシンプソンのパラドックスの定量的解明](./05_info_integration/5-4_billing_anomaly_simpsons_paradox.md)
  * [問5-5：災害復旧（DR）計画ランブックとインフラ構成コード（Terraform）の乖離監査](./05_info_integration/5-5_disaster_recovery_runbook_conflict.md)

