#!/bin/bash

# 依存パッケージをインストール
pip install --upgrade pip
pip install -r requirements.txt

# アプリケーションを起動
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000

