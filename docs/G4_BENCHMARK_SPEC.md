# ai-benchmarks v4: G4 (RTX PRO 6000) × ローカルPodman 自律対話エージェント運用仕様書

- **作成日**: 2026-10-21
- **正本配置**: `~/workspace/projects/ai-benchmarks/docs/G4_BENCHMARK_SPEC.md`
- **対象ベンチマーク**: `ai-benchmarks v4`（全25問 × 温度5段階 `[0.2, 0.3, 0.4, 0.5, 0.6]` ＝ **1モデル計125試行**）

---

## 1. システムアーキテクチャ概要

本ベンチマークは、**「推論（頭脳）」** と **「実行環境（手足）」** を物理的に分離して運用する。

* **モデル推論（頭脳）**: Google Colab **G4**（NVIDIA RTX PRO 6000 Blackwell Server Edition 96GB GDDR7）
* **実行環境・採点（手足）**: ローカルマシン上の Podman サンドボックス（`bench-box`）
* **通信路**: Cloudflare Tunnel（`trycloudflare.com`）によるセキュアかつ高速なHTTP API連携
* **原則**: **手元でスクリプトとコンテナ環境を100%準備してからColabを起動**し、GPUインスタンスの課金時間を最短（純粋な推論時間のみ）に抑える。

---

## 2. 過去の失敗と根本原因（二度と繰り返さない教訓）

| 過去の過ち | 発生した問題 | 今後の是正ルール |
| :--- | :--- | :--- |
| **単発プロンプト投げ** | モデルが `ls -la` 等の探索コマンドを吐いた1ターン目で強制終了し、コード修正もテスト採点もゼロだった。 | **ReAct型のマルチターン対話ループ（最大15往復）を回し、直るまで自己修正させる。** |
| **Colab上でのclone/build** | 毎回 `git clone` や `cmake` ビルドを走らせて貴重なGPU時間を溶かした。 | **Google Drive（`bin/`）の事前ビルド済みバイナリを `/content/bin` に数秒でコピーして即起動。** |
| **壊れやすいMCP自動化への固執** | 画面情報（`$DISPLAY`）のないCLIからブラウザ操作を呼んで60秒タイムアウトとリバエン沼にハマった。 | **推論はAPI直叩き（Cloudflareトンネル経由）、Colab操作はブラウザタブ共有かセル直貼りで最速起動。** |
| **手元コンテナの環境不足** | 素の `python-slim` を使い、`git` や `curl`、`pytest` が入っておらずエージェントがコマンド実行不能に陥った。 | **Ubuntu 24.04 ベースで Python, Node.js, git, curl, pytest, uvicorn を完全事前インストール。** |

---

## 3. インフラ選定：なぜ G4（RTX PRO 6000 Blackwell）一択なのか

Google Colab において、A100 ではなく **G4** を採用する決定論的理由：

| 項目 | **G4 (RTX PRO 6000 Blackwell)** | A100-SXM4 (40GB) | 比較優位性 |
| :--- | :--- | :--- | :--- |
| **VRAM** | **96 GB GDDR7** | 40 GB HBM2 | **2.4倍**（長大コンテキスト・KVキャッシュでもOOM皆無） |
| **メモリ帯域** | **1,792 GB/s（1.8 TB/s）** | 1,555 GB/s | **1.15倍**（デコード速度が極めて高速） |
| **演算性能 (BF16)** | **960 TFLOPs** (第5世代Tensorコア) | 312 TFLOPs | **約3倍**（プロンプト処理・Prefillが爆速） |
| **Colab消費ユニット** | **6.71 ユニット / h** | 13.08 ユニット / h | **ほぼ半額（48%安価）** |

### 推論速度の期待値
* **MoEモデル（K2-Horizon-36B-A4B 等）**: **約 130 〜 180 tok/s**（1問あたり推論6〜7秒）
* **Denseモデル（35B全層モデル）**: **約 55 〜 65 tok/s**
* **Prefill速度**: **1,500 〜 3,000+ tok/s**（Flash Attention + バッチ2048）
* **全125試行の所要時間**: 1モデルあたり **約30〜40分** で完走。

---

## 4. Colab G4 側の起動パラメータ（超速構成）

Driveマウント後、事前ビルド済みバイナリを配置して以下のパラメータで起動する：

```bash
/content/bin/llama-server \
  -m "/content/drive/MyDrive/Google AI Studio/colab/models/<model_slug>/<model>.gguf" \
  -c 16384 \
  -ngl 99 \
  -fa \
  -b 2048 \
  -ub 1024 \
  -ctk q8_0 \
  -ctv q8_0 \
  -np 1 \
  --port 8080 \
  --host 0.0.0.0
```

* `-c 16384`: 16kコンテキスト。自己修正ログ（3〜4往復）を収めつつ最速のレイテンシを維持。
* `-fa`: Flash Attention。PrefillとKVキャッシュ帯域を最適化。
* `-b 2048 -ub 1024`: Blackwellの960 TFLOPsを活かす大容量バッチ。
* `-ctk q8_0 -ctv q8_0`: KVキャッシュ量子化（精度劣化なく帯域を半減）。
* `-np 1`: 単一スロット集中（1.8TB/sの全帯域を1試行に注ぎ込む）。

---

## 5. 実行環境（手元Podman `bench-box`）スペック要件

エージェントが実行する全25問のテストおよびコマンドを100%エラーなしで受け止めるためのフル装備コンテナ：

```bash
podman run -d --name bench-box \
  --userns=keep-id \
  -v /home/takayoshi/workspace/lab/bench-sandbox:/workspace:z \
  docker.io/library/ubuntu:24.04 \
  bash -c "
    apt-get update && apt-get install -y \
      python3 python3-pip python3-venv python3-dev \
      nodejs npm git curl wget jq lsof procps sqlite3 build-essential && \
    pip3 install --break-system-packages \
      pytest pytest-asyncio uvicorn fastapi httpx psutil grpcio protobuf && \
    sleep infinity
  "
```

### 必須ツールの対応タスク
* **`git`**: 問1-4（Detached HEAD、未コミット退避、reflog操作）
* **`curl` / `wget`**: 問1-1（Unixソケット経由のヘルスチェック `curl --unix-socket ...`）
* **`lsof` / `procps` (`ps`, `pkill`)**: 問1-1（ソケットバインド競合）, 問1-3（常駐デーモンメモリリーク）
* **`sqlite3` CLI**: 問4-4（SQLite WALデッドロック解析）
* **`nodejs` / `npm`**: エージェントがJSで補助スクリプトを実行する際のフォールバック
* **`pytest`, `pytest-asyncio`, `uvicorn`, `fastapi`**: 全自動テストハーネス

---

## 6. ベンチマーク実行方式：ターミナル対話ReActループ

1. **初期化**: 各試行（1/125）開始時、Podman内の `/workspace` をGitクリーンまたはテンプレートからクリーン復元（状態汚染の防止）。
2. **課題提示**: モデルに問題概要・制約・作業ディレクトリを提示。
3. **対話ループ（最大15ターン）**:
   * モデルが思考（Reasoning）を出力し、Bashコマンド（````bash ... ````）を生成。
   * 手元のランナーがコマンドを抽出し、Podmanコンテナ内で実行（タイムアウト30秒）。
   * 実行結果（stdout/stderr末尾2000文字）をモデルにフィードバック。
   * モデルがエラーを読んで自己修正を継続。
4. **提出・採点**:
   * モデルが完了を宣言するか、最大ターンに達した時点で非公開Holdoutテストを実行。
   * 各問20点満点（計500点満点）でスコアリング。

---

## 7. ログ完全永続化ルール

* **1試行（1/125）ごとに即時ディスク書き込み（Flush）**:
  メモリに保持せず、毎問完了時に JSON ファイルへ追記。中断時はそこから自動レジューム可能。
* **二重永続化**:
  * 手元: `~/workspace/projects/ai-benchmarks/benchmark_runs/<model>_125trials.json`
  * Drive: `/content/drive/MyDrive/Google AI Studio/colab/benchmarks/results_v4/results_<model>.json`
* **保存項目**:
  `model`, `task_id`, `temperature`, `duration_s`, `tok_s`, `tokens`, `reasoning_content`, `extracted_code`, `chat_history`（全ターミナル往復ログ）, `passed`, `score`, `stdout`, `stderr`
