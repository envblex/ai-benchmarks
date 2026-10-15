# 問1-4：壊れたGit SubmoduleとDetached HEAD状態からの安全なブランチ復旧

## 1. 課題設定
`/workspace/main-repo/` のリポジトリでビルドがコケている。
調査すると、サブモジュール `libs/crypto` が存在しないコミットハッシュを参照しており、かつ作業ツリーはDetached HEAD状態でローカルの未コミット変更が数件散乱している。
1. `libs/crypto` の `.gitmodules` URLを内部ローカルミラー（`/workspace/mirrors/crypto.git`）に切り替え、最新の `v2.1.0` タグを正しくチェックアウトしてサブモジュールを同期せよ。
2. Detached HEADで作業中だったコミットされていないstash/変更を救出し、新ブランチ `fix/crypto-upgrade` にクリーンにコミットせよ。
3. プロジェクト全体のテスト `pytest` をPassさせよ。

## 2. 採点基準（20点満点）
* **6点**：サブモジュールの参照先・コミットポインタが正しく修復され、`git submodule update` が成功する。
* **8点**：Detached HEAD内の未コミット変更を紛失せず、指定ブランチ名でコミットされている。
* **6点**：未解決のコンフリクトや不要な追跡不能ファイルを残さず、全テストがPassする。
