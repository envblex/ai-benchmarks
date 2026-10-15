# 問5-3：クラウドIAMポリシーとロール信頼関係からの特権昇格（Privilege Escalation）パス検出

## 1. 課題設定
AWS風のIAMポリシーJSON（ユーザー10名、ロール15個、ポリシードキュメント30個）が与えられる。
一見すると管理者権限（`AdministratorAccess`）を持つユーザーは存在しないが、ポリシーの組み合わせ（例：`iam:PassRole` と `ec2:RunInstances`、または `lambda:UpdateFunctionCode`）によって、一般ユーザー「alice」が最終的にAdmin権限を奪取できる特権昇格パス（Escalation Path）が1本存在する。
この昇格パスをステップ順のJSONで出力せよ。

## 2. 採点基準（20点満点）
* **12点**：特権昇格を可能にしている中間ロールと悪用可能なアクションの組み合わせを正確に特定している。
* **8点**：aliceからAdministrator到達までの遷移ステップが正解の攻撃グラフと完全一致する。
