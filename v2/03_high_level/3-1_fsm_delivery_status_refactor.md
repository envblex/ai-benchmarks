# 問3-1：複雑な有限状態機械（FSM）を持つ配送ステータスエンジンのリファクタリング

## 1. 課題設定
EC配送管理システムのステータス遷移ロジック（現在、ネストした200行の `if/elif/else` で書かれている）が与えられる。
ステータス：`ORDERED`, `PAID`, `PREPARING`, `SHIPPED`, `IN_TRANSIT`, `DELIVERED`, `FAILED_ATTEMPT`, `RETURNED`, `CANCELLED`。
このコードをStateパターンまたは明示的な遷移テーブル（Transition Table）にリファクタリングした上で、以下の2つの仕様変更を適用せよ。
1. `FAILED_ATTEMPT`（不在持ち戻り）は最大3回まで許容し、3回失敗した時点で自動的に `RETURNED` へ遷移させる。
2. `IN_TRANSIT` 状態のときのみ、ユーザーからの「置き配指定（`DROP_OFF_REQUESTED`）」イベントを受け付けてメタデータを更新できる（ただし冷凍商品フラグがある場合は例外 `InvalidOperationError` を投げる）。

## 2. 採点基準（20点満点）
* **8点**：既存の全40パターンの状態遷移回帰テストをすべてPassする。
* **6点**：不正な状態遷移に対して厳密に `InvalidTransitionError` を投げる。
* **6点**：追加された「3回不在自動返送」および「置き配制限」の境界値テストがPassし、クラスの凝集度が高い設計になっている。
