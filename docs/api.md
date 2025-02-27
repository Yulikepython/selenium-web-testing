# API リファレンス

このドキュメントでは、Selenium Web Testingフレームワークの主要なクラスとメソッドについて説明します。

## 設定 (settings.py)

`config/settings.py` ファイルに含まれる設定オプション:

| 設定 | 説明 | デフォルト値 |
|-----|------|------------|
| `BASE_URL` | テスト対象のベースURL | `"https://example.com"` |
| `BROWSER` | 使用するブラウザ (chrome, firefox, edge, safari) | `"chrome"` |
| `HEADLESS` | ヘッドレスモードを有効にするかどうか | `False` |
| `WINDOW_WIDTH` | ブラウザウィンドウの幅 | `1920` |
| `WINDOW_HEIGHT` | ブラウザウィンドウの高さ | `1080` |
| `IMPLICIT_WAIT` | 暗黙的な待機時間（秒） | `10` |
| `EXPLICIT_WAIT` | 明示的な待機時間（秒） | `20` |
| `SCREENSHOT_DIR` | スクリーンショットを保存するディレクトリ | `"screenshots"` |
| `TAKE_SCREENSHOT_ON_FAILURE` | テスト失敗時にスクリーンショットを撮るかどうか | `True` |

## Pytestフィクスチャ (conftest.py)

| フィクスチャ | スコープ | 説明 |
|------------|---------|------|
| `base_url` | session | テスト対象のベースURLを返す |
| `driver` | class | WebDriverのセットアップとティアダウンを行う |
| `navigate` | function | 指定されたパスに移動するヘルパー関数 |

## PageActions クラス

`PageActions`クラスは、Seleniumの一般的な操作をラップし、より使いやすくするためのユーティリティクラスです。

### 初期化

```python
def __init__(self, driver: WebDriver):
    """
    PageActionsクラスの初期化
    
    Args:
        driver: Seleniumのwebdriverインスタンス
    """
```

### 要素の検索

```python
def find(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
    """
    要素を見つける
    
    Args:
        locator: (検索方法, 検索値)のタプル。例: (By.ID, "my-id")
        timeout: 待機時間（秒）、Noneの場合はデフォルト値を使用
        
    Returns:
        WebElement: 見つかった要素
        
    Raises:
        TimeoutException: 要素が見つからない場合
    """
```

```python
def find_all(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> list:
    """
    全ての一致する要素を見つける
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
        
    Returns:
        list: 見つかった要素のリスト
    """
```

### 要素の操作

```python
def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
    """
    要素をクリックする
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
    """
```

```python
def type_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None, clear_first: bool = True) -> None:
    """
    テキストを入力する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        text: 入力するテキスト
        timeout: 待機時間（秒）
        clear_first: 入力前にフィールドをクリアするかどうか
    """
```

```python
def scroll_to_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
    """
    要素までスクロールする
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
    """
```

```python
def hover_over(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
    """
    要素にマウスオーバーする
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
    """
```

### フォーム処理

```python
def select_dropdown_option_by_text(self, locator: Tuple[By, str], option_text: str, 
                                 timeout: Optional[int] = None) -> None:
    """
    ドロップダウンからテキストでオプションを選択する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        option_text: 選択するオプションのテキスト
        timeout: 待機時間（秒）
    """
```

```python
def select_dropdown_option_by_value(self, locator: Tuple[By, str], option_value: str,
                                  timeout: Optional[int] = None) -> None:
    """
    ドロップダウンから値でオプションを選択する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        option_value: 選択するオプションの値
        timeout: 待機時間（秒）
    """
```

### 要素の検証

```python
def is_element_present(self, locator: Tuple[By, str], timeout: int = 0) -> bool:
    """
    要素が存在するかどうかを確認する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
        
    Returns:
        bool: 要素が存在する場合はTrue、そうでない場合はFalse
    """
```

```python
def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
    """
    要素のテキストを取得する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
        
    Returns:
        str: 要素のテキスト
    """
```

```python
def get_attribute(self, locator: Tuple[By, str], attribute: str, timeout: Optional[int] = None) -> str:
    """
    要素の属性値を取得する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        attribute: 取得する属性の名前
        timeout: 待機時間（秒）
        
    Returns:
        str: 属性の値
    """
```

### 待機と同期

```python
def wait_for_element(self, locator: Tuple[By, str], timeout: Optional[int] = None, 
                   condition: str = "presence") -> WebElement:
    """
    要素が特定の状態になるまで待機する
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
        condition: 待機条件（presence, visibility, clickable）
        
    Returns:
        WebElement: 条件を満たした要素
    """
```

```python
def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
    """
    ページの読み込みが完了するまで待機する
    
    Args:
        timeout: 待機時間（秒）
    """
```

### フレームと警告

```python
def switch_to_iframe(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
    """
    iframeに切り替える
    
    Args:
        locator: (検索方法, 検索値)のタプル
        timeout: 待機時間（秒）
    """
```

```python
def switch_to_default_content(self) -> None:
    """
    デフォルトのコンテンツに戻る
    """
```

```python
def accept_alert(self, timeout: Optional[int] = None) -> None:
    """
    アラートを受け入れる
    
    Args:
        timeout: 待機時間（秒）
    """
```

```python
def dismiss_alert(self, timeout: Optional[int] = None) -> None:
    """
    アラートを却下する
    
    Args:
        timeout: 待機時間（秒）
    """
```

### ユーティリティ

```python
def take_screenshot(self, filename: str) -> str:
    """
    スクリーンショットを撮る
    
    Args:
        filename: 保存するファイル名
        
    Returns:
        str: スクリーンショットのパス
    """
```

## BasePage クラス

`BasePage`クラスは、すべてのページオブジェクトの基底クラスです。

### 初期化

```python
def __init__(self, driver: WebDriver, base_url: str = settings.BASE_URL):
    """
    BasePage クラスの初期化
    
    Args:
        driver: Seleniumのwebdriverインスタンス
        base_url: ベースURL
    """
```

### ページナビゲーション

```python
def open(self, path: str = ""):
    """
    指定されたパスのページを開く
    
    Args:
        path: ページのパス
    """
```

```python
def navigate_back(self):
    """ブラウザの戻るボタンを押す"""
```

```python
def navigate_forward(self):
    """ブラウザの進むボタンを押す"""
```

```python
def refresh(self):
    """ページを更新する"""
```

### ページ情報

```python
def get_title(self) -> str:
    """
    ページのタイトルを取得する
    
    Returns:
        str: ページのタイトル
    """
```

```python
def get_current_url(self) -> str:
    """
    現在のURLを取得する
    
    Returns:
        str: 現在のURL
    """
```

### JavaScript実行

```python
def execute_script(self, script: str, *args):
    """
    JavaScriptを実行する
    
    Args:
        script: 実行するJavaScript
        *args: スクリプトに渡す引数
        
    Returns:
        実行結果
    """
```

### 待機

```python
def wait_for_url_contains(self, text: str, timeout: int = None):
    """
    URLに特定のテキストが含まれるまで待機する
    
    Args:
        text: URLに含まれるべきテキスト
        timeout: 待機時間（秒）
    """
```

```python
def wait_for_title_contains(self, text: str, timeout: int = None):
    """
    タイトルに特定のテキストが含まれるまで待機する
    
    Args:
        text: タイトルに含まれるべきテキスト
        timeout: 待機時間（秒）
    """
```

### スクリーンショット

```python
def take_screenshot(self, filename: str) -> str:
    """
    スクリーンショットを撮る
    
    Args:
        filename: ファイル名
        
    Returns:
        str: スクリーンショットのパス
    """
```