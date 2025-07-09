"""
Setup script for steamscraper package.
This is a backup setup.py for compatibility with older pip versions.
"""

from setuptools import setup, find_packages

setup(
    name="steamscraper",
    version="0.1.0",
    description="Steam game data scraper and parser",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "beautifulsoup4>=4.13.4",
        "requests>=2.32.4",
    ],
    extras_require={
        "dev": [
            "pytest>=8.4.1",
            "pytest-mock>=3.14.1",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)