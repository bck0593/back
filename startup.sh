#!/bin/bash

# pipを最新版にアップグレード
pip install --upgrade pip

# 依存パッケージをインストール
pip install -r requirements.txt

# アプリケーションをgunicornで起動（4ワーカー・uvicornワーカー）
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000
