# 🚀 FastAPIサンプル 🚀

## 🔸 環境構築

### サーバー証明書作成

1. 証明書格納ディレクトリに移動

    ```bash
    cd container/web/ssl
    ```

1. 秘密鍵生成

    ```bash
    openssl genrsa 2024 > server.key
    ```
1. 証明書署名要求生成

    ```bash
    openssl req -new -key server.key > server.csr
    ```

1. 証明書署名要求生成

    ```bash
    openssl x509 -req -days 3650 -signkey server.key < server.csr > server.crt
    ```

※OpenSSLの場合

### 環境変数ファイルの作成

1. 環境変数ファイルの作成

    ```bash
    touch container/app/src/.env
    ```

1. 環境変数の設定

    ```env
    ALLOW_ORIGINS=["*"]
    ALLOW_HEADERS=["*"]

    DB_HOST=host.docker.internal:5432
    DB_USER=postgres
    DB_PASS=Zh9BbsS7
    DB_NAME=fastapi_sample_dev

    DB_HOST_TEST=host.docker.internal:5432
    DB_USER_TEST=postgres
    DB_PASS_TEST=Zh9BbsS7
    DB_NAME_TEST=fastapi_sample_test

    CSRF_KEY=Xv4qMrh8
    JWT_KEY=Qm3FwsTn

    LOG_DIR=logs

    DEBUG=True
    ```

### コンテナの起動

1. コンテナの起動

    ```bash
    docker compose up -d
    ```

1. マイグレーション

    ```bash
    docker compose exec app alembic upgrade head
    ```

## 🔸 起動確認

[https://localhost](https://localhost) にアクセスして、以下のレスポンスが返ってきたら完了

```
{"message": "Hello world"}
```
