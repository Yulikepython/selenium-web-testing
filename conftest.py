"""
Pytestの共通設定ファイル。
WebDriverの初期化とテスト実行の構成を定義します。
"""

import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 設定ファイルをインポート
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import settings


def pytest_addoption(parser):
    """コマンドラインオプションを追加する"""
    parser.addoption("--browser", action="store", default=settings.BROWSER,
                     help="Select browser: chrome, firefox, edge, safari")
    parser.addoption("--headless", action="store_true", default=settings.HEADLESS,
                     help="Run browser in headless mode")
    parser.addoption("--base-url", action="store", default=settings.BASE_URL,
                     help="Base URL for the tests")


@pytest.fixture(scope="session")
def base_url(request):
    """テスト対象のベースURLを返す"""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="class")
def driver(request):
    """WebDriverのセットアップとティアダウンを行う"""
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    
    # ブラウザ設定
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"Chrome WebDriverの初期化に失敗しました: {e}")
            # 代替方法
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    
    elif browser_name == "safari":
        driver = webdriver.Safari(service=SafariService())
    
    else:
        raise ValueError(f"サポートされていないブラウザ: {browser_name}")
    
    # ウィンドウサイズ設定
    if browser_name != "chrome":  # Chromeの場合は既にオプションで設定済み
        driver.set_window_size(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
    
    # 暗黙的な待機時間を設定
    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    
    # テストに使用するためにdriverをrequest.nodeに保存
    request.cls.driver = driver
    
    # テスト実行後にdriverを閉じる
    yield driver
    
    driver.quit()


@pytest.fixture(scope="function")
def navigate(driver, base_url):
    """指定されたパスに移動するヘルパー関数"""
    def _navigate(path=""):
        # 絶対URLの場合はそのまま使用
        if path.startswith(('http://', 'https://')):
            url = path
        else:
            # 相対パスの場合はベースURLと結合
            url = f"{base_url.rstrip('/')}/{path.lstrip('/')}"
        driver.get(url)
        return driver.current_url
    
    return _navigate


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """テスト失敗時にスクリーンショットを撮影するためのフック"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed and settings.TAKE_SCREENSHOT_ON_FAILURE:
        try:
            driver = item.instance.driver
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = item.nodeid.replace("::", "_").replace(".py", "").replace("/", "_")
            screenshot_dir = settings.SCREENSHOT_DIR
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{test_name}_{timestamp}.png")
            driver.save_screenshot(screenshot_path)
            print(f"スクリーンショットを保存しました: {screenshot_path}")
        except Exception as e:
            print(f"スクリーンショットの撮影に失敗しました: {e}")