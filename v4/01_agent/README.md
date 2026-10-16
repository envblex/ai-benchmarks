# Agent性（自律調査・インフラ障害復旧・自律トラブルシューティング）

原因のネタバレがないブラックボックス環境で、ログやプロセス、OSシグナルを能動的に調査し、根本原因の特定から復旧・テスト完走まで自律的に完遂する能力を測定します。（全タスク非特権・自己完結型）

## 問題一覧

* [問1-1：ASGIリバースプロキシのUnixソケット通信障害・502復旧](./1-1_asgi_socket_proxy_502_recovery.md)
* [問1-2：Webhook受信プロキシの署名検証不整合とリプレイ攻撃脆弱性の解明・修正](./1-2_webhook_signature_replay_guard.md)
* [問1-3：常駐データコレクターデーモンの周期的OOMクラッシュ調査とメモリリークの外科手術](./1-3_daemon_memory_leak_surgical_patch.md)
* [問1-4：壊れたGitリポジトリ（Detached HEAD・参照不整合・未コミット退避）の自動復旧](./1-4_git_detached_head_branch_recovery.md)
* [問1-5：CIで間欠的に失敗する非同期イベントバスFlakyテストの根本原因特定と決定論的修正](./1-5_flaky_test_deterministic_elimination.md)
