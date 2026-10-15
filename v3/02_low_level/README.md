# コーディング性（低レイヤー：性能・メモリ効率・並行制御・バイナリ処理）

厳格なメモリ上限・高並行下でのデータ競合・バイナリ境界跨ぎなど、ハードウェアとOSの制約を意識した外科手術的パッチと最適化能力を測定します。

## 問題一覧

* [問2-1：cgroupsメモリ制限（30MB）下での150MB CSVパイプラインOOM解消](./2-1_external_merge_sort_oom_bypass.md)
* [問2-2：並行メッセージキュー（SPMC）のデータ競合・読み飛ばしバグ特定と解消](./2-2_spmc_ring_buffer_race_fix.md)
* [問2-3：ビットパッキング・RLE展開エンジンのバイト境界アライメント跨ぎバグ修復](./2-3_unaligned_rle_bitpack_repair.md)
* [問2-4：高並行トークンバケット型レートリミッターのロック競合ボトルネック解消](./2-4_token_bucket_lazy_refill_lock_contention.md)
* [問2-5：追記専用SSTableエンジンにおけるコンパクション時データ消失バグの修正](./2-5_sstable_compaction_data_loss_fix.md)
