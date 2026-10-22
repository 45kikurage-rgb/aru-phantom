# Aru-Phantom 署名・更新台帳

更新日：2026-10-22 JST。対象はこの独立アプリのみです。既存ARUNOリポジトリ・Cloudflare・DB・署名鍵は変更しません。

| 項目 | 値 |
| --- | --- |
| アプリ名 | Aru-Phantom（アルファントム） |
| package / applicationId | com.aruno.aruphantom |
| versionName / versionCode | 1.1.4-aruno.1 / 12 |
| 用途 | このAPK本体の更新用・専用署名鍵。アプリ内で複製APKに使う鍵とは別 |
| alias | aru-phantom-release |
| 公開証明書SHA-256 | d22573f8b1fa29e6e59884ff23d95c0f6b7d23d1aa1609d0cffb9c860f69c6be |
| 管理者 | 45kikurage-rgb |
| 鍵方式 | RSA3072 / PKCS12。外側AES-256-GCM暗号化 |
| 主保管 | 非公開 45kikurage-rgb/aru-phantom-signing-backup / envelope.json |
| 独立暗号化コピー | Library Aru-Phantom_signing_recovery_A_2026-10-22.zip（libfile_b7edb1f4cbd08191922cd44e809a00df） |
| 復号情報の別管理 | Library ZIP内のAと、非公開repo内のBの両方が必要。単独では復号不可 |
| 非公開保管の固定commit | a7f63fdbd94b18197c2d74de4d5cfdfa66afce23 |
| 取得方法 | Libraryで上記IDを取得し、GitHub接続で非公開repoのpart-b.b64を取得 |
| 最終復元試験 | 2026-10-22。生成時のローカル鍵・パスワードを削除後、永続保管のA/Bを再取得し別ディレクトリ・別プロセスで復元。証明書一致と2種APKの署名検証に成功 |

## 更新時の手順

1. 最新の統括CURRENT §20・§21と本台帳を読む。公開鍵の指紋が一致する既存鍵を復元する。新鍵で代用しない。
2. GitHub接続とLibrary接続の両方を使い、秘密を会話に出力せず必要な復元情報を取得する。
3. `scripts/restore_signing.py RECOVERY_A.zip PART_B.b64 PRIVATE_OUTPUT_DIR` を実行する（Python cryptographyが必要）。
4. バージョンコードを増やしてビルドし、復元した同じ鍵で署名する。GitHub Actionsは利用しない。
5. 署名・アプリID・バージョン・APKのSHA-256を照合し、Releasesへ掲載後に外部から再取得して一致を確認する。
6. 作業後は復元した秘密鍵・パスワードの一時コピーを削除する。

暗号化コピーは2か所にありますが、復号はA/Bの両方を必要とします。いずれかのサービスへのアクセスを失った場合、そのアクセスを回復するまで復元できません。片方だけで復旧できる構成とは異なります。保管先のアクセス権を維持してください。

鍵・復号パスワード・復元用の部分情報を公開リポジトリ・チャット・報告書へ記載しません。アプリ本体の更新鍵を、利用者がアプリ内で作る複製用の鍵と混同しないでください。

## 初版検証

- 開発元ソース：2f803e4623b8f1bf1e891e26d2f74c52053b35f5
- ローカル `assembleRelease` 成功。GitHub Actionsは実行しない。
- 既存JUnit：141件中110成功、31スキップ（既定では外部サイトとのライブ試験を実行しない）、失敗0。
- 日本語チェック4件成功：全対象文言、辞書キー、差し込み値、言語選択経路。
- Android UI文言186項目と、配布元画面の日本語辞書464+239項目を追加。
- arm64-v8a版・universal版の署名検証成功。アプリID・versionCode・表示名・日本語の梱包を確認。
- 実機の画面表示・LINEの複製/ログイン/更新は未検証。Telegram連携の認証情報は含まない。

配布物のSHA-256はReleasesのSHA256SUMS.txtを参照してください。
