from setuptools import setup, find_packages

setup(
    name="Termage",
    version="0.2.0",
    packages=find_packages(),
    license="MIT",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[],
    url="https://github.com/bczsalba/termage",
    author="BcZsalba",
    author_email="bczsalba@gmail.com",
    entry_points={
        "console_scripts": ["termage = termage.__main__:main"],
        "mkdocs.plugins": [
            "termage = termage.mkdocs_plugin:TermagePlugin",
        ],
    },
)
