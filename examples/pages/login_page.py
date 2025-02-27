"""
ログインページのサンプル実装。
実際のプロジェクトでは、このようなページオブジェクトを作成します。
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_web_testing.src.base_page import BasePage


class LoginPage(BasePage):
    """ログインページのページオブジェクト"""
    
    # ページのURL
    URL_PATH = "login"
    
    # ページ内の要素のロケーター
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    
    def __init__(self, driver: WebDriver, base_url: str):
        """
        LoginPageクラスの初期化
        
        Args:
            driver: Seleniumのwebdriverインスタンス
            base_url: ベースURL
        """
        super().__init__(driver, base_url)
    
    def open_login_page(self):
        """ログインページを開く"""
        return self.open(self.URL_PATH)
    
    def login(self, username: str, password: str):
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
    
    def get_error_message(self) -> str:
        """
        エラーメッセージを取得する
        
        Returns:
            str: エラーメッセージ
        """
        return self.actions.get_text(self.ERROR_MESSAGE)
    
    def is_username_field_displayed(self) -> bool:
        """
        ユーザー名フィールドが表示されているかどうかを確認する
        
        Returns:
            bool: 表示されている場合はTrue、そうでない場合はFalse
        """
        return self.actions.is_element_present(self.USERNAME_FIELD)
    
    def is_error_message_displayed(self) -> bool:
        """
        エラーメッセージが表示されているかどうかを確認する
        
        Returns:
            bool: 表示されている場合はTrue、そうでない場合はFalse
        """
        return self.actions.is_element_present(self.ERROR_MESSAGE)