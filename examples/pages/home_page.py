"""
ホームページのサンプル実装。
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_web_testing.src.base_page import BasePage


class HomePage(BasePage):
    """ホームページのページオブジェクト"""
    
    # ページのURL
    URL_PATH = ""
    
    # ページ内の要素のロケーター
    WELCOME_MESSAGE = (By.CSS_SELECTOR, ".welcome-message")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login']")
    SEARCH_BOX = (By.ID, "search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-button")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav.main-nav")
    NAVIGATION_LINKS = (By.CSS_SELECTOR, "nav.main-nav a")
    
    def __init__(self, driver: WebDriver, base_url: str):
        """
        HomePageクラスの初期化
        
        Args:
            driver: Seleniumのwebdriverインスタンス
            base_url: ベースURL
        """
        super().__init__(driver, base_url)
    
    def open_home_page(self):
        """ホームページを開く"""
        return self.open(self.URL_PATH)
    
    def get_welcome_message(self) -> str:
        """
        ウェルカムメッセージを取得する
        
        Returns:
            str: ウェルカムメッセージ
        """
        return self.actions.get_text(self.WELCOME_MESSAGE)
    
    def click_login_link(self):
        """ログインリンクをクリックする"""
        self.actions.click(self.LOGIN_LINK)
        from selenium_web_testing.examples.pages.login_page import LoginPage
        return LoginPage(self.driver, self.base_url)
    
    def search(self, query: str):
        """
        検索を行う
        
        Args:
            query: 検索クエリ
        """
        self.actions.type_text(self.SEARCH_BOX, query)
        self.actions.click(self.SEARCH_BUTTON)
        return self
    
    def get_navigation_links(self) -> list:
        """
        ナビゲーションリンクのリストを取得する
        
        Returns:
            list: ナビゲーションリンクのリスト
        """
        return self.actions.find_all(self.NAVIGATION_LINKS)
    
    def get_navigation_link_texts(self) -> list:
        """
        ナビゲーションリンクのテキストのリストを取得する
        
        Returns:
            list: ナビゲーションリンクのテキストのリスト
        """
        links = self.get_navigation_links()
        return [link.text for link in links]
    
    def click_navigation_link(self, link_text: str):
        """
        指定されたテキストのナビゲーションリンクをクリックする
        
        Args:
            link_text: クリックするリンクのテキスト
        """
        links = self.get_navigation_links()
        for link in links:
            if link.text == link_text:
                link.click()
                return self
        
        raise ValueError(f"リンクが見つかりません: {link_text}")