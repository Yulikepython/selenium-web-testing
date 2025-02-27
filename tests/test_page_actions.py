"""
PageActionsクラスのユニットテスト
"""

import pytest
from unittest.mock import MagicMock, patch
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium_web_testing.src.page_actions import PageActions


class TestPageActions:
    """PageActionsクラスのテスト"""
    
    @pytest.fixture
    def mock_driver(self):
        """モックドライバを作成するフィクスチャ"""
        driver = MagicMock()
        return driver
    
    @pytest.fixture
    def page_actions(self, mock_driver):
        """PageActionsインスタンスを作成するフィクスチャ"""
        return PageActions(mock_driver)
    
    def test_find(self, page_actions, mock_driver):
        """find関数のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element
        
        # findメソッドをパッチ
        with patch('selenium.webdriver.support.ui.WebDriverWait.until', return_value=mock_element):
            # テスト対象の関数を呼び出す
            element = page_actions.find((By.ID, "test-id"))
            
            # アサーション
            assert element == mock_element
    
    def test_click(self, page_actions):
        """click関数のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        
        # findメソッドをパッチ
        with patch.object(page_actions, 'find', return_value=mock_element):
            # テスト対象の関数を呼び出す
            page_actions.click((By.ID, "test-id"))
            
            # アサーション
            mock_element.click.assert_called_once()
    
    def test_type_text(self, page_actions):
        """type_text関数のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        
        # findメソッドをパッチ
        with patch.object(page_actions, 'find', return_value=mock_element):
            # テスト対象の関数を呼び出す
            page_actions.type_text((By.ID, "test-id"), "test text")
            
            # アサーション
            mock_element.clear.assert_called_once()
            mock_element.send_keys.assert_called_once_with("test text")
    
    def test_type_text_no_clear(self, page_actions):
        """type_text関数（クリアしない）のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        
        # findメソッドをパッチ
        with patch.object(page_actions, 'find', return_value=mock_element):
            # テスト対象の関数を呼び出す
            page_actions.type_text((By.ID, "test-id"), "test text", clear_first=False)
            
            # アサーション
            mock_element.clear.assert_not_called()
            mock_element.send_keys.assert_called_once_with("test text")
    
    def test_is_element_present_true(self, page_actions, mock_driver):
        """is_element_present関数（要素が存在する場合）のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        mock_driver.find_element.return_value = mock_element
        
        # テスト対象の関数を呼び出す
        result = page_actions.is_element_present((By.ID, "test-id"))
        
        # アサーション
        assert result is True
    
    def test_is_element_present_false(self, page_actions, mock_driver):
        """is_element_present関数（要素が存在しない場合）のテスト"""
        # 例外を発生させる
        mock_driver.find_element.side_effect = NoSuchElementException("Element not found")
        
        # テスト対象の関数を呼び出す
        result = page_actions.is_element_present((By.ID, "test-id"))
        
        # アサーション
        assert result is False
    
    def test_get_text(self, page_actions):
        """get_text関数のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        mock_element.text = "test text"
        
        # findメソッドをパッチ
        with patch.object(page_actions, 'find', return_value=mock_element):
            # テスト対象の関数を呼び出す
            text = page_actions.get_text((By.ID, "test-id"))
            
            # アサーション
            assert text == "test text"
    
    def test_get_attribute(self, page_actions):
        """get_attribute関数のテスト"""
        # モックエレメントを設定
        mock_element = MagicMock()
        mock_element.get_attribute.return_value = "test value"
        
        # findメソッドをパッチ
        with patch.object(page_actions, 'find', return_value=mock_element):
            # テスト対象の関数を呼び出す
            value = page_actions.get_attribute((By.ID, "test-id"), "test-attr")
            
            # アサーション
            assert value == "test value"
            mock_element.get_attribute.assert_called_once_with("test-attr")