"""
セットアップファイル
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="selenium-web-testing",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Pythonを使用したSeleniumウェブテストフレームワーク",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/selenium-web-testing",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pytest>=7.0.0",
        "selenium>=4.0.0",
        "webdriver-manager>=4.0.0",
        "pytest-html>=3.0.0",
    ],
)