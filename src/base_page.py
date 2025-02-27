"""
ベースページクラス。
すべてのページオブジェクトの基底クラスとして機能します。
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from selenium_web_testing.src.page_actions import PageActions
from selenium_web_testing.config import settings


class BasePage:
    """ページオブジェクトの基底クラス"""
    
    def __init__(self, driver: WebDriver, base_url: str = settings.BASE_URL):
        """
        BasePage クラスの初期化
        
        Args:
            driver: Seleniumのwebdriverインスタンス
            base_url: ベースURL
        """
        self.driver = driver
        self.base_url = base_url
        self.actions = PageActions(driver)
    
    def open(self, path: str = ""):
        """
        指定されたパスのページを開く
        
        Args:
            path: ページのパス
        """
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(url)
        self.actions.wait_for_page_load()
        return self
    
    def get_title(self) -> str:
        """
        ページのタイトルを取得する
        
        Returns:
            str: ページのタイトル
        """
        return self.driver.title
    
    def get_current_url(self) -> str:
        """
        現在のURLを取得する
        
        Returns:
            str: 現在のURL
        """
        return self.driver.current_url
    
    def navigate_back(self):
        """ブラウザの戻るボタンを押す"""
        self.driver.back()
        self.actions.wait_for_page_load()
        return self
    
    def navigate_forward(self):
        """ブラウザの進むボタンを押す"""
        self.driver.forward()
        self.actions.wait_for_page_load()
        return self
    
    def refresh(self):
        """ページを更新する"""
        self.driver.refresh()
        self.actions.wait_for_page_load()
        return self
    
    def execute_script(self, script: str, *args):
        """
        JavaScriptを実行する
        
        Args:
            script: 実行するJavaScript
            *args: スクリプトに渡す引数
            
        Returns:
            実行結果
        """
        return self.driver.execute_script(script, *args)
    
    def wait_for_url_contains(self, text: str, timeout: int = None):
        """
        URLに特定のテキストが含まれるまで待機する
        
        Args:
            text: URLに含まれるべきテキスト
            timeout: 待機時間（秒）
        """
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(text)
        )
        return self
    
    def wait_for_title_contains(self, text: str, timeout: int = None):
        """
        タイトルに特定のテキストが含まれるまで待機する
        
        Args:
            text: タイトルに含まれるべきテキスト
            timeout: 待機時間（秒）
        """
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(
            EC.title_contains(text)
        )
        return self
    
    def take_screenshot(self, filename: str) -> str:
        """
        スクリーンショットを撮る
        
        Args:
            filename: ファイル名
            
        Returns:
            str: スクリーンショットのパス
        """
        return self.actions.take_screenshot(filename)