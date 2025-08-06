from setuptools import setup, find_packages

setup(
    name="sanitor",
    version="0.1",
    packages=find_packages(),       # sanitor/ package
    py_modules=["sanitor_cli"],     # top-level CLI script
    entry_points={
        "console_scripts": [
            "sanitor = sanitor_cli:main",
        ],
    },
)