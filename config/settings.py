"""
テスト設定ファイル。
ここにテスト対象のURLやブラウザの設定を記述します。
"""

# テスト対象のベースURL
BASE_URL = "https://example.com"

# ブラウザ設定 (chrome, firefox, edge, safari)
BROWSER = "chrome"

# ブラウザのオプション
HEADLESS = False  # ヘッドレスモード（画面表示なし）
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# 待機時間設定（秒）
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20

# スクリーンショット設定
SCREENSHOT_DIR = "screenshots"
TAKE_SCREENSHOT_ON_FAILURE = True