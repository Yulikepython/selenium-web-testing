# Selenium Web Testing Framework

Pythonを使用したSeleniumウェブテストフレームワークです。このフレームワークはPytestと組み合わせて、ウェブアプリケーションを効率的にテストするための基盤を提供します。

## 特徴

- **設定ファイルベース**: テスト設定をコードから分離
- **ページオブジェクトモデル**: テストとページの実装を分離して保守性を高める
- **ユーティリティクラス**: よく使われるSeleniumの操作をラップして使いやすく
- **クロスブラウザサポート**: Chrome、Firefox、Edge、Safariに対応
- **スクリーンショット自動取得**: テスト失敗時に自動でスクリーンショットを取得
- **詳細なドキュメント**: すべてのクラスとメソッドに詳細なドキュメントを提供

## 要件

- Python 3.7以上
- pytest 7.4.0
- selenium 4.11.2
- webdriver-manager 4.0.0

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/selenium-web-testing.git
cd selenium-web-testing

# 依存関係をインストール
pip install -r requirements.txt
```

## 使用方法

### 設定

`config/settings.py` ファイルでテストの基本設定を行います：

```python
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
```

### ページオブジェクト作成

新しいページオブジェクトを作成するには、`BasePage` クラスを継承します：

```python
from selenium.webdriver.common.by import By
from selenium_web_testing.src.base_page import BasePage

class LoginPage(BasePage):
    # ページのURL
    URL_PATH = "login"
    
    # ページ内の要素のロケーター
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    def login(self, username, password):
        self.actions.type_text(self.USERNAME_FIELD, username)
        self.actions.type_text(self.PASSWORD_FIELD, password)
        self.actions.click(self.LOGIN_BUTTON)
        return self
```

### テスト作成

テストを作成するには、ページオブジェクトを使います：

```python
import pytest
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestLogin:
    def test_login_process(self, base_url):
        # ログインページをインスタンス化
        login_page = LoginPage(self.driver, base_url)
        
        # ログインページを開く
        login_page.open_login_page()
        
        # ログインを実行
        login_page.login("testuser", "password")
        
        # アサーション
        assert "dashboard" in self.driver.current_url
```

### テスト実行

```bash
# すべてのテストを実行
pytest

# 特定のテストを実行
pytest tests/test_login.py

# ブラウザを指定してテストを実行
pytest --browser firefox

# ヘッドレスモードでテストを実行
pytest --headless

# ベースURLを指定してテストを実行
pytest --base-url https://staging.example.com

# HTMLレポートを生成
pytest --html=report.html
```

## ディレクトリ構造

```
selenium-web-testing/
├── config/
│   ├── __init__.py
│   └── settings.py         # テスト設定
├── src/
│   ├── __init__.py
│   ├── page_actions.py     # ページアクション・ユーティリティ
│   └── base_page.py        # ベースページクラス
├── examples/
│   ├── pages/              # ページオブジェクトの例
│   │   ├── __init__.py
│   │   ├── home_page.py
│   │   └── login_page.py
│   └── tests/              # テストの例
│       ├── __init__.py
│       ├── test_home.py
│       └── test_login.py
├── tests/                  # フレームワークのユニットテスト
│   ├── __init__.py
│   └── test_page_actions.py
├── conftest.py             # Pytestの共通設定
├── requirements.txt        # 依存関係
└── README.md               # ドキュメント
```

## サンプル

フレームワークの使用例は `examples` ディレクトリにあります：

- `examples/pages/`: ページオブジェクトの実装例
- `examples/tests/`: テストの実装例

## ライセンス

MIT