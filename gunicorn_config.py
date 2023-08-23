# gunicorn_config.py

# Gunicornが使用するワーカープロセスの数
workers = 4

# LINEボットアプリケーションのエントリポイント（アプリケーションオブジェクトを含むモジュールのパス）
app_module = 'main:app'

# リクエストを待ち受けるポート
bind = '0.0.0.0:443'

# ログファイルの設定
accesslog = '-'  # 標準出力にログを出力
errorlog = '-'   # 標準出力にエラーログを出力
