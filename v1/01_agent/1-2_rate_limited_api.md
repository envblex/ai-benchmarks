# 問1-2：ページネーションとレート制限のあるローカルAPIからのデータ取得

## 1. 課題設定
ローカルで稼働するモックAPI（`http://localhost:8000/api/items`）から全アイテムを取得し、在庫切れ（`stock == 0`）かつ予約注文数が10件以上の商品ID一覧を抽出せよ。
APIは1リクエストあたり最大20件を返し、`next_cursor` によるページネーションが必要である。また、1秒間に5回以上アクセスすると `HTTP 429 Too Many Requests`（`Retry-After: 2` ヘッダ付き）を返す。

## 2. 入力・API仕様
- エンドポイント: `http://localhost:8000/api/items?cursor={cursor}&limit=20`
- レスポンス例:
```json
{
  "items": [{"id": "ITEM-001", "name": "...", "stock": 0, "backorders": 12}],
  "next_cursor": "abc123cursor",
  "has_more": true
}
```

## 3. 期待される出力
- 出力先: `/workspace/output/targeted_items.json`
- フォーマット:
```json
{
  "matched_item_ids": ["ITEM-004", "ITEM-019", "ITEM-102"],
  "total_scanned": 300,
  "request_count": 16
}
```

## 4. 採点基準（20点満点）
* **10点**：`next_cursor` を最後まで辿り、全300件のデータを漏れなく取得して正しい商品ID一覧を出力している。
* **6点**：`HTTP 429` 発生時にクラッシュせず、適切にウェイトを入れてリトライ処理を行っている。
* **4点**：無駄な無限ループを起こさず、25リクエスト以内で完了している。
