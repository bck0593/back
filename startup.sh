#!/bin/bash

# 仮想環境がなければ作成
python -m venv antenv
source antenv/bin/activate

# 依存パッケージをインストール
pip install --upgrade pip
pip install -r requirements.txt

# アプリケーションを起動
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
