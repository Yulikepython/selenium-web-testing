"""
ホームページのテストサンプル。
"""

import pytest
from selenium_web_testing.examples.pages.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestHome:
    """ホームページのテストクラス"""
    
    def test_home_page_loads(self, base_url):
        """ホームページが正しく読み込まれることを確認するテスト"""
        # ホームページをインスタンス化
        home_page = HomePage(self.driver, base_url)
        
        # ホームページを開く
        home_page.open_home_page()
        
        # ページのタイトルを確認
        assert "Home" in home_page.get_title(), "ホームページのタイトルが正しくありません"
        
        # ウェルカムメッセージが表示されていることを確認
        welcome_message = home_page.get_welcome_message()
        assert "Welcome" in welcome_message, f"ウェルカムメッセージが正しくありません: {welcome_message}"
    
    def test_navigation_links(self, base_url):
        """ナビゲーションリンクが正しく表示されることを確認するテスト"""
        # ホームページをインスタンス化
        home_page = HomePage(self.driver, base_url)
        
        # ホームページを開く
        home_page.open_home_page()
        
        # ナビゲーションリンクのテキストを取得
        nav_links = home_page.get_navigation_link_texts()
        
        # 期待されるナビゲーションリンク
        expected_links = ["Home", "About", "Contact", "Login"]
        
        # 全ての期待されるリンクが存在することを確認
        for link in expected_links:
            assert link in nav_links, f"ナビゲーションリンク '{link}' が見つかりません"
    
    def test_login_link(self, base_url):
        """ログインリンクをクリックするとログインページに移動することを確認するテスト"""
        # ホームページをインスタンス化
        home_page = HomePage(self.driver, base_url)
        
        # ホームページを開く
        home_page.open_home_page()
        
        # ログインリンクをクリック
        login_page = home_page.click_login_link()
        
        # ログインページに移動したことを確認
        assert "login" in login_page.get_current_url().lower(), "ログインページに移動していません"
        assert "Login" in login_page.get_title(), "ログインページのタイトルが正しくありません"
    
    def test_search_functionality(self, base_url):
        """検索機能が正しく動作することを確認するテスト"""
        # ホームページをインスタンス化
        home_page = HomePage(self.driver, base_url)
        
        # ホームページを開く
        home_page.open_home_page()
        
        # 検索を実行
        search_query = "test"
        home_page.search(search_query)
        
        # 検索結果ページに移動したことを確認
        # 実際のアプリケーションに合わせて確認方法を実装
        assert "search" in home_page.get_current_url().lower(), "検索結果ページに移動していません"
        
        # 検索クエリがURLに含まれていることを確認
        assert search_query in home_page.get_current_url(), f"検索クエリ '{search_query}' がURLに含まれていません"