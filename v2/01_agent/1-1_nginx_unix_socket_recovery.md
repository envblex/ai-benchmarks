# 問1-1：壊れたNginxリバースプロキシ設定とUnixドメインソケットの疎通復旧

## 1. 課題設定
`/workspace/infra/` にあるNginx設定とFastAPIバックエンドが通信不能（`502 Bad Gateway`）になっている。原因は以下の3箇所に潜んでいる。
1. `nginx.conf` 内のupstreamディレクティブで指定されたUnixドメインソケットのパスと、FastAPI（Uvicorn）がバインドしているソケットパスが微妙に異なる。
2. 生成されたソケットファイルのパーミッションが `0600`（所有者のみ）になっており、Nginxの実行ユーザー（`www-data`）から読み書きできない。
3. Nginx設定内の `proxy_set_header Host` に不要な改行が含まれており、構文チェック（`nginx -t`）は通るがHTTPパーサーエラーを引き起こす。
これらを特定・修復し、ローカルの `curl http://localhost/api/v1/health` が正常に `HTTP 200 {"status": "healthy"}` を返す状態にせよ。

## 2. 入力ファイル
- `/workspace/infra/nginx.conf`
- `/workspace/infra/service.py`
- `/workspace/infra/run.sh`

## 3. 採点基準（20点満点）
* **6点**：ソケットパスの不一致およびパーミッション問題を正しく特定・修正している。
* **6点**：ヘッダの不正構文を除去し、Nginxプロセスを正常リロード（`nginx -s reload` 等）できている。
* **8点**：評価ハーネスから `GET http://localhost/api/v1/health` へのリクエストが `HTTP 200` を返す。
