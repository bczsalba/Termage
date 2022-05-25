from setuptools import setup, find_packages

import mkdocs_termage_plugin as termage

setup(
    name="mkdocs-termage-plugin",
    version=termage.__version__,
    packages=find_packages(),
    license="MIT",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["pytermgui>=6.2.1"],
    python_requires=">=3.7.0",
    url="https://github.com/bczsalba/mkdocs-termage-plugin",
    author="BcZsalba",
    author_email="bczsalba@gmail.com",
    entry_points={
        "mkdocs.plugins": [
            "termage = mkdocs_termage_plugin:TermagePlugin",
        ]
    },
)
