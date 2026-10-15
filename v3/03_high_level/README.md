# コーディング性（高レイヤー：設計・状態管理・リファクタリング・堅牢性）

複雑な業務ドメイン、ステートマシン、分散ワークフローの障害注入テスト（Chaos Testing）から生還する堅牢なアーキテクチャ修復能力を測定します。

## 問題一覧

* [問3-1：配送追跡FSMの不正遷移・ゾンビ状態引き起こしバグの解消](./3-1_fsm_delivery_zombie_state_elimination.md)
* [問3-2：サーキットブレーカーのHalf-Open遷移時スレッドセーフティ不備と誤遮断修正](./3-2_circuit_breaker_sliding_window_thread_safety.md)
* [問3-3：決済マイクロサービスにおけるネットワーク障害時のSaga補償トランザクション漏れ修正](./3-3_saga_orchestration_chaos_recovery.md)
* [問3-4：多言語スキーマバリデータの再帰的依存フィールド評価時スタックオーバーフロー回避](./3-4_dependent_schema_recursive_deadlock.md)
* [問3-5：共同編集エンジンの3-Way差分マージにおける競合検出漏れ（サイレント上書き）解消](./3-5_three_way_diff_merge_conflict_leak.md)
