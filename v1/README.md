# AI実務エンジニアリング・ベンチマーク V1

全25問（5カテゴリ × 各5問）、各問20点・計500点満点の評価セットです。

## カテゴリ一覧

### [01_agent: Agent性（CLI操作・API連携・自律トラブルシューティング）](./01_agent/)
Linuxの標準コマンド、ファイル操作、ローカルAPIを組み合わせて、環境内の問題を調査・解決する能力を測定します。

  * [問1-1：文字コードと日付形式がバラバラな売上CSV群のクレンジングと集計](./01_agent/1-1_csv_cleansing_aggregation.md)
  * [問1-2：ページネーションとレート制限のあるローカルAPIからのデータ取得](./01_agent/1-2_rate_limited_api.md)
  * [問1-3：起動しないWebアプリケーションの原因特定と復旧](./01_agent/1-3_broken_web_app_recovery.md)
  * [問1-4：Gitのコンフリクト解消とバグ混入コミットの特定（Git Bisect）](./01_agent/1-4_git_bisect_conflict_resolution.md)
  * [問1-5：プロンプトインジェクションを含む社内ドキュメントからの情報抽出](./01_agent/1-5_prompt_injection_doc_extraction.md)

### [02_low_level: コーディング性（低レイヤー：性能・メモリ効率・並行制御・バイナリ処理）](./02_low_level/)
実務で必要となる計算量・メモリ使用量の削減、スレッドセーフな実装、バイナリプロトコルの正確なパースを評価します。

  * [問2-1：メモリ制限（50MB）下での1GBアクセスログのTop-K集計](./02_low_level/2-1_memory_limited_log_topk.md)
  * [問2-2：スレッドセーフかつTTL（有効期限）付きのLRUキャッシュの実装](./02_low_level/2-2_ttl_lru_cache.md)
  * [問2-3：独自バイナリパケット（エンディアン・ビットフィールド・CRC）のパーサー実装](./02_low_level/2-3_binary_packet_parser.md)
  * [問2-4：デッドロックを起こさないマルチリソース・ワーカープールの実装](./02_low_level/2-4_deadlock_free_worker_pool.md)
  * [問2-5：N+1問題と全件スキャンを解消するクエリ・インデックス最適化](./02_low_level/2-5_n_plus_one_query_optimization.md)

### [03_high_level: コーディング性（高レイヤー：設計・状態管理・リファクタリング・堅牢性）](./03_high_level/)
ビジネスロジックの複雑さを整理し、仕様変更や通信エラーに強いクリーンな設計を行う能力を測定します。

  * [問3-1：スパゲッティ化した割引・クーポン計算エンジンのリファクタリングと機能追加](./03_high_level/3-1_discount_coupon_refactoring.md)
  * [問3-2：二重決済と在庫マイナスを防ぐ冪等（Idempotent）な注文APIの実装](./03_high_level/3-2_idempotent_order_api.md)
  * [問3-3：循環参照とエラー伝播をサポートする依存関係タスクランナーの実装](./03_high_level/3-3_dag_task_runner.md)
  * [問3-4：プラグイン可能なマルチチャネル通知ルーターの設計とフォールバック制御](./03_high_level/3-4_notification_router.md)
  * [問3-5：Undo / Redo（取り消し・やり直し）と競合検知を備えたリッチテキスト状態の管理](./03_high_level/3-5_undo_redo_rich_text.md)

### [04_logical_reasoning: 論理推論・制約充足（実務的なパズル・シフト作成・最適化）](./04_logical_reasoning/)
条件が複雑に絡み合った実務的なスケジュールや割り当て問題を解く能力を測ります。

  * [問4-1：看護師のシフト表作成（6つの制約条件をすべて満たす割り当て）](./04_logical_reasoning/4-1_nurse_scheduling.md)
  * [問4-2：会議室の予約競合解消と最大利用人数の最適化](./04_logical_reasoning/4-2_meeting_room_optimization.md)
  * [問4-3：発言の真偽とタイムラインから犯人と犯行時刻を特定する論理パズル](./04_logical_reasoning/4-3_server_room_intruder_puzzle.md)
  * [問4-4：複数倉庫からの配送コスト・CO2排出量の上限付き最小化](./04_logical_reasoning/4-4_multi_warehouse_dispatch.md)
  * [問4-5：不完全なリーグ戦結果テーブルからの全試合スコア復元](./04_logical_reasoning/4-5_league_score_restoration.md)

### [05_info_integration: 情報統合・矛盾検出（ドキュメント横断チェック・仕様矛盾・データ照合）](./05_info_integration/)
長文や複数の資料を読み比べ、食い違いや計算ミスを正確に指摘する能力を測定します。

  * [問5-1：要件定義書・API仕様書（OpenAPI）・DB定義（DDL）の3者間不整合の網羅的検出](./05_info_integration/5-1_spec_mismatch_detection.md)
  * [問5-2：3つのマイクロサービスの分散ログからの障害根本原因（Root Cause）の特定](./05_info_integration/5-2_microservices_log_root_cause.md)
  * [問5-3：社内経費精算規定の改定履歴と申請データのコンプライアンス違反チェック](./05_info_integration/5-3_expense_compliance_audit.md)
  * [問5-4：財務・売上レポートの「グラフ・本文・集計表」間の数値改ざんと計算ミスの検出](./05_info_integration/5-4_financial_report_discrepancy.md)
  * [問5-5：複数の予定表・会場マップ・お知らせプリントからの個人スケジュール構築](./05_info_integration/5-5_schedule_deduplication.md)

