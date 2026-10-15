# 問1-1：文字コードと日付形式がバラバラな売上CSV群のクレンジングと集計

## 1. 課題設定
`/workspace/data/` 内に50個のCSVファイルがある。ファイルごとに文字コード（UTF-8, Shift_JIS, EUC-JP）、改行コード（LF, CRLF）、日付表記（`YYYY-MM-DD`, `YYYY/MM/DD`, `MM/DD/YYYY`）が混在しており、一部に重複行や金額欄の表記揺れ（`"¥1,200"`, `1200`）がある。これらをすべて正規化し、月別・店舗別の売上合計を `/workspace/output/summary.json` に出力せよ。

## 2. 入力データ仕様
- 配置場所: `/workspace/data/*.csv`（計50ファイル）
- 文字コード: UTF-8, Shift_JIS (CP932), EUC-JP
- カラム構成: `transaction_id,store_id,timestamp,amount,item_name`

## 3. 期待される出力
- 出力先: `/workspace/output/summary.json`
- フォーマット:
```json
{
  "2026-01": {
    "store_A": 1542000,
    "store_B": 980500
  },
  "2026-02": { ... }
}
```

## 4. 採点基準（20点満点）
* **8点**：文字化けを起こさず全50ファイルを読み込めている。
* **6点**：日付表記の揺れと金額のカンマ・通貨記号を正しく正規化し、重複行（ID一致）を除外できている。
* **6点**：出力された `summary.json` の各数値が正解データと完全一致する。
