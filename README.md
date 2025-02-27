# Selenium Web Testing Framework

Python を使用した Selenium ウェブテストフレームワークです。このフレームワークは Pytest と組み合わせて、ウェブアプリケーションを効率的にテストするための基盤を提供します。

## 特徴

- **設定ファイルベース**: テスト設定をコードから分離
- **ページオブジェクトモデル**: テストとページの実装を分離して保守性を高める
- **ユーティリティクラス**: よく使われる Selenium の操作をラップして使いやすく
- **クロスブラウザサポート**: Chrome、Firefox、Edge、Safari に対応
- **スクリーンショット自動取得**: テスト失敗時に自動でスクリーンショットを取得
- **詳細なドキュメント**: すべてのクラスとメソッドに詳細なドキュメントを提供

## 要件

- Python 3.7 以上
- pytest 7.4.0
- selenium 4.11.2
- webdriver-manager 4.0.0

## インストール

```bash
# リポジトリをクローン
git clone https://github.com/yourusername/selenium-web-testing.git
cd selenium-web-testing

# 必要に応じて、仮想環境を作成
python -m venv venv
source venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

## 使用方法

### クイックスタート

このプロジェクトを動作させるための最小限のコマンドは以下の通りです：

```bash
# 仮想環境を有効化
source venv/bin/activate

# 一番シンプルなブラウザテストを実行
pytest examples/tests/test_raw_selenium.py::TestRawSelenium::test_website_title -v

# Google検索テストを実行（実用的なSeleniumの使用例）
pytest examples/tests/test_login.py -v

# 設定したサイトへのアクセステスト
pytest examples/tests/test_home.py -v

# すべてのサンプルテストを実行
pytest examples/tests/ -v

# ヘッドレスモードでテストを実行（画面表示なし、CI環境に最適）
pytest examples/tests/ --headless 
```

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
from src.base_page import BasePage

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
from examples.pages.login_page import LoginPage

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
pytest examples/tests/test_login.py

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

### 動作確認の詳細

このプロジェクトには複数のテストが含まれています。選択肢として使えるテストは以下の通りです：

```bash
# 仮想環境を有効化
source venv/bin/activate

# 1. 最もシンプルなテスト（設定したサイトにアクセスし基本情報を取得）
pytest examples/tests/test_home.py -v

# 2. Seleniumを使った基本操作テスト（実際のGoogle検索を実行）
pytest examples/tests/test_login.py -v

# 3. シンプルなWebサイトアクセスとJavaScript実行テスト
pytest examples/tests/test_raw_selenium.py -v

# ヘッドレスモードでテストを実行（画面表示なし）
pytest examples/tests/ --headless

# ブラウザを指定してテストを実行（chromeの代わりにfirefoxを使用）
pytest examples/tests/ --browser firefox
```

各テストは実際のウェブサイトにアクセスし、基本的なSelenium操作を行います。失敗時は自動的にスクリーンショットが保存されます。

## トラブルシューティング

よくある問題と解決方法：

1. **ImportError**: モジュールが見つからない場合は、正しいPython環境（venv）を有効化しているか確認してください。

2. **WebDriverException**: ブラウザドライバが見つからない場合、webdriver-managerが自動でドライバをダウンロードしますが、ネットワーク接続に問題がある可能性があります。

3. **テスト失敗**: テストが失敗した場合、`screenshots`ディレクトリに自動保存されたスクリーンショットを確認して問題の原因を特定してください。

4. **パスの問題**: importエラーが発生する場合は、プロジェクトのルートディレクトリからコマンドを実行しているか確認してください。

## ライセンス

MIT
