Regardless of your entrypoint, the options available are going to be the same.


### Include

Includes a file within a codeblock. The file path must originate from the same directory as `mkdocs.yml`.

For example, let's say we have the following structure:

```
mkdocs.yml
docs/
    index.md 
    src/
        intro01.py
        intro02.py
```

To include `intro01.py` into a Termage block within `index.md`, you could use:

````
\```termage include=docs/src/intro01.py
print("Code from the original codeblock is retained!")
```
````

!!! info
    The `include` option will always "prefix" the actual codeblock's value with whatever is included.

    As such, if `docs/src/intro01.py` had the content:

    ```python3
    print("Included text will always preface the real value of a codeblock")
    ```

    Termage will parse the block as:

    ````markdown
    \```termage <options>
    print("Included text will always preface the real value of a codeblock")
    print("Code from the original codeblock is retained!")
    ```
    ````


### Hide lines

The plugin has a special bit of syntax to signify `Run this line of code, but don't display it`. It is denoted by prefacing any hidden line with an ampersand (&):

!!! note ""

    ```` title="Source"
    \```termage title=Hidden\ lines
    &from pytermgui.pretty import print

    print(locals())
    ```
    ````

    ```termage title=Hidden\ lines
    &from pytermgui.pretty import print

    print(locals())
    ```



### Width and Height

Sets the terminal's dimension of the given axis. Must be given an integer, which will be taken as a character-count.

=== "`width=50` `height=10`"

    ```termage-svg include=docs/src/dimension_demo.py width=50 height=10
    ```

=== "`width=100` `height=20`"

    ```termage-svg include=docs/src/dimension_demo.py width=100 height=20
    ```

!!! info
    If no dimensions are provided, they default to (80, 24).



### Foreground & Background

Modifies the terminal's default colors. `foreground` is used for all non-styled text, and background is used as both the background to the terminal's contents as well as the window that it emulates.

=== "Default"

    ```termage-svg
    print("Hello")
    ```

=== "`foreground=green` `background=#DDDDDD`"

    ```termage-svg foreground=green background=#DDDDDD
    print("Hello")
    ```

!!! info
    Foreground defaults to __#DDDDDD__, and background defaults to __#212121__.


### Tabs

Sets the text labels of each of the tabs.

Accepts two values, delimited by a single `,`. The first value is used for the Python code, and the second is used for the SVG output.

=== "Default"

    ```termage include=docs/src/dimension_demo.py
    ```

=== "`tabs=Code,SVG`"

    ```termage include=docs/src/dimension_demo.py tabs=Code,SVG
    ```

### Title

Sets the title at the top of the output terminal.

!!! warning
    When using the plugin, make sure to escape any spaces present in your title!

    For example, instead of `title=My title`, or `title="My title"` use `title=My\ Title`.

=== "Default"

    ```termage-svg include=docs/src/dimension_demo.py
    ```

=== "`title=My\ fancy\ title`"

    ```termage-svg title=My\ fancy\ title include=docs/src/dimension_demo.py 
    ```
