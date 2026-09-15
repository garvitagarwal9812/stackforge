from setuptools import setup, find_packages

setup(
    name="stackforge-dev",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "prompt_toolkit>=3.0.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0",
        "click>=8.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "stackforge=stackforge.cli:main",
        ],
    },
)
