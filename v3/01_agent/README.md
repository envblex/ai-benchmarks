# Agent性（CLI自律調査・インフラ障害復旧・自律トラブルシューティング）

原因のネタバレがないブラックボックス環境で、ログやプロセス、OSシグナルを能動的に調査し、根本原因の特定から復旧・テスト完走まで自律的に完遂する能力を測定します。

## 問題一覧

* [問1-1：本番Nginxリバースプロキシの502 Bad Gateway原因特定と自律復旧](./1-1_nginx_502_socket_investigation.md)
* [問1-2：Webhook受信プロキシの署名検証不整合とリプレイ攻撃脆弱性の解明・修正](./1-2_webhook_signature_replay_guard.md)
* [問1-3：常駐データコレクターデーモンの周期的OOMクラッシュ調査とメモリリークの外科手術](./1-3_daemon_memory_leak_surgical_patch.md)
* [問1-4：壊れたGit SubmoduleとDetached HEAD状態からのリグレッションなし自動復旧](./1-4_git_submodule_detached_head_recovery.md)
* [問1-5：CIで間欠的に失敗するFlakyテストの根本原因特定と決定論的修正](./1-5_flaky_test_deterministic_elimination.md)
