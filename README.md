# Termage

See the [docs](https://termage.bczsalba.com) for some live examples.

`Termage` allows you to generate up-to-date, reproducible and _real_ screenshots of Python output while building your documentation. It uses [PyTermGUI](https://github.com/bczsalba/pytermgui) to create the SVGs, and pre-processes your markdown file into a `codefences` format.

![Code](https://raw.githubusercontent.com/bczsalba/mkdocs-termage-plugin/master/assets/code.png)
![Output](https://raw.githubusercontent.com/bczsalba/mkdocs-termage-plugin/master/assets/output.png)


## Installation

`Termage` is best installed using `pip`:

```
$ pip install mkdocs-termage-plugin
```

This installs the plugin, as well as PyTermGUI as a dependency. By this point you probably _should_ already have mkdocs installed.


## Setup

To use the plugin, you should first add it to your `mkdocs.yml` plugin list:

```yaml
plugins:
    - termage
```
