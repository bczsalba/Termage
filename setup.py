from setuptools import setup, find_packages

import pytermgui

setup(
    name="mkdocs-termage-plugin",
    version=pytermgui.__version__,
    packages=find_packages(),
    license="MIT",
    description="",
    # long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    python_requires=">=3.7.0",
    url="https://github.com/bczsalba/mkdocs-termage",
    author="BcZsalba",
    author_email="bczsalba@gmail.com",
    # entry_points={"console_scripts": ["ptg = pytermgui.cmd:main"]},
    entry_points={
        "mkdocs.plugins": [
            "termage = mkdocs_termage_plugin:TermagePlugin",
        ]
    },
)
