# 問1-4：壊れたGit SubmoduleとDetached HEAD状態からのリグレッションなし自動復旧

## 1. 課題設定
マルチリポジトリ構成の開発プロジェクト（`/workspace/core-engine/`）において、不正なマージ操作とサブモジュールの参照先コミット不整合により、CIビルドが `fatal: reference is not a tree` で停止している。
さらに、サブモジュール側で緊急ホットフィックスがコミットされていたにもかかわらず `Detached HEAD` 状態で放置され、親リポジトリの追跡ブランチとの同期が破綻している。
エージェントはGitのオブジェクトツリー、コミット履歴、reflogを精査し、コミット履歴を消失させることなく安全に正常な同期状態へ修復せよ。

## 2. 作業環境
- 親リポジトリ: `/workspace/core-engine/`
- サブモジュール: `/workspace/core-engine/libs/crypto/`
- CI再現スクリプト: `/workspace/scripts/run_ci_check.sh`

## 3. 達成条件
1. サブモジュール内で宙に浮いているコミット（Dangling / Detached commit）を特定し、適切な追跡ブランチへ統合すること。
2. 親リポジトリ側のサブモジュールポインタを最新の安全なコミットに更新し、`.gitmodules` の設定を整合させること。
3. `git submodule status` および `run_ci_check.sh` がクリーンに完了すること。

## 4. 採点基準（20点満点）
* **6点**：サブモジュール内の未追跡・Detachedコミットを消失させずに回収・マージしている。
* **6点**：親リポジトリのコミットポインタとブランチ追跡関係を正しく更新している。
* **8点**：Holdoutテスト（クリーンチェックアウトからの `git submodule update --init --recursive` および全体ビルド）が正常完了する。
