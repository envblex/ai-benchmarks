# 低レイヤー（性能・メモリ効率・並行制御・バイナリ処理）

厳格なメモリ上限・高並行下でのデータ競合・バイナリ境界跨ぎなど、ハードウェアとOSの制約を意識した外科手術的パッチと最適化能力を測定します。（全タスク非特権・自己完結型）

## 問題一覧

* [問2-1：メモリ上限（30MB）下での150MBトランザクションCSV外部ソート](./2-1_external_merge_sort_memory_limit.md)
* [問2-2：マルチスレッドSPMC固定長リングバッファの競合状態・データ読み飛ばし解消](./2-2_spmc_ring_buffer_concurrency_fix.md)
* [問2-3：ビットパッキング・可変長RLEエンコーダの非アライメント境界跨ぎデータ破壊修復](./2-3_unaligned_rle_bitpack_repair.md)
* [問2-4：高並行トークンバケット型レートリミッターのロック競合（CAS/Lazy Refill）最適化](./2-4_token_bucket_lazy_refill_lock_contention.md)
* [問2-5：追記専用SSTableエンジンにおけるコンパクション時データ消失バグの修正](./2-5_sstable_compaction_data_loss_fix.md)
