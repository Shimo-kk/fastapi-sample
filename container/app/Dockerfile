FROM python:3.12-alpine3.19

# ワークディレクトリの指定
WORKDIR /src

# 環境変数の設定
ENV PYTHONPATH /src
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPYCACHEPREFIX=/var/cache/python

# ソースコードをコピー
COPY /src /src

# パッケージのインストール
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 8000番を公開
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--reload", "--port", "8000", "--host", "0.0.0.0"]
