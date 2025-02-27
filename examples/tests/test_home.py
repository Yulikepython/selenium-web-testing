"""
簡単なブラウザテストのサンプル。
"""

import pytest


@pytest.mark.usefixtures("driver")
class TestSite:
    """基本的なWebサイトアクセスのテスト"""
    
    def test_site_loads(self, base_url):
        """設定されたサイトが正しく読み込まれることを確認するテスト"""
        # 設定されたURLに移動
        self.driver.get(base_url)
        
        # タイトルが存在することを確認
        assert self.driver.title is not None, "ページタイトルが取得できません"
        print(f"ページタイトル: {self.driver.title}")
        
        # ページソースが取得できることを確認
        assert len(self.driver.page_source) > 0, "ページソースが取得できません"
        
        # 現在のURLを確認
        current_url = self.driver.current_url
        assert current_url.startswith("http"), f"URLが正しくありません: {current_url}"