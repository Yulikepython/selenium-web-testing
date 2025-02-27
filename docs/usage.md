# 使用方法

このドキュメントでは、Selenium Web Testingフレームワークの使い方を詳しく説明します。

## 基本概念

このフレームワークは以下の主要なコンポーネントで構成されています：

1. **設定（config）**: テスト環境の設定
2. **ページアクション（PageActions）**: Seleniumの操作をラップしたユーティリティ
3. **ベースページ（BasePage）**: すべてのページオブジェクトの基底クラス
4. **ページオブジェクト**: 各Webページを表すクラス
5. **テストクラス**: 実際のテスト

## フレームワークの設定

### 設定ファイル

`config/settings.py` ファイルでグローバル設定を行います：

```python
# テスト対象のベースURL
BASE_URL = "https://example.com"

# ブラウザ設定 (chrome, firefox, edge, safari)
BROWSER = "chrome"

# ブラウザのオプション
HEADLESS = False
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

# 待機時間設定（秒）
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 20

# スクリーンショット設定
SCREENSHOT_DIR = "screenshots"
TAKE_SCREENSHOT_ON_FAILURE = True
```

## ページオブジェクトの作成

### ベースページ

すべてのページオブジェクトは`BasePage`クラスを継承します：

```python
from selenium_web_testing.src.base_page import BasePage

class MyPage(BasePage):
    # ページの実装
    pass
```

### ページ要素の定義

ページ内の要素はクラス変数として定義します：

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
```

### ページメソッドの実装

ページの操作をメソッドとして実装します：

```python
def login(self, username, password):
    """
    ログインを行う
    
    Args:
        username: ユーザー名
        password: パスワード
    """
    self.actions.type_text(self.USERNAME_FIELD, username)
    self.actions.type_text(self.PASSWORD_FIELD, password)
    self.actions.click(self.LOGIN_BUTTON)
    return self
```

## テストの作成

### Pytestフィクスチャの使用

テストクラスには`driver`フィクスチャを使用します：

```python
import pytest

@pytest.mark.usefixtures("driver")
class TestExample:
    def test_something(self, base_url):
        # テスト実装
        pass
```

### ページオブジェクトの使用

テスト内でページオブジェクトを使用します：

```python
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

### パラメータ化テスト

複数のデータセットでテストを実行するには：

```python
@pytest.mark.parametrize("username,password,expected", [
    ("user1", "pass1", True),
    ("user2", "pass2", False),
    ("user3", "pass3", True)
])
def test_multiple_logins(self, base_url, username, password, expected):
    login_page = LoginPage(self.driver, base_url)
    login_page.open_login_page()
    login_page.login(username, password)
    
    # 期待される結果を確認
    is_logged_in = "dashboard" in self.driver.current_url
    assert is_logged_in == expected
```

## Page Actionsの使用

### 要素の取得

```python
# 要素を見つける
element = self.actions.find((By.ID, "my-element"))

# 全ての一致する要素を見つける
elements = self.actions.find_all((By.CSS_SELECTOR, ".item"))
```

### 要素の操作

```python
# クリック
self.actions.click((By.ID, "button"))

# テキスト入力
self.actions.type_text((By.ID, "input"), "Hello World")

# ドロップダウン選択
self.actions.select_dropdown_option_by_text((By.ID, "dropdown"), "Option 1")
```

### 要素の検証

```python
# 要素が存在するか確認
is_present = self.actions.is_element_present((By.ID, "element"))

# 要素のテキストを取得
text = self.actions.get_text((By.ID, "element"))

# 要素の属性を取得
attr = self.actions.get_attribute((By.ID, "element"), "href")
```

### 待機と同期

```python
# 要素が特定の状態になるまで待機
self.actions.wait_for_element((By.ID, "element"), condition="clickable")

# ページの読み込みが完了するまで待機
self.actions.wait_for_page_load()
```

## テストの実行

### 通常実行

```bash
# すべてのテストを実行
pytest

# 特定のテストを実行
pytest tests/test_login.py

# 特定のテストクラスを実行
pytest tests/test_login.py::TestLogin

# 特定のテストメソッドを実行
pytest tests/test_login.py::TestLogin::test_login_process
```

### パラメータ指定

```bash
# ブラウザを指定
pytest --browser firefox

# ヘッドレスモード
pytest --headless

# ベースURLを指定
pytest --base-url https://staging.example.com
```

### レポート生成

```bash
# HTMLレポートを生成
pytest --html=report.html

# JUnitレポートを生成
pytest --junitxml=report.xml
```

## 実際の使用例

より詳細な使用例は `examples` ディレクトリを参照してください。これには以下が含まれます：

- ページオブジェクトの例 (`examples/pages/`)
- テストの例 (`examples/tests/`)

これらの例は、フレームワークの実際の使用方法を示しています。