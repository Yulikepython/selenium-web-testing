"""
生のSeleniumを使用したテストサンプル。
ページオブジェクトを使用せずに、Seleniumの基本的な使い方を示します。
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.usefixtures("driver")
class TestRawSelenium:
    """生のSeleniumを使用したテストクラス"""
    
    def test_simple_google_search(self, navigate):
        """シンプルなGoogle検索のテスト"""
        # Googleのホームページに移動
        navigate("https://www.google.com")
        
        # 検索ボックスを探す
        search_box = self.driver.find_element(By.NAME, "q")
        
        # 検索ワードを入力
        search_box.send_keys("Selenium Python")
        
        # 検索ボタンをクリック
        search_box.submit()
        
        # 検索結果ページが表示されるまで待機
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Selenium Python")
        )
        
        # タイトルに検索ワードが含まれていることを確認
        assert "Selenium Python" in self.driver.title
    
    def test_explicit_wait(self, navigate):
        """明示的な待機を使用したテスト"""
        # Wikipediaのホームページに移動
        navigate("https://www.wikipedia.org")
        
        # 検索ボックスを探す
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchInput"))
        )
        
        # 検索ワードを入力
        search_box.send_keys("Selenium (software)")
        
        # 検索ボタンをクリック
        search_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        search_button.click()
        
        # ページが読み込まれるまで待機
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstHeading"))
        )
        
        # ページのタイトルが正しいことを確認
        heading = self.driver.find_element(By.ID, "firstHeading")
        assert "Selenium" in heading.text
    
    def test_multiple_elements(self, navigate):
        """複数の要素を扱うテスト"""
        # Wikipediaのホームページに移動
        navigate("https://www.wikipedia.org")
        
        # 全ての言語リンクを取得
        language_links = self.driver.find_elements(By.CSS_SELECTOR, ".central-featured-lang")
        
        # 少なくとも10の言語リンクが存在することを確認
        assert len(language_links) >= 10, f"言語リンクが少なくとも10個存在することを期待していましたが、{len(language_links)}個しか見つかりませんでした"
        
        # 英語のリンクが存在することを確認
        english_link_found = False
        for link in language_links:
            if "English" in link.text:
                english_link_found = True
                break
        
        assert english_link_found, "英語のリンクが見つかりませんでした"
    
    def test_javascript_execution(self, navigate):
        """JavaScriptを実行するテスト"""
        # Wikipediaのホームページに移動
        navigate("https://www.wikipedia.org")
        
        # JavaScriptを使用してページのタイトルを変更
        new_title = "Modified by Selenium"
        self.driver.execute_script(f"document.title = '{new_title}';")
        
        # タイトルが変更されたことを確認
        assert self.driver.title == new_title
        
        # JavaScriptを使用してページをスクロール
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # スクロール位置を確認
        scroll_position = self.driver.execute_script("return window.pageYOffset;")
        assert scroll_position > 0