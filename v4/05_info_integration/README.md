# 情報統合・仕様監査・脆弱性検出（スキーマ破壊・トレーシング不整合・権限昇格）

長大なドキュメント、スキーマ定義、分散トレーシングログ、IAMポリシー群を横断解析し、サイレント障害やセキュリティ脆弱性の再現・修正パッチを作成する能力を測定します。（全タスク非特権・自己完結型）

## 問題一覧

* [問5-1：gRPC Protobuf・OpenAPIスキーマ変更に伴うGatewayのサイレント型崩れ監査と修復](./5-1_grpc_protobuf_openapi_type_mismatch.md)
* [問5-2：OpenTelemetry分散トレーシングログからの非同期キューデータ化け箇所の特定と修正](./5-2_opentelemetry_tracing_silent_corruption.md)
* [問5-3：クラウドIAMポリシーとAssumeRole信頼関係における特権昇格脆弱性の塞ぎ込み](./5-3_cloud_iam_privilege_escalation_fix.md)
* [問5-4：複数データソース間の売上集計乖離（シンプソンのパラドックス）の定量的解明とSQL修正](./5-4_billing_simpsons_paradox_sql_repair.md)
* [問5-5：災害復旧（DR）計画ランブックとIaC定義の乖離監査と自動修復パッチ](./5-5_disaster_recovery_runbook_drift_patch.md)
