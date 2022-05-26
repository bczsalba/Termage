`Termage` allows you to generate up-to-date, reproducible and _real_ screenshots of Python output while building your documentation. It uses [PyTermGUI](https://github.com/bczsalba/pytermgui) to create the SVGs, and pre-processes your markdown file into a `codefences` format.

!!! info
    Termage requires the following markdown extensions:

    - attr-list
    - pymdown-superfences
    - pymdown-tabbed


```termage height=10 width=60
from pytermgui import highlight_python, tim

code = """
while True:
    if condition:
        print("Hello")
    else:
        print("Goodbye")

    input()

"""

tim.print(highlight_python(code))
```


## Installation

`Termage` is best installed using `pip`:

```
$ pip install mkdocs-termage-plugin
```

This installs the plugin, as well as PyTermGUI as a dependency. By this point you probably _should_ already have mkdocs installed.


## Setup

To use the plugin, you should first add it to your `mkdocs.yml` plugin list:

```yaml title="mkdocs.yml"
plugins:
    - termage
```

!!! warning
    Termage should be loaded before any other markdown pre-processor plugins, to avoid conflicts while formatting.

Additionally, you need to make sure some markdown extensions are enabled:

```yaml title="mkdocs.yml"
markdown_extensions:
  - attr_list
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
```
