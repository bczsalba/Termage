`Termage` is a wrapper library for [PyTermGUI](https://github.com/bczsalba/pytermgui)'s SVG export functionalities. Other than providing the module, it also offers a [CLI](cli.md) and an [MkDocs plugin](plugin.md) to put SVGs just about anywhere you can think of.

!!! success ""
    Termage has native support for capturing applications based on `PyTermGUI`'s `WindowManager`!


```termage title=Hey\ there!
from pytermgui import tim, ColorPicker
from pytermgui.pretty import print

tim.print("Welcome to [!gradient(112) bold]Termage[/]!\n")
tim.print("Termage allows you to display [italic]any[/italic] terminal output in a terminal-mimicking [bold]SVG[/bold]!")

tim.print("\nHere are the current locals:")
print(locals())
```


## Installation

`Termage` is best installed using `pip`:

```
$ pip install termage
```

This will install PyTermGUI, as well as Termage. The MkDocs plugin is included within the installation as well.

```termage include=source_file.py title=My\ SVG width=84 height=15
```
