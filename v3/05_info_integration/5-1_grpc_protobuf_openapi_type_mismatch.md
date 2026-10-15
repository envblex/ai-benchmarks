# 問5-1：gRPC Protobuf型変更に伴うGatewayのサイレント型崩れとE2Eテスト修正

## 1. 課題設定
マイクロサービスアーキテクチャ（`/workspace/gateway-service/`）において、バックエンドgRPCサービスのProtoファイルが更新され、決済金額フィールドが `int32` から `string`（64bit整数桁あふれ対策および固定小数点対応）に変更された。
しかし、外部公開用のOpenAPI仕様書およびBFF（Backend For Frontend）側のJSONシリアライザが追従しておらず、E2Eテストで金額の末尾切り捨てや型キャスト例外がサイレントに発生している。
エージェントはProto定義、OpenAPIスキーマ、およびマッピングコードを横断調査し、型安全性を維持する完全な修正パッチを適用してCIをグリーンにせよ。

## 2. 作業環境
- リポジトリ: `/workspace/gateway-service/`
  - バックエンドProto: `proto/payment.proto`
  - 公開OpenAPI: `docs/openapi.yaml`
  - マッピング層: `src/mappers/payment.ts` または `src/mappers/payment.py`
- テスト実行: `pytest tests/test_e2e_contracts.py`

## 3. 達成条件
1. 契約テスト（Contract Test）の失敗箇所から、型仕様の食い違い（Proto vs OpenAPI vs アプリコード）を洗い出すこと。
2. 既存のクライアント互換性を壊さないように配慮しつつ、スキーマ定義とマッピング層を整合させること。
3. すべての契約検証テストおよび型チェック（TypeScriptまたはmypy）をエラー0件で通過させること。

## 4. 採点基準（20点満点）
* **8点**：Proto変更に起因するスキーマ・マッパー・バリデーションの不整合箇所をすべて特定・修正している。
* **6点**：静的型検査（mypy/tsc）およびシリアライズ/デシリアライズテストを正常パスさせている。
* **6点**：Holdoutスキーマ境界値テスト（int64最大値・小数が渡された際の精度保証）を100%パスする。
