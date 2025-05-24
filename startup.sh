#!/bin/bash

# pip で必要なものをグローバルインストール
pip install --upgrade pip
pip install -r requirements.txt

# アプリケーションを起動
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app

