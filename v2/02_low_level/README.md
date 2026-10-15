# コーディング性（低レイヤー：性能・メモリ効率・並行制御・バイナリ処理）

制限環境下でのリソース最適化、ビット/バイトレベルの低レイヤー制御能力を測定します。

## 問題一覧

* [問2-1：メモリ制限（30MB）下での100万行CSV外部ソート（External Merge Sort）](./2-1_external_merge_sort_csv.md)
* [問2-2：ロックフリー/最小ロックの固定長リングバッファ（SPMCキュー）実装](./2-2_concurrent_ring_buffer_spmc.md)
* [問2-3：アライメント跨ぎビットパッキングと可変長RLE圧縮・展開器](./2-3_unaligned_bit_packing_rle.md)
* [問2-4：バースト許容トークンバケット型レートリミッターの高並行実装](./2-4_token_bucket_lazy_refill.md)
* [問2-5：追記専用SSTableとスパースインデックスによるミニマムKVSストレージエンジン](./2-5_mini_sstable_sparse_index.md)
