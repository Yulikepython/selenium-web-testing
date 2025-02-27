"""
ログインページのテストサンプル。
このテストでは、ログインページの機能をテストします。
"""

import pytest
from selenium_web_testing.examples.pages.login_page import LoginPage


@pytest.mark.usefixtures("driver")
class TestLogin:
    """ログインページのテストクラス"""
    
    def test_login_page_loads(self, base_url):
        """ログインページが正しく読み込まれることを確認するテスト"""
        # ログインページをインスタンス化
        login_page = LoginPage(self.driver, base_url)
        
        # ログインページを開く
        login_page.open_login_page()
        
        # ページのタイトルを確認
        assert "Login" in login_page.get_title(), "ログインページのタイトルが正しくありません"
        
        # ユーザー名フィールドが表示されていることを確認
        assert login_page.is_username_field_displayed(), "ユーザー名フィールドが表示されていません"
    
    def test_invalid_login(self, base_url):
        """無効なログイン情報でログインが失敗することを確認するテスト"""
        # ログインページをインスタンス化
        login_page = LoginPage(self.driver, base_url)
        
        # ログインページを開く
        login_page.open_login_page()
        
        # 無効なログイン情報でログイン
        login_page.login("invalid_user", "invalid_password")
        
        # エラーメッセージが表示されることを確認
        assert login_page.is_error_message_displayed(), "エラーメッセージが表示されていません"
        
        # エラーメッセージが正しいことを確認
        error_message = login_page.get_error_message()
        assert "Invalid username or password" in error_message, f"エラーメッセージが正しくありません: {error_message}"
    
    @pytest.mark.parametrize("username,password", [
        ("user1", "password1"),
        ("user2", "password2"),
        ("user3", "password3")
    ])
    def test_multiple_login_attempts(self, base_url, username, password):
        """
        複数のログイン情報でテストを行う
        
        Args:
            base_url: ベースURL
            username: ユーザー名
            password: パスワード
        """
        # ログインページをインスタンス化
        login_page = LoginPage(self.driver, base_url)
        
        # ログインページを開く
        login_page.open_login_page()
        
        # パラメータ化されたログイン情報でログイン
        login_page.login(username, password)
        
        # 実際のアプリケーションでは、ログイン成功後の状態を確認する必要があります
        # 例えば、リダイレクト先のURLやエラーメッセージなど
        assert True, "このテストは実際のアプリケーションに合わせて実装してください"