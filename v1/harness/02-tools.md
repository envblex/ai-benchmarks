# エージェントに提供されるツール定義 (Tool Calling Schema)

参照: `ok.pdf` p.13

すべての呼び出しと返り値はハーネス側で OpenTelemetry 形式のトレースログとして記録される。エージェントはサンドボックス環境と対話するために、以下の 4 つの関数 (Tool) のみを呼び出すことができる。

## 1. `execute_bash`

```json
{
  "name": "execute_bash",
  "parameters": {
    "type": "object",
    "properties": {
      "command": { "type": "string", "description": "実行するシェルコマンド文字列" },
      "timeout_sec": { "type": "integer", "description": "タイムアウト秒数 (最大 120 秒)", "default": 30 }
    },
    "required": ["command"]
  }
}
```

- サンドボックス内の `/workspace` ディレクトリをカレントディレクトリとして bash コマンドを実行する。状態 (環境変数、カレントディレクトリ、作成されたファイル) は呼び出し間で保持される。

## 2. `read_file`

```json
{
  "name": "read_file",
  "parameters": {
    "type": "object",
    "properties": {
      "filepath": { "type": "string" },
      "start_line": { "type": "integer", "default": 1 },
      "end_line": { "type": "integer", "default": 200 }
    },
    "required": ["filepath"]
  }
}
```

- 指定されたファイルの内容を行番号付きで読み取る。巨大なファイルを一度に読み取ってコンテキストを溢れさせることを防ぐため、行範囲を指定して部分的な読み取りが可能になっている。

## 3. `write_file`

```json
{
  "name": "write_file",
  "parameters": {
    "type": "object",
    "properties": {
      "file_path": { "type": "string" },
      "content": { "type": "string" }
    },
    "required": ["file_path", "content"]
  }
}
```

- 指定されたパスにファイルを新規作成または上書き保存する。既存の読み取り専用ファイルやテストハーネスファイルの改ざんは検知され、即座に 0 点となる。

## 4. `submit_final_answer`

```json
{
  "name": "submit_final_answer",
  "parameters": {
    "type": "object",
    "properties": {
      "submission_payload": {
        "type": "object",
        "description": "各問題の Output Schema で厳密に指定されたキーと型を持つ JSON オブジェクト"
      }
    },
    "required": ["submission_payload"]
  }
}
```

- タスクの完了を宣言し、最終的な解答ペイロード (JSON オブジェクト) を提出して評価セッションを終了する。
