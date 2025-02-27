"""
ページ操作のためのユーティリティ関数。
Seleniumの一般的な操作をラップし、より使いやすくします。
"""

from typing import Optional, Union, Tuple

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium_web_testing.config import settings


class PageActions:
    """ページ操作のためのユーティリティクラス"""

    def __init__(self, driver: WebDriver):
        """
        PageActionsクラスの初期化
        
        Args:
            driver: Seleniumのwebdriverインスタンス
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
    
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
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def find_all(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> list:
        """
        全ての一致する要素を見つける
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
            
        Returns:
            list: 見つかった要素のリスト
        """
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return self.driver.find_elements(*locator)
    
    def click(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        要素をクリックする
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
        """
        element = self.find(locator, timeout)
        element.click()
    
    def type_text(self, locator: Tuple[By, str], text: str, timeout: Optional[int] = None, clear_first: bool = True) -> None:
        """
        テキストを入力する
        
        Args:
            locator: (検索方法, 検索値)のタプル
            text: 入力するテキスト
            timeout: 待機時間（秒）
            clear_first: 入力前にフィールドをクリアするかどうか
        """
        element = self.find(locator, timeout)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def is_element_present(self, locator: Tuple[By, str], timeout: int = 0) -> bool:
        """
        要素が存在するかどうかを確認する
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
            
        Returns:
            bool: 要素が存在する場合はTrue、そうでない場合はFalse
        """
        try:
            if timeout > 0:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
            else:
                self.driver.find_element(*locator)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
    
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
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        wait = WebDriverWait(self.driver, timeout)
        
        if condition == "presence":
            return wait.until(EC.presence_of_element_located(locator))
        elif condition == "visibility":
            return wait.until(EC.visibility_of_element_located(locator))
        elif condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        else:
            raise ValueError(f"サポートされていない待機条件: {condition}")
    
    def get_text(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> str:
        """
        要素のテキストを取得する
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
            
        Returns:
            str: 要素のテキスト
        """
        element = self.find(locator, timeout)
        return element.text
    
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
        element = self.find(locator, timeout)
        return element.get_attribute(attribute)
    
    def scroll_to_element(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        要素までスクロールする
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
        """
        element = self.find(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        要素にマウスオーバーする
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
        """
        element = self.find(locator, timeout)
        ActionChains(self.driver).move_to_element(element).perform()
    
    def select_dropdown_option_by_text(self, locator: Tuple[By, str], option_text: str, 
                                     timeout: Optional[int] = None) -> None:
        """
        ドロップダウンからテキストでオプションを選択する
        
        Args:
            locator: (検索方法, 検索値)のタプル
            option_text: 選択するオプションのテキスト
            timeout: 待機時間（秒）
        """
        from selenium.webdriver.support.ui import Select
        
        element = self.find(locator, timeout)
        select = Select(element)
        select.select_by_visible_text(option_text)
    
    def select_dropdown_option_by_value(self, locator: Tuple[By, str], option_value: str,
                                      timeout: Optional[int] = None) -> None:
        """
        ドロップダウンから値でオプションを選択する
        
        Args:
            locator: (検索方法, 検索値)のタプル
            option_value: 選択するオプションの値
            timeout: 待機時間（秒）
        """
        from selenium.webdriver.support.ui import Select
        
        element = self.find(locator, timeout)
        select = Select(element)
        select.select_by_value(option_value)
    
    def wait_for_page_load(self, timeout: Optional[int] = None) -> None:
        """
        ページの読み込みが完了するまで待機する
        
        Args:
            timeout: 待機時間（秒）
        """
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    
    def switch_to_iframe(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> None:
        """
        iframeに切り替える
        
        Args:
            locator: (検索方法, 検索値)のタプル
            timeout: 待機時間（秒）
        """
        iframe = self.find(locator, timeout)
        self.driver.switch_to.frame(iframe)
    
    def switch_to_default_content(self) -> None:
        """
        デフォルトのコンテンツに戻る
        """
        self.driver.switch_to.default_content()
    
    def accept_alert(self, timeout: Optional[int] = None) -> None:
        """
        アラートを受け入れる
        
        Args:
            timeout: 待機時間（秒）
        """
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
    
    def dismiss_alert(self, timeout: Optional[int] = None) -> None:
        """
        アラートを却下する
        
        Args:
            timeout: 待機時間（秒）
        """
        if timeout is None:
            timeout = settings.EXPLICIT_WAIT
        
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        self.driver.switch_to.alert.dismiss()
    
    def take_screenshot(self, filename: str) -> str:
        """
        スクリーンショットを撮る
        
        Args:
            filename: 保存するファイル名
            
        Returns:
            str: スクリーンショットのパス
        """
        import os
        from datetime import datetime
        
        os.makedirs(settings.SCREENSHOT_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(settings.SCREENSHOT_DIR, f"{filename}_{timestamp}.png")
        self.driver.save_screenshot(filepath)
        return filepath